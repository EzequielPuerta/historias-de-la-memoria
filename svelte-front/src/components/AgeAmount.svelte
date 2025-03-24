<script>
    import { onMount, onDestroy } from 'svelte';
    import { Chart, registerables } from 'chart.js';
    import ChartDataLabels from 'chartjs-plugin-datalabels';
    import zoomPlugin from 'chartjs-plugin-zoom';

    Chart.register(...registerables, ChartDataLabels, zoomPlugin);

    let minAge = 0;
    let maxAge = 0;
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
            const ageResponse = await fetch('backend-api/min-and-max-ages', {
                method: 'GET',
            });
            if (!ageResponse.ok) {
                throw new Error('Network response was not ok for min and max ages');
            }
            const ageData = await ageResponse.json();
            minAge = ageData[0].min_age;
            maxAge = ageData[0].max_age;

            //----
            const response = await fetch('backend-api/age-amounts/', {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            data.sort((a, b) => a.from - b.from);

            const ageGroups = [];
            const counts = [];

            data.forEach(item => {
                ageGroups.push(item._id);
                counts.push(item.count);
            });

            chartData.labels = ageGroups;
            chartData.datasets[0].data = counts;

            createChart();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

    function createChart() {
        const ctx = document.getElementById('ageAmountChart').getContext('2d');
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
                        text: 'Histograma por edad'
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
                            text: 'Grupos etarios'
                        },
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

<div class="max-w-sm mx-auto mb-4">
    <div class="bg-white border border-gray-200 rounded-lg shadow-md p-4">
        <h2 class="text-lg font-semibold text-gray-800">Rango de edad</h2>
        <p class="text-md text-gray-700">Edad mínima: <span class="font-bold">{minAge}</span></p>
        <p class="text-md text-gray-700">Edad máxima: <span class="font-bold">{maxAge}</span></p>
    </div>
</div>

<canvas id="ageAmountChart" width="800" height="400"></canvas>

<style>
    canvas {
        max-width: 100%;
        height: auto;
        margin: 0 auto;
    }
</style>