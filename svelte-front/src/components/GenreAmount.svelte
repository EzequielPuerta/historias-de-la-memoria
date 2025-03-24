<!-- src/GenreAmount.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import { Chart, registerables } from 'chart.js';
    import ChartDataLabels from 'chartjs-plugin-datalabels';

    Chart.register(...registerables, ChartDataLabels);

    let totalVictims = 0;
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
            const response = await fetch('api/genre-amounts/', {
                method: 'GET',
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            chartData.labels = data.map(item => item.genre);
            chartData.datasets[0].data = data.map(item => item.count);
            totalVictims = data.reduce((n, {count}) => n + count, 0);
            createChart();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

    function createChart() {
        const ctx = document.getElementById('genreAmountChart').getContext('2d');
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
                        text: 'Cantidad de víctimas por sexo'
                    },
                    datalabels: {
                        color: '#fff',
                        formatter: (value, context) => {
                            return value;
                        },
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

<div class="max-w-sm mx-auto">
    <div class="bg-white border border-gray-200 rounded-lg shadow-md p-4">
        <h2 class="text-lg font-semibold text-gray-800">Víctimas totales:</h2>
        <p class="text-2xl font-bold text-gray-900">{totalVictims}</p>
    </div>
</div>

<canvas id="genreAmountChart" width="400" height="400"></canvas>

<style>
    canvas {
        max-width: 100%;
        height: auto;
        margin: 0 auto;
    }
</style>