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
                label: 'Asesinatos',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                fill: true,
                pointRadius: 2,
            },
            {
                label: 'Desapariciones',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                pointRadius: 2,
            }
        ]
    };

    const monthOrder = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

    onMount(async () => {
        try {
            const response = await fetch('backend-api/murders-and-kidnappings-by-month-and-year/', {
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
                const monthIndex = monthOrder.indexOf(month);
                const key = `${year}-${month}`;

                if (!aggregatedData[key]) {
                    aggregatedData[key] = {
                        year: year,
                        month: month,
                        murders_count: 0,
                        kidnappings_count: 0
                    };
                }

                aggregatedData[key].murders_count += item.murders_count;
                aggregatedData[key].kidnappings_count += item.kidnappings_count;
            });
            
            const months = [];
            const murdersCounts = [];
            const kidnappingsCounts = [];

            const sortedKeys = Object.keys(aggregatedData).sort((a, b) => {
                const [yearA, monthA] = a.split('-');
                const [yearB, monthB] = b.split('-');
                if (yearA === yearB) {
                    return monthOrder.indexOf(monthA) - monthOrder.indexOf(monthB);
                }
                return yearA - yearB;
            });

            sortedKeys.forEach(key => {
                const { year, month, murders_count, kidnappings_count } = aggregatedData[key];
                const shortMonth = month.slice(0, 3);
                const monthLabel = `${shortMonth} ${year}`;
                if (!months.includes(monthLabel)) {
                    months.push(monthLabel);
                }
                murdersCounts.push(murders_count);
                kidnappingsCounts.push(kidnappings_count);
            });

            chartData.labels = months;
            chartData.datasets[0].data = murdersCounts;
            chartData.datasets[1].data = kidnappingsCounts;
            createChart();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });

    function createChart() {
        const ctx = document.getElementById('murdersAndKidnappingsByMonthAndYearChart').getContext('2d');
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
                        text: 'Asesinatos y desapariciones por mes y año'
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

<canvas id="murdersAndKidnappingsByMonthAndYearChart" width="800" height="900"></canvas>

<style>
    canvas {
        max-width: 100%;
        height: auto;
        margin: 0 auto;
    }
</style>