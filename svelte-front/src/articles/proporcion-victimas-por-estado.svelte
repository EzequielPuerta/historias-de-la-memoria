<script>
    import MurdersAndKidnappings from '../components/charts/MurdersAndKidnappings.svelte';
    import MurdersAndKidnappingsByMonthAndYear from '../components/charts/MurdersAndKidnappingsByMonthAndYear.svelte';
</script>

<div>
    <h1>¿Cuál es la distribución de las víctimas según su estado?</h1>
    <p class="py-3">
        También podemos agrupar a las víctimas por si se sabe que fueron asesinadas o secuestradas y desaparecidas (no se conoce su paradero, por lo tanto no se puede confirmar su asesinato).
    </p>
    <MurdersAndKidnappings />

    <p class="py-3">
        Si agrupamos los casos de asesinatos y desapariciones por mes y año, podemos observar como el Estado fue mucho mas represivo y violento durante el '76 y el '77. A su vez, la cantidad de desapariciones (que hasta el día de hoy no se han podido determinar los paraderos) por lo general siempre fue mayor a la cantidad de asesinatos conocidos.
    </p>
    <MurdersAndKidnappingsByMonthAndYear />
</div>