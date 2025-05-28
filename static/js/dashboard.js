const ctx = document.getElementById('salesChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Sales',
                    data: [200, 200, 200, 200, 300, 400],
                    backgroundColor: [
                        'rgba(37,99,235,0.7)',
                        'rgba(37,99,235,0.7)',
                        'rgba(37,99,235,0.7)',
                        'rgba(37,99,235,0.7)',
                        'rgba(37,99,235,0.7)',
                        'rgba(37,99,235,1)'
                    ],
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { display: false }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: '#e5e7eb' }
                    }
                }
            }
        });

