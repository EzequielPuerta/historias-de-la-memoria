<script>
    import { onMount } from "svelte";
    import Youtube from "svelte-youtube-embed";
    import * as d3 from 'd3';
    import { Chart, registerables } from 'chart.js';
    Chart.register(...registerables);

    let rawData = [];
    let fullGraph;
    let nodes = [];
    let links = [];
    let clusterCount = 0;
    let largestClusterSize = 0;
    let clusterSizes = [];
    let clusterChart;

    let filteredGraph;
    let selectedSize = 9;
    let clustersBySize = {};

    onMount(async () => {
        const script = document.createElement("script");
        script.setAttribute("async", "");
        script.setAttribute("src", "https://platform.twitter.com/widgets.js");
        script.setAttribute("charset", "utf-8");
        document.body.appendChild(script);

        try {
            const response = await fetch('backend-api/related-victims');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            rawData = await response.json();
            const { clusterLabels, clusterData } = createFullGraph();
            createClusterChart(clusterLabels, clusterData);
            renderGraph(nodes, links, fullGraph, 800, 1300, 1);
            filterAndRender();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

    function createFullGraph() {
        const clusterFrequency = {};

        rawData.forEach(item => {
            const nodeId = item._id;
            if (!nodes.find(node => node.id === nodeId)) {
                nodes.push({ id: nodeId, name: item.name });
            }

            item.related_victims.forEach(related => {
                const victimId = related.victim._id;
                links.push({ source: nodeId, target: victimId, relationship: related.relationship });
                if (!nodes.find(node => node.id === victimId)) {
                    nodes.push({ id: victimId, name: related.victim.name });
                }
            });
        });

        const clusters = findClusters(nodes, links);
        clusterCount = clusters.length;
        largestClusterSize = Math.max(...clusters.map(cluster => cluster.length));

        clusters.forEach(cluster => {
            const size = cluster.length;
            clusterSizes.push(size);
            clusterFrequency[size] = (clusterFrequency[size] || 0) + 1;

            if (!clustersBySize[size]) {
                clustersBySize[size] = [];
            }
            clustersBySize[size].push(cluster);
        });

        const clusterLabels = Object.keys(clusterFrequency);
        const clusterData = Object.values(clusterFrequency);
        return {clusterLabels, clusterData};
    }

    function renderGraph(nodes, links, graph, width, height, currentScale) {
        const zoom = d3.zoom()
            .scaleExtent([0, 5])
            .on('zoom', (event) => {
                currentScale = event.transform.k;
                g.attr('transform', event.transform);

                g.selectAll('.connected-label').style('font-size', `${Math.max(8, 8 / currentScale)}px`);
                g.selectAll('.edge-label').style('font-size', `${Math.max(8, 8 / currentScale)}px`);
            });

        const svg = d3.select(graph)
            .append('svg')
            .attr('viewBox', `0 0 ${width} ${height}`)
            .attr('preserveAspectRatio', 'xMidYMid meet')
            .classed('w-full h-auto', true)
            .call(zoom);

        const g = svg.append('g');

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-200))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = g.append('g')
            .attr('class', 'links')
            .selectAll('line')
            .data(links)
            .enter().append('line')
            .attr('stroke-width', 1)
            .attr('stroke', 'Gainsboro');

        const node = g.append('g')
            .attr('class', 'nodes')
            .selectAll('g')
            .data(nodes)
            .enter().append('g')
            .attr('class', 'node');
        
        node.append('title').text(d => d.name);

        const circles = node.append('circle')
            .attr('r', 15)
            .attr('fill', 'MediumTurquoise')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended))
            .on('click', function(event, d) {
                const relatedUrl = rawData.find(item => item._id === d.id)?.source_entry.url;
                if (relatedUrl) {
                    window.open(relatedUrl, '_blank');
                }
            });

        const edgeLabels = g.append('g')
            .attr('class', 'edge-labels')
            .selectAll('text')
            .data(links)
            .enter().append('text')
            .attr('class', 'edge-label')
            .attr('text-anchor', 'middle')
            .attr('dy', -5)
            .attr('fill', 'gray');

        circles.on('mouseover', function(event, d) {
            g.selectAll('.connected-label').remove();
            g.selectAll('.edge-label').remove();

            const addLabelWithBackground = (text, x, y) => {
                const group = g.append('g')
                    .attr('class', 'connected-label-group')
                    .attr('transform', `translate(${x}, ${y - 10})`);

                const textElem = group.append('text')
                    .text(text)
                    .attr('text-anchor', 'middle')
                    .style('font-size', `${Math.max(8, 20 / currentScale)}px`)
                    .style('fill', 'white');

                requestAnimationFrame(() => {
                    const bbox = textElem.node().getBBox();
                    group.insert('rect', 'text')
                        .attr('x', bbox.x - 4)
                        .attr('y', bbox.y - 2)
                        .attr('width', bbox.width + 8)
                        .attr('height', bbox.height + 4)
                        .attr('fill', 'black')
                        .attr('rx', 4);
                });
            };

            addLabelWithBackground(d.name, d.x, d.y);

            const connectedNodes = links.filter(link => link.source.id === d.id || link.target.id === d.id);
            connectedNodes.forEach(link => {
                const targetNode = link.source.id === d.id ? link.target : link.source;
                addLabelWithBackground(targetNode.name, targetNode.x, targetNode.y);

                const edgeId = `${d.id}-${targetNode.id}`;
                const existingLabel = g.selectAll('.edge-label')
                    .filter(function() {
                        return d3.select(this).attr('data-edge-id') === edgeId;
                    });

                if (existingLabel.empty()) {
                    g.append('text')
                        .attr('class', 'edge-label')
                        .attr('text-anchor', 'middle')
                        .attr('dy', -5)
                        .attr('fill', 'LightPink')
                        .text(link.relationship)
                        .attr('x', (d.x + targetNode.x) / 2)
                        .attr('y', (d.y + targetNode.y) / 2)
                        .style('font-size', `${Math.max(8, 15 / currentScale)}px`)
                        .attr('data-edge-id', edgeId);
                } else {
                    const currentText = existingLabel.text();
                    existingLabel.text(currentText + ' / ' + link.relationship);
                }

                g.selectAll('.links line')
                    .filter(link => link.source.id === d.id || link.target.id === d.id)
                    .attr('stroke-width', 2)
                    .attr('stroke', 'SlateBlue');
            });
        })
        .on('mouseout', function() {
            g.selectAll('.connected-label').remove();
            g.selectAll('.connected-label-group').remove();
            g.selectAll('.edge-label').remove();

            g.selectAll('.links line')
                .attr('stroke-width', 1)
                .attr('stroke', 'Gainsboro');
        });

        simulation
            .nodes(nodes)
            .on('tick', () => {
                link.attr('x1', d => d.source.x)
                    .attr('y1', d => d.source.y)
                    .attr('x2', d => d.target.x)
                    .attr('y2', d => d.target.y);

                node.attr('transform', d => `translate(${d.x}, ${d.y})`);
                edgeLabels.attr('x', d => (d.source.x + d.target.x) / 2)
                    .attr('y', d => (d.source.y + d.target.y) / 2);
            });

        simulation.force('link').links(links);

        const bounds = d3.extent(nodes, d => d.x);
        const xScale = width / (bounds[1] - bounds[0]);
        const yScale = height / (d3.extent(nodes, d => d.y)[1] - d3.extent(nodes, d => d.y)[0]);
        const scale = Math.min(xScale, yScale);

        const centerX = (bounds[0] + bounds[1]) / 2;
        const centerY = d3.mean(nodes, d => d.y);

        g.attr('transform', `translate(${width / 2 - centerX * scale}, ${height / 2 - centerY * scale}) scale(${scale})`);

        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }
    }

    function filterAndRender() {
        const filteredClusters = clustersBySize[selectedSize] || [];
        const filteredNodeIds = new Set(filteredClusters.flat());
        const filteredNodes = nodes.filter(n => filteredNodeIds.has(n.id));
        const filteredLinks = links.filter(l => 
            filteredNodeIds.has(l.source.id || l.source) &&
            filteredNodeIds.has(l.target.id || l.target)
        );
        d3.select(filteredGraph).select('svg').remove();
        renderGraph(filteredNodes, filteredLinks, filteredGraph, 1000, 800, 1.6);
    }

    function findClusters(nodes, links) {
        const visited = new Set();
        const clusters = [];

        function dfs(nodeId, cluster) {
            visited.add(nodeId);
            cluster.push(nodeId);
            for (const link of links) {
                const nextNodeId = link.source === nodeId ? link.target : link.source.id;
                if (nextNodeId && !visited.has(nextNodeId)) {
                    dfs(nextNodeId, cluster);
                }
            }
        }

        nodes.forEach(node => {
            if (!visited.has(node.id)) {
                const cluster = [];
                dfs(node.id, cluster);
                clusters.push(cluster);
            }
        });

        return clusters;
    }

    function createClusterChart(labels, data) {
        const ctx = document.getElementById('clusterChart').getContext('2d');
        if (clusterChart) {
            clusterChart.destroy();
        }
        clusterChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Histograma de tamaño de clústers',
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 1)',
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Cantidad'
                        },
                        beginAtZero: true,
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Tamaño'
                        }
                    }
                }
            }
        });
    }
