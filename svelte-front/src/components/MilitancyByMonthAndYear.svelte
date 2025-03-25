<!-- src/MurdersAndKidnappings.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import { Chart, registerables } from 'chart.js';
    import zoomPlugin from 'chartjs-plugin-zoom';

    Chart.register(...registerables, zoomPlugin);

    let chart;
    let chartData = {
        labels: [],
        datasets: [
            {
                label: 'Militantes',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true,
            },
            {
                label: 'Militancia desconocida',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
            }
        ]
    };

    const monthOrder = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

    onMount(async () => {
        try {
            const response = await fetch('backend-api/militancy-by-month-and-year/', {
                method: 'GET'
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            const aggregatedData = {};
            data.forEach(item => {
                const year = item.year;
                const month = item.month;
                const key = `${year}-${month}`;

                if (!aggregatedData[key]) {
                    aggregatedData[key] = {
                        year: year,
                        month: month,
                        with_militancy: 0,
                        without_militancy: 0
                    };
                }

                aggregatedData[key].with_militancy += item.with_militancy;
                aggregatedData[key].without_militancy += item.without_militancy;
            });
            
            const months = [];
            const withMilitancy = [];
            const withoutMilitancy = [];

            const sortedKeys = Object.keys(aggregatedData).sort((a, b) => {
                const [yearA, monthA] = a.split('-');
                const [yearB, monthB] = b.split('-');
                
                if (yearA === yearB) {
                    return monthOrder.indexOf(monthA) - monthOrder.indexOf(monthB);
                }
                return yearA - yearB;
            });

            sortedKeys.forEach(key => {
                const { year, month, with_militancy, without_militancy } = aggregatedData[key];
                const shortMonth = month.slice(0, 3);
                const monthLabel = `${shortMonth} ${year}`;
                if (!months.includes(monthLabel)) {
                    months.push(monthLabel);
                }
                withMilitancy.push(with_militancy);
                withoutMilitancy.push(without_militancy);
            });

            chartData.labels = months;
            chartData.datasets[0].data = withMilitancy;
            chartData.datasets[1].data = withoutMilitancy;
            createChart();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

    function createChart() {
        const ctx = document.getElementById('militancyByMonthAndYearChart').getContext('2d');
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
                        text: 'Víctimas militantes por mes y año'
                    },
                    datalabels: {
                        display: false
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

<canvas id="militancyByMonthAndYearChart" width="800" height="900"></canvas>

<style>
    canvas {
        max-width: 100%;
        height: auto;
        margin: 0 auto;
    }
</style>