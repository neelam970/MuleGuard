const updateStatusBtn =
    document.getElementById("updateAlertStatusBtn");


updateStatusBtn.addEventListener("click", async function () {

    const alertId = this.dataset.alertId;

    const status =
        document.getElementById("alertStatus").value;

    const csrfToken =
        document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {

        const response = await fetch(
            `/api/alerts/${alertId}/`,
            {
                method: "PATCH",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },

                body: JSON.stringify({
                    status: status
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {

            console.error("API Error:", data);

            alert(
                "Failed to update alert status."
            );

            return;
        }

        alert(
            "Alert status updated successfully!"
        );

        window.location.reload();

    } catch (error) {

        console.error(
            "Error updating alert:",
            error
        );

        alert(
            "Something went wrong."
        );
    }
});