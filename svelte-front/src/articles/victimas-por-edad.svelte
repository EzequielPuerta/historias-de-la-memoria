<script>
    import AgeAmount from '../components/charts/AgeAmount.svelte'
</script>

<div>
    <h1>¿Qué edades tenían las víctimas al momento de su desaparición/asesinato?</h1>
    <p class="py-3">
        Podemos también considerar la edad de cada víctima y agruparlas en bloques de 5 años, para realizar un histograma de frecuencias. De esta manera observamos que hubo víctimas de todas las edades, en un rango desde los primeros meses de vida, hasta la edad de 81 años. La gran mayoría, eran jóvenes de entre 20 y 30 años.
    </p>

    <AgeAmount />
</div>