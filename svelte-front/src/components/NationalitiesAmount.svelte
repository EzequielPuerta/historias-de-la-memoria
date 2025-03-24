<!-- src/components/NationalitiesAmount.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import { Chart, registerables } from 'chart.js';
    import ChartDataLabels from 'chartjs-plugin-datalabels';
    import zoomPlugin from 'chartjs-plugin-zoom';

    Chart.register(...registerables, ChartDataLabels, zoomPlugin);

    let totalCountries = 0;
    let chart;
    let chartData = {
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
            const response = await fetch('api/nationalities-amounts/', {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            const nationalities = [];
            const counts = [];

            data.forEach(item => {
                nationalities.push(item.nationality);
                counts.push(item.count);
            });
            chartData.labels = nationalities;
            chartData.datasets[0].data = counts;
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
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                    },
                    title: {
                        display: true,
                        text: 'Cantidad de víctimas por nacionalidad'
                    },
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: 'x',
                        },
                        zoom: {
                            wheel: {
                                enabled: true,
                            },
                            pinch: {
                                enabled: true
                            },
                            enabled: true,
                            mode: 'x',
                            speed: 0.1,
                            threshold: 2
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Nacionalidades'
                        },
                        ticks: {
                            maxRotation: 90,
                            minRotation: 90,
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Cantidad'
                        }
                    }
                }
            }
        });
    }

    onDestroy(() => {
        if (chart) {
            chart.destroy();
        }
    });
</script>

<div class="max-w-sm mx-auto">
    <div class="bg-white border border-gray-200 rounded-lg shadow-md p-4">
        <h2 class="text-lg font-semibold text-gray-800">Cantidad total de Países:</h2>
        <p class="text-2xl font-bold text-gray-900">{totalCountries}</p>
    </div>
</div>

<canvas id="nationalitiesAmountChart" width="800" height="600"></canvas>

<style>
    canvas {
        max-width: 100%;
        height: auto;
        margin: 0 auto;
    }
</style>