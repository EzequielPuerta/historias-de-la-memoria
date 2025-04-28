<script>
    import MilitancyByMonthAndYear from '../components/charts/MilitancyByMonthAndYear.svelte'
</script>

<div>
    <h1>¿Qué se sabe sobre la militancia de las víctimas?</h1>
    <p class="py-3">
        Algo interesante que se puede observar en los datos sobre los desaparecidos y asesinados por el Terrorismo de Estado, es su actividad militante. En muchos casos, se conoce si militaban y en que espacios lo hacían.
    </p>
    <p class="py-3">
        Si agrupamos por un lado a quienes se les conoce militancia, y por el otro a quienes no, y los ordenamos por mes y año de desaparición o asesinato, según corresponda, podemos observar que ambas curvas son similares la mayor parte del tiempo, excepto durante los años '76 y '77, donde habíamos visto que el accionar represivo se recrudeció y a su vez, obtenemos muchos mas casos de personas a las que no se le conoce actividad militante.
    </p>
    <p class="py-3">
        <strong>Notar que desconocer su militancia no implica que no hayan sido militantes de algún espacio. Notar que conocer su militancia tampoco implica que hayan sido parte de una organización guerrillera.</strong>
    </p>
    <MilitancyByMonthAndYear />
</div>