</script>

<div>
    <p class="py-3">
        El día de ayer, nuestro <em>bot</em> de <strong>"Historias de la Memoria"</strong> publicó un posteo sobre <a href="https://es.wikipedia.org/wiki/H%C3%A9ctor_Germ%C3%A1n_Oesterheld" target="_blank" class="text-primary">Héctor Germán Oesterheld</a>, a raíz de su secuestro el <strong>27 de abril de 1977</strong> a manos de las Fuerzas Armadas:
    </p>

    <div class="py-6">
        <div class="mx-auto w-25">
            <blockquote class="twitter-tweet">
                <a
                    href="https://twitter.com/user/status/1916507895455273278"
                    aria-label="Tweet sobre la desaparición de Oesterheld">
                </a>
            </blockquote>
        </div>
    </div>

    <p class="py-3">
        Para aquellos que no lo conozcan (y tampoco hayan hecho <em>click</em> en el enlace que dejamos un poco más arriba, en su nombre propio 😉), les presentamos al gran escritor y guionista argentino, quién junto al dibujante <span class="text-primary">Francisco Solano López</span> creó la prestigiosa historieta <a href="https://es.wikipedia.org/wiki/El_Eternauta" target="_blank" class="text-primary">El Eternauta (1957)</a> , considerada una de las más importantes de Latinoamérica. Es llamado el <strong>padre de la historieta moderna argentina</strong>.
    </p>

    <p class="py-3">
        Si, esa serie nueva de <span class="text-primary">Netflix</span> próxima a estrenarse este miércoles <strong>30 de abril</strong>, está basada en dicha historieta de Oesterheld.
    </p>

    <div class="py-6">
        <Youtube id="ykLTd5aTa88" />
    </div>

    <p class="py-3">
        Quizás algo que tampoco conocías sobre él, es que tuvo 4 hijas. Ellas y Oesterheld militaban en Montoneros, algo que afectó el vínculo con su esposa Elsa. Al momento del secuestro de Héctor, dos de sus hijas ya habían sido desaparecidas. <a href="https://basededatos.parquedelamemoria.org.ar/registros/6562/" target="_blank" class="text-primary">Beatriz (20)</a> y <a href="https://basededatos.parquedelamemoria.org.ar/registros/6564/" target="_blank" class="text-primary">Diana (22 años)</a>. Ésta última, embarazada de 6 meses para ese entonces. A su compañero, <a href="https://basededatos.parquedelamemoria.org.ar/registros/652/" target="_blank" class="text-primary">Raul Ernesto Araldi</a> lo asesinaron en Tucumán, en algún momento entre 1976 y 1977. Ya habían sido padres de un hijo que al momento del secuestro de Diana tenía 1 año.
    </p>
    <p class="py-3">
        Este bebé fue dejado por lo militares en Casa Cuna de Tucumán y terminaría con sus abuelos paternos. Muchos años mas tarde, en 2013, <a href="https://www.abuelas.org.ar/nietas-y-nietos/41" target="_blank" class="text-primary">Fernando Araldi Oesterheld</a>, quién fuera ese bebé huérfano y tras haber entregado una muestra de sangre para tratar de encontrar a su hermano o hermana, fue llamado por los Antropólogos Forenses para identificar los restos de su papá.
    </p>

    <p class="py-3">
        Volviendo al '77, y con Oesterheld ya secuestrado, le siguieron las desapariciones de sus otras dos hijas, <a href="https://basededatos.parquedelamemoria.org.ar/registros/6561/" target="_blank" class="text-primary">Estela (25)</a> y <a href="https://basededatos.parquedelamemoria.org.ar/registros/6565/" target="_blank" class="text-primary">Marina (20)</a>. A Estela, intentando escapar, le dispararon y la cargaron herida en una camioneta. A su pareja, <a href="https://basededatos.parquedelamemoria.org.ar/registros/6319/" target="_blank" class="text-primary">Raúl Oscar Mortola</a>, lo desaparecieron horas antes en el mismo operativo. Todo indica que fue fusilado aunque no se pudo corroborar. Ambos tenían un hijo en común de 3 años, <span class="text-primary">Martín Oesterheld Mortola</span>, quién fue entregado a su abuela Elsa Sánchez de Oesterheld.
    </p>
    <p class="py-3">
        Por su parte, Marina había sido secuestrada junto a su compañero <a href="https://basededatos.parquedelamemoria.org.ar/registros/2288/" target="_blank" class="text-primary">Alberto Oscar Seindlis</a>. Su estado sigue siendo desconocido. Ambos esperaban un bebé: Marina estaba embarazada de 8 meses al momento del secuestro. Estando detenido de forma clandestina, a Oesterheld se le informó sobre todo esto, incluso del embarazo de Marina.
    </p>

    <p class="py-3">
        De la tragedia sufrida por la familia Oesterheld a manos del Terrorismo de Estado, solo sobrevivieron 2 nietos y la esposa de Héctor, <a href="https://www.abuelas.org.ar/las-abuelas/622" target="_blank" class="text-primary">Elsa Sánchez de Oesterheld</a>, quién luego integró <span class="text-primary">Abuelas de Plaza de Mayo</span>. Oesterheld además de perder su propia vida, perdió a sus 4 hijas, 3 yernos y 2 nietos nonatos; 10 personas en total... Al día de hoy siguen siendo buscados por su hermano y primo, Fernando y Martín.
    </p>

    <figure class="py-6">
        <img
            src="/static/oesterheld-familia.jpg"
            alt="Familia Oesterheld"
        />
        <figcaption>La familia Oesterheld en su casa de Béccar, durante <em>"los años felices"</em>.</figcaption>
    </figure>

    <div class="divider whitespace-normal break-words text-center py-10 px-4 sm:px-0">¿Que otras familias fueron destruidas?</div>

    <p class="py-3">
        La <strong class="text-primary"><a href="http://basededatos.parquedelamemoria.org.ar" target="_blank">Base de Datos de Consulta Pública del Parque de la Memoria</a></strong> posee la relación familiar de un gran porcentaje de las víctimas totales. Si representamos a cada víctima como un <em>nodo</em> y usamos esa información familiar para generar enlaces entre los mismos, podremos así crear una red.
    </p>
    <p class="py-3">
        Las distintas familias se observarán como conjuntos de víctimas (o nodos) enlazadas entre sí, pero aisladas de los otros conjuntos. Contando la cantidad de víctimas pertenecientes a cada familia resultante tendrémos una noción del impacto de la dictadura en su seno familiar.
    </p>
    
    <div class="flex flex-col md:flex-row justify-center items-start gap-8 mt-8 w-full">
        <div class="flex flex-col gap-8 flex-1 min-w-[300px] max-w-[600px]">
            <div class="card bg-secondary text-secondary-content w-full">
                <div class="card-body">
                    <h2 class="card-title">Información de Clusters</h2>
                    <div class="flex-container">
                        <p class="text-md text-secondary-content">Número de Clusters: <span class="text-secondary-content font-bold">{clusterCount}</span></p>
                        <div class="divider divider-horizontal"></div>
                        <p class="text-md text-secondary-content">Tamaño del Cluster más grande: <span class="text-secondary-content font-bold">{largestClusterSize}</span></p>
                    </div>
                </div>
            </div>
            <canvas id="clusterChart" width="800" height="1000" class="w-full"></canvas>
        </div>
    
        <div class="hidden md:flex divider divider-horizontal"></div>
    
        <div bind:this={fullGraph} class="flex-1 min-w-[300px] max-w-[600px] w-full"></div>
    </div>

    <p class="py-3">
        Son demasiadas familias aisladas unas de otras... es difícil poder apreciar algo en la nube de nombres y relaciones.
    </p>

    <div class="divider whitespace-normal break-words text-center py-10 px-4 sm:px-0">Filtremos a las familias por la cantidad de sus víctimas</div>

    <p class="py-3">
        De esta manera se observa que las familias mas golpeadas fueron los <span class="text-primary">Santucho</span> con 9 víctimas relacionadas en la <strong>Base de Datos</strong>, y los <span class="text-primary">Oesterheld</span>, con 8 víctimas (de las 10 víctimas conocidas y mencionadas anteriormente, no se cuentan los nietos nonatos de Héctor ya que no poseen una entrada propia en la <strong>Base de Datos</strong>).
    </p>

    <p class="py-3">
        Mas allá de este detalle, estos vínculos no están completos. Por ejemplo, en el caso de los Santucho, se sabe que <a href="https://basededatos.parquedelamemoria.org.ar/registros/6408/" target="_blank" class="text-primary">Cristina Silvia Navajas</a>, primer esposa de <a href="https://indice.memoriaabierta.org.ar/item/45074" target="_blank" class="text-primary">Julio Santucho</a> fue víctima del Terrorismo de Estado, pero como su esposo no lo fue, quedó desvinculada del resto de las víctimas de la familia Santucho.
    </p>

    <p class="py-3">
        Sería interesante expandir este análisis con las <em>víctimas simultáneas</em>, es decir aquellas víctimas registradas en la <strong>Base de Datos</strong> que están relacionadas entre sí por haber sido secuestradas o asesinadas durante el mismo evento. Por ejemplo, Cristina fue secuestrada junto a <a href="https://basededatos.parquedelamemoria.org.ar/registros/7841/" target="_blank" class="text-primary">Manuela Elmina Santucho</a> y <a href="https://basededatos.parquedelamemoria.org.ar/registros/3602/" target="_blank" class="text-primary">Alicia Raquel D'Ambra</a> (quién a su vez, también tenía un hermano que luego sería desaparecido, <a href="https://basededatos.parquedelamemoria.org.ar/registros/3601/" target="_blank" class="text-primary">Carlos Alberto D'Ambra</a>). Estos vínculos no están siendo representados... aún.
    </p>

    <div class="flex flex-col justify-center items-center gap-4 mt-8 w-full">
        <div class="form-control w-full max-w-xs">
            <label class="label" for="cluster-size">
                <span class="label-text">Tamaño</span>
            </label>
            <select id="cluster-size" class="select select-bordered" bind:value={selectedSize} on:change={filterAndRender}>
                {#each Array(7).fill(0).map((_, i) => i + 3) as size}
                    <option value={size}>{size}</option>
                {/each}
            </select>
        </div>

        <div bind:this={filteredGraph} class="min-w-[600px] max-w-[1000px] w-full"></div>
    </div>
</div>

<style>
    canvas {
        max-width: 100%;
        height: auto;
        margin: 0 auto;
    }
    .flex-container {
        display: inline-flex;
        align-items: center;
        justify-content: flex-start;
        margin-bottom: 20px;
    }
</style>
