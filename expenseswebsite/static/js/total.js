document.addEventListener('DOMContentLoaded', () => {
    fetch('/dashboard/') 
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalRevenue').innerText = `$${data.total_revenue.toFixed(2)}`;
            document.getElementById('totalSales').innerText = data.total_sales;

            const topProductsList = document.getElementById('topProducts');

            topProductsList.innerHTML = '';
            
            data.top_products.forEach(product => {
                const li = document.createElement('li');
                li.textContent = `${product.product_name}: ${product.total_quantity} units sold`;
                topProductsList.appendChild(li);
            });

            const lowStockList = document.getElementById('lowStockProducts');
            data.low_stock_products.forEach(product => {
                const li = document.createElement('li');
                li.classList.add('low-stock');
                li.textContent = `${product.product_name}: ${product.total_quantity} left`;
                lowStockList.appendChild(li);
            });

            const dates = data.sales_trends.map(item => item.date);
            const revenues = data.sales_trends.map(item => item.revenue);

            const ctx = document.getElementById('salesTrendChart').getContext('2d');
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
                    scales: {
                        x: { title: { display: true, text: 'Date' }},
                        y: { title: { display: true, text: 'Revenue ($)' }, beginAtZero: true }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching dashboard data:', error));
});