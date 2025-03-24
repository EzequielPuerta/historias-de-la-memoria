<script>
    import MurdersAndKidnappings from './components/MurdersAndKidnappings.svelte';
    import MurdersAndKidnappingsByMonthAndYear from './components/MurdersAndKidnappingsByMonthAndYear.svelte';
    import GenreAmount from './components/GenreAmount.svelte';
    import AffectedChildrenPerYear from './components/AffectedChildrenPerYear.svelte'
    import NationalitiesAmount from './components/NationalitiesAmount.svelte'
    import AgeAmount from './components/AgeAmount.svelte'
    import MilitancyByMonthAndYear from './components/MilitancyByMonthAndYear.svelte'
</script>

<main>
    <h1 class="text-2xl font-bold">Historias de la Memoria</h1>
    <p>
        Gracias al trabajo del equipo a cargo de la <a href="http://basededatos.parquedelamemoria.org.ar" target="_blank">Base de Datos de Consulta Pública del Parque de la Memoria</a>, podemos visualizar el impacto del Terrorismo de Estado perpetrado en la Argentina durante los años 1969 y 1983.
    </p>
    <p>
        En dicha base de datos podemos consultar información relativa a la vida y circunstancias de desaparición y/o asesinato de cada una de las personas comprendida en el mismo. Agradecemos a la generosidad del equipo para utilizarla.
    </p>
    <p>
        Si dichos datos los agrupamos y agregamos de diversas maneras, podremos responder distintas preguntas que nos podamos cuestionar al respecto. Por ejemplo:
    </p>

    <h2>¿Cuál es la proporción de víctimas femeninas y masculinas?</h2>
    <GenreAmount />

    <p>
        Notar que actualmente, la base de datos posee información acerca de <strong>8948</strong> víctimas. La misma se encuentra en constante construcción y revisión.
    </p>
    
    <h2>¿Cuál fue el impacto del Terrorismo de Estado en las infancias vinculadas a las víctimas?</h2>
    <p>
        Conocemos también muchos casos de personas embarazadas que fueron víctimas del accionar represivo del Estado durante dicho período. Si contabilizamos los mismos, agrupados por año, podemos obtener la cantidad de víctimas embarazadas al momento de ser secuestradas o asesinadas. Muchos de esos embarazos son casos de nietos y nietas recuperados por Las Abuelas de Plaza de Mayo.
    </p>
    <p>
        A su vez, sabemos cuantos hijos o hijas tenía cada víctima. Si los sumamos, agrupados por año, podremos tener una noción de cuantos chicos quedaron sin alguno de sus padres.
    </p>
    <p>
        Vale aclarar que ésta última sumatoria no tiene (aún) contemplado casos donde ambos padres fueron víctimas y podríamos estar considerando dos veces a los mismos hijos. Tampoco se tiene en cuenta los casos donde los propios hijos pudieran ser víctimas.
    </p>
    <AffectedChildrenPerYear />

    <h2>¿Cuál es la distribución de las víctimas según su estado?</h2>
    <p>
        También podemos agrupar a las víctimas por si se sabe que fueron asesinadas o secuestradas y desaparecidas (no se conoce su paradero, por lo tanto no se puede confirmar su asesinato).
    </p>
    <MurdersAndKidnappings />

    <p>
        Si agrupamos los casos de asesinatos y desapariciones por mes y año, podemos observar como el Estado fue mucho mas represivo y violento durante el '76 y el '77. A su vez, la cantidad de desapariciones (que hasta el día de hoy no se han podido determinar los paraderos) por lo general siempre fue mayor a la cantidad de asesinatos conocidos.
    </p>
    <MurdersAndKidnappingsByMonthAndYear />

    <h2>¿Cuál es la cantidad de víctimas agrupadas por nacionalidad?</h2>
    <p>
        Si agrupamos los casos, esta vez por su nacionalidad, podremos observar que hubo en total 34 nacionalidades afectadas por el Terrorismo de Estado. La enorme mayoría, argentinos, como es de esperar.
    </p>
    <NationalitiesAmount />

    <h2>¿Qué edades tenían las víctimas al momento de su desaparición/asesinato?</h2>
    <p>
        Podemos también considerar la edad de cada víctima y agruparlas en bloques de 5 años, para realizar un histograma de frecuencias. De esta manera observamos que hubo víctimas de todas las edades, en un rango desde los primeros meses de vida, hasta la edad de 81 años. La gran mayoría, eran jóvenes de entre 20 y 30 años.
    </p>
    <AgeAmount />

    <h2>¿Qué se sabe sobre la militancia de las víctimas?</h2>
    <p>
        Algo interesante que se puede observar en los datos sobre los desaparecidos y asesinados por el Terrorismo de Estado, es su actividad militante. En muchos casos, se conoce si militaban y en que espacios lo hacían.
    </p>
    <p>
        Si agrupamos por un lado a quienes se les conoce militancia, y por el otro a quienes no, y los ordenamos por mes y año de desaparición o asesinato, según corresponda, podemos observar que ambas curvas son similares la mayor parte del tiempo, excepto durante los años '76 y '77, donde habíamos visto que el accionar represivo se recrudeció y a su vez, obtenemos muchos mas casos de personas a las que no se le conoce actividad militante.
    </p>
    <p>
        <strong>Notar que desconocer su militancia no implica que no hayan sido militantes de algún espacio. Notar que conocer su militancia tampoco implica que hayan sido parte de una organización guerrillera.</strong>
    </p>
    <MilitancyByMonthAndYear />

    <p>
        Pero hasta ahora solo vimos números y datos, que si bien son reales y crudos, no dejan de ser fríos... Pero detrás de todos esos datos y valores, hubo vidas que se perdieron, familias que se quebraron para siempre, compañeros y amigos que desaparecieron de golpe. Es por eso que éste proyecto también tiene otra cara. Hemos creado un <em>bot</em> de <em>X</em> (ex <em>Twitter</em>) que día a día irá publicando un <em>hilo</em> mencionando los casos ocurridos en esa misma fecha, pero entre los años 1969 y 1983. Este <em>bot</em> es una suerte de intervención digital. Como las <a href="https://www.espaciomemoria.ar/proyectos/baldosas-por-la-memoria/" target="">"Baldosas por la Memoria"</a> pero en el medio de tu <em>feed</em>. Ayudanos a correr la voz!
    </p>

    <a href="https://x.com/HDeLaMemoria" target="">Historias de la Memoria: Seguime en X</a>

    <p>
        Porque las víctimas del Terrorismo de Estado no son solamente un número, son caras, nombres, hijos, padres, amores, amistades, historias que nos recuerdan lo importante de mantener viva la <strong>Memoria</strong>.
    </p>

    <p>Este proyecto seguirá en crecimiento...</p>
</main>

<style>
    main {
        text-align: center;
        padding: 2em;
    }
    h1, h2 {
        margin: 0 20px;
    }
    p {
        text-align: justify;
        margin: 2em 20px;
    }
</style>