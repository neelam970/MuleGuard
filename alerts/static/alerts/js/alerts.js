const alertTableBody = document.getElementById("alertTableBody");


async function loadAlerts() {

    try {

        const response = await fetch("/api/alerts/");

        if (!response.ok) {
            throw new Error("Failed to fetch alerts");
        }

        const alerts = await response.json();

        displayAlerts(alerts);

    } catch (error) {

        console.error("Error loading alerts:", error);

        alertTableBody.innerHTML = `
            <tr>
                <td colspan="8">
                    Failed to load alerts.
                </td>
            </tr>
        `;
    }
}


function displayAlerts(alerts) {

    alertTableBody.innerHTML = "";

    if (alerts.length === 0) {

        alertTableBody.innerHTML = `
            <tr>
                <td colspan="8">
                    No alerts found.
                </td>
            </tr>
        `;

        return;
    }

    alerts.forEach(alert => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${alert.alert_id}</td>

            <td>
                ${alert.customer_id} - ${alert.customer_name}
            </td>

            <td>
                ${alert.transaction_id}
            </td>

            <td>
                ${alert.rule}
            </td>

            <td>
                ${alert.risk_score}
            </td>

            <td>
                <span class="severity ${alert.severity.toLowerCase()}">
                    ${alert.severity}
                </span>
            </td>

            <td>
                <span class="status ${alert.status.toLowerCase()}">
                    ${alert.status.replace("_", " ")}
                </span>
            </td>

            <td>
                ${new Date(alert.created_at).toLocaleString()}
            </td>
            <td>
<button class="investigate-alert-btn" data-id="${alert.id}">
    Investigate
</button>
            </td>
        `;

        alertTableBody.appendChild(row);
    });
}
document.addEventListener("click", function (event) {

    if (event.target.classList.contains("investigate-alert-btn")) {

        const alertId = event.target.dataset.id;

        window.location.href = `/dashboard/alerts/${alertId}/`;
    }

});


loadAlerts();