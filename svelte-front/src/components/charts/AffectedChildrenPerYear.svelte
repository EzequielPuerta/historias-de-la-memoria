<script>
    import { onMount, onDestroy } from 'svelte';
    import { Chart, registerables } from 'chart.js';
    import ChartDataLabels from 'chartjs-plugin-datalabels';
    import zoomPlugin from 'chartjs-plugin-zoom';
    import ValueCard from '../ValueCard.svelte';

    Chart.register(...registerables, ChartDataLabels, zoomPlugin);

    let totalPregnants = 0;
    let chart;
    let chartData = {
        labels: [],
        datasets: [
            {
                label: 'Víctimas embarazadas',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true,
                pointRadius: 2,
            },
            {
                label: 'Infancias que perdieron algún padre',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                pointRadius: 2,
            }
        ]
    };

    onMount(async () => {
        try {
            const response = await fetch('backend-api/pregnants-per-year/', {
                method: 'GET',
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            data.sort((a, b) => a.year - b.year);
            const years = data.map(item => item.year);
            const pregnantCounts = [];

            data.forEach(item => {
                pregnantCounts.push(item.pregnant_count);
            });

            chartData.labels = years;
            chartData.datasets[0].data = pregnantCounts;
            totalPregnants = data.reduce((n, {pregnant_count}) => n + pregnant_count, 0);

            // ----
            const childrenResponse = await fetch('backend-api/children-amounts-by-year/', {
                method: 'GET'
            });

            if (!childrenResponse.ok) {
                throw new Error('Network response was not ok for children counts');
            }

            const childrenData = await childrenResponse.json();
            const totalChildrenCounts = [];
            childrenData.forEach(item => {
                const index = years.indexOf(item.year);
                if (index !== -1) {
                    totalChildrenCounts[index] = item.total_children;
                }
            });
            chartData.datasets[1].data = totalChildrenCounts;
            createChart();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

    function createChart() {
        const ctx = document.getElementById('affectedChildrenPerYearChart').getContext('2d');
        if (chart) {
            chart.destroy();
        }
        chart = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                    },
                    title: {
                        display: true,
                        text: 'Víctimas embarazadas e infancias que perdieron algún padre (por año)'
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
                    y: {
                        beginAtZero: true,
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
    <ValueCard title="Cantidad total de embarazos" value={totalPregnants} />
</div>

<canvas id="affectedChildrenPerYearChart" width="800" height="900"></canvas>

<style>
    canvas {
        max-width: 100%;
        height: auto;
        margin: 0 auto;
    }
</style>