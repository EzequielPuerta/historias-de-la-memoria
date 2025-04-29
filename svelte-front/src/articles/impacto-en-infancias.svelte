<script>
    import AffectedChildrenPerYear from '../components/charts/AffectedChildrenPerYear.svelte'
</script>

<div>
    <p class="py-3">
        Conocemos también muchos casos de personas embarazadas que fueron víctimas del accionar represivo del Estado durante dicho período. Si contabilizamos los mismos, agrupados por año, podemos obtener la cantidad de víctimas embarazadas al momento de ser secuestradas o asesinadas. Muchos de esos embarazos son casos de nietos y nietas recuperados por Las Abuelas de Plaza de Mayo.
    </p>
    <p class="py-3">
        A su vez, sabemos cuantos hijos o hijas tenía cada víctima. Si los sumamos, agrupados por año, podremos tener una noción de cuantos chicos quedaron sin alguno de sus padres.
    </p>
    <p class="py-3">
        Vale aclarar que ésta última sumatoria no tiene (aún) contemplado casos donde <strong>ambos padres fueron víctimas</strong> y podríamos estar considerando dos veces a los mismos hijos. Tampoco se tiene en cuenta los casos donde los propios hijos pudieran ser víctimas. Por último, al contar los embarazos no estamos considerando los casos de <strong>embarazos múltiples</strong> (gemelos, mellizos, trillizos, etc). La cantidad de bebes secuestrados podría ser mayor.
    </p>

    <AffectedChildrenPerYear />
</div>