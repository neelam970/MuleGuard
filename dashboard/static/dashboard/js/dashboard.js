document.addEventListener("DOMContentLoaded", function () {

    // Transaction Activity Chart
    const transactionCtx = document.getElementById("transactionChart");

    if (transactionCtx) {
        new Chart(transactionCtx, {
            type: "line",

            data: {
                labels: [
                    "Mon",
                    "Tue",
                    "Wed",
                    "Thu",
                    "Fri",
                    "Sat",
                    "Sun"
                ],

                datasets: [{
                    label: "Transactions",
                    data: [120, 190, 150, 220, 180, 250, 210],
                    borderWidth: 2,
                    tension: 0.4,
                    fill: false
                }]
            },

            options: {
                responsive: true,

                plugins: {
                    legend: {
                        display: true
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }


    // Risk Distribution Chart
    const riskCtx = document.getElementById("riskChart");

    if (riskCtx) {
        new Chart(riskCtx, {
            type: "doughnut",

            data: {
                labels: [
                    "Low Risk",
                    "Medium Risk",
                    "High Risk"
                ],

                datasets: [{
                    label: "Risk Distribution",
                    data: [60, 25, 15],
                    borderWidth: 1
                }]
            },

            options: {
                responsive: true,

                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }

});