<script>
    import { onMount } from "svelte";
    import { articles } from '../articles/index.js';
    import ArticleCard from '../components/ArticleCard.svelte';

    onMount(() => {
        const script = document.createElement("script");
        script.setAttribute("async", "");
        script.setAttribute("src", "https://platform.twitter.com/widgets.js");
        script.setAttribute("charset", "utf-8");
        document.body.appendChild(script);
    });
</script>

<div>
    <p class="py-3">
        Gracias al trabajo del equipo a cargo de la <strong class="text-primary"><a href="http://basededatos.parquedelamemoria.org.ar" target="_blank">Base de Datos de Consulta Pública del Parque de la Memoria</a></strong>, podemos visualizar el impacto del Terrorismo de Estado perpetrado en la Argentina entre los años 1969 y 1983.
    </p>
    <p class="py-3">
        En dicha base de datos podemos consultar información relativa a la vida y circunstancias de desaparición y/o asesinato de cada una de las personas comprendida en el mismo. Agradecemos a la generosidad del equipo para utilizarla en los diversos artículos de la presente web.
    </p>

    <img
        src="/static/parquedelamemoria.jpg"
        alt="Parque de la memoria"
    />

    <div class="divider textarea-xl py-10">Artículos disponibles</div>

    <ul class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {#each articles as article}
        <li>
            <ArticleCard {...article} />
        </li>
        {/each}
    </ul>

    <div class="divider"></div>

    <p class="py-3">
        Los artículos listados previamente solo vemos números y datos, que si bien son reales y crudos, no dejan de ser fríos... Pero detrás de todos esos datos, hubo vidas que se perdieron, familias que se quebraron para siempre, compañeros y amigos que desaparecieron de golpe...
    </p>
    <p class="py-3">
        Es por eso que éste proyecto también tiene otra cara. Hemos creado un <span class="text-primary"><em>bot</em> de <em>X</em> (ex <em>Twitter</em>)</span> que día a día irá publicando un <em>hilo</em> mencionando los casos ocurridos en esa misma fecha, pero entre los años 1969 y 1983. Este <em>bot</em> es una suerte de intervención digital. Como las <a href="https://www.espaciomemoria.ar/proyectos/baldosas-por-la-memoria/" target="" class="text-primary">"Baldosas por la Memoria"</a> pero en el medio de tu <em>feed</em>. Ayudanos a correr la voz!
    </p>

    <div class="mx-auto w-25">
        <blockquote class="twitter-tweet">
            <a href="https://twitter.com/user/status/1902564824136962475">
                Historias de la Memoria: Seguime en X
            </a>
        </blockquote>
    </div>

    <p class="py-3">
        Porque las víctimas del Terrorismo de Estado no son solamente un número, son caras, nombres, hijos, padres, amores, amistades, historias que nos recuerdan lo importante de mantener viva la <strong>Memoria</strong>.
    </p>

    <p class="py-3 text-secondary">
        <strong>
            Este proyecto seguirá en crecimiento...
        </strong>
    </p>
</div>
