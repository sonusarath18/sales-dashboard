document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('salesTrendsChart').getContext('2d');

    fetch('http://127.0.0.1:8000/sales_trends/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const salesTrends = data.sales_trends;

            const dates = salesTrends.map(item => item.date);
            const revenues = salesTrends.map(item => item.revenue);

            console.log("Dates:", dates);
            console.log("Revenues:", revenues);

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Daily Revenue',
                        data: revenues,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.3 
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            title: { display: true, text: 'Date' }
                        },
                        y: {
                            title: { display: true, text: 'Revenue ($)' },
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching or rendering chart:', error));
});
