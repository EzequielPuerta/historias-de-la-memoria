<script>
    import { onMount, onDestroy } from 'svelte';
    import { Chart, registerables } from 'chart.js';
    import ChartDataLabels from 'chartjs-plugin-datalabels';

    Chart.register(...registerables, ChartDataLabels);

    let chart;
    let chartData = {
        labels: [],
        datasets: [{
            label: 'Cantidad',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(255, 206, 86, 1)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',    
                'rgba(75, 192, 192, 1)',
                'rgba(255, 206, 86, 1)',
            ],
            borderWidth: 1
        }]
    };

    onMount(async () => {
        try {
            const response = await fetch('backend-api/murders-and-kidnappings/', {
                method: 'GET',
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            chartData.labels = data.map(item => item.fact_type);
            chartData.datasets[0].data = data.map(item => item.count);
            createChart();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

    function createChart() {
        const ctx = document.getElementById('murdersAndKidnappingsChart').getContext('2d');
        if (chart) {
            chart.destroy();
        }
        chart = new Chart(ctx, {
            type: 'pie',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Cantidad de víctimas'
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'end'
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

<canvas id="murdersAndKidnappingsChart" width="400" height="400"></canvas>

<style>
    canvas {
        max-width: 100%;
        height: auto;
        margin: 0 auto;
    }
</style>