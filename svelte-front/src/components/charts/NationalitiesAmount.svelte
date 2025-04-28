<script>
    import { onMount, onDestroy } from 'svelte';
    import { Chart, registerables } from 'chart.js';
    import ChartDataLabels from 'chartjs-plugin-datalabels';
    import zoomPlugin from 'chartjs-plugin-zoom';

    import ValueCard from '../ValueCard.svelte';
    Chart.register(...registerables, ChartDataLabels, zoomPlugin);

    let chart;
    let totalCountries = 0;
    let showFirstElement = true;
    let fullChartData = {
        labels: [],
        datasets: [
            {
                label: 'Cantidad',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 1)',
            }
        ]
    };
    let filteredChartData = {
        labels: [],
        datasets: [
            {
                label: 'Cantidad',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 1)',
            }
        ]
    };

    onMount(async () => {
        try {
            const response = await fetch('backend-api/nationalities-amounts/', {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            data.sort((a, b) => b.count - a.count);
            const nationalities = data.map(item => item.nationality);
            const counts = data.map(item => item.count);

            fullChartData.labels = nationalities;
            fullChartData.datasets[0].data = counts;
            filteredChartData.labels = nationalities.slice(1);
            filteredChartData.datasets[0].data = counts.slice(1);
            totalCountries = data.length;
            createChart();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

    function createChart() {
        const ctx = document.getElementById('nationalitiesAmountChart').getContext('2d');
        if (chart) {
            chart.destroy();
        }
        chart = new Chart(ctx, {
            type: 'bar',
            data: showFirstElement ? fullChartData : filteredChartData,
            options: {
                responsive: true,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: true,
                    },
                    title: {
                        display: true,
                        text: 'Cantidad de víctimas por nacionalidad'
                    },
                    datalabels: {
                        display: false
                    },
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: 'xy',
                        },
                        zoom: {
                            wheel: {
                                enabled: true,
                            },
                            pinch: {
                                enabled: true
                            },
                            enabled: true,
                            mode: 'xy',
                            speed: 0.1,
                            threshold: 2
                        }
                    }
                },
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
                            text: 'Nacionalidades'
                        },
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0,
                        }
                    }
                }
            }
        });
    }

    function toggleFirstElement() {
        showFirstElement = !showFirstElement;
        createChart();
    }

    onDestroy(() => {
        if (chart) {
            chart.destroy();
        }
    });
</script>

<div class="flex flex-col sm:flex-row justify-center items-center gap-10">
    <ValueCard title="Cantidad total de Países" value={totalCountries} />

    <div class="divider divider-horizontal"></div>

    <button
        on:click={toggleFirstElement}
        class="btn btn-primary w-full sm:w-auto"
    >
        {showFirstElement ? 'Ocultar argentinos' : 'Mostrar argentinos'}
    </button>
</div>

<canvas id="nationalitiesAmountChart" width="800" height="1300"></canvas>

<style>
    canvas {
        max-width: 100%;
        height: auto;
        margin: 0 auto;
    }
</style>