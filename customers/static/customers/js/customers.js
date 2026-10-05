let allCustomers = [];

const customerTableBody = document.getElementById("customerTableBody");


// ===============================
// Load Customers
// ===============================

async function loadCustomers() {

    try {

        const response = await fetch("/api/customers/");

        if (!response.ok) {
            throw new Error("Failed to fetch customers");
        }

        const customers = await response.json();

        allCustomers = customers;

        displayCustomers(allCustomers);

    } catch (error) {

        console.error("Error loading customers:", error);

    }
}


// ===============================
// Display Customers
// ===============================

function displayCustomers(customers) {

    customerTableBody.innerHTML = "";

    customers.forEach(customer => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${customer.customer_id}</td>

            <td>${customer.full_name}</td>

            <td>${customer.email}</td>

            <td>${customer.kyc_status}</td>

            <td>${customer.risk_level}</td>

            <td>${customer.account_status}</td>

            <td>
                <button class="edit-btn">Edit</button>
                <button
                    class="investigate-btn"
                    data-id="${customer.id}"
                >
                    Investigate
                </button>
            </td>   
        `;

        customerTableBody.appendChild(row);

    });
}
document.addEventListener("click", function (event) {

    if (event.target.classList.contains("investigate-btn")) {

        const customerId = event.target.dataset.id;

        window.location.href =
            `/dashboard/customers/${customerId}/investigate/`;
    }

});


// ===============================
// Search Customers
// ===============================

const searchCustomer =
    document.getElementById("searchCustomer");

const searchCustomerBtn =
    document.getElementById("searchCustomerBtn");


searchCustomerBtn.addEventListener("click", () => {

    const searchText =
        searchCustomer.value.trim().toLowerCase();


    const filteredCustomers = allCustomers.filter(customer =>

        customer.customer_id
            .toLowerCase()
            .includes(searchText)

        ||

        customer.full_name
            .toLowerCase()
            .includes(searchText)

        ||

        customer.email
            .toLowerCase()
            .includes(searchText)

    );


    displayCustomers(filteredCustomers);

});


// ===============================
// Load customers when page opens
// ===============================

loadCustomers();


// ===============================
// Customer Modal
// ===============================

const addCustomerBtn =
    document.getElementById("addCustomerBtn");

const customerModal =
    document.getElementById("customerModal");

const closeModalBtn =
    document.getElementById("closeModalBtn");

const cancelBtn =
    document.getElementById("cancelBtn");


addCustomerBtn.addEventListener("click", () => {

    customerModal.style.display = "flex";

});


closeModalBtn.addEventListener("click", () => {

    customerModal.style.display = "none";

});


cancelBtn.addEventListener("click", () => {

    customerModal.style.display = "none";

});


// ===============================
// Create Customer
// ===============================

const customerForm =
    document.getElementById("customerForm");


customerForm.addEventListener("submit", async (event) => {

    event.preventDefault();


    const csrfToken =
        document.querySelector(
            "[name=csrfmiddlewaretoken]"
        ).value;


    const customerData = {

        customer_id:
            document.getElementById("customer_id").value,

        full_name:
            document.getElementById("full_name").value,

        email:
            document.getElementById("email").value,

        phone:
            document.getElementById("phone").value,

        date_of_birth:
            document.getElementById("date_of_birth").value,

        address:
            document.getElementById("address").value,

        kyc_status:
            document.getElementById("kyc_status").value,

        risk_level:
            document.getElementById("risk_level").value,

        account_status:
            document.getElementById("account_status").value
    };


    try {

        const response = await fetch(
            "/api/customers/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },

                body: JSON.stringify(customerData)
            }
        );


        const data = await response.json();


        if (!response.ok) {

            console.error(
                "Validation errors:",
                data
            );

            alert(
                "Failed to create customer. Check the form values."
            );

            return;
        }


        alert(
            "Customer created successfully!"
        );


        customerForm.reset();

        customerModal.style.display = "none";


        // Reload customers after creation

        loadCustomers();

    }

    catch (error) {

        console.error(
            "Error creating customer:",
            error
        );

        alert(
            "Something went wrong while creating the customer."
        );

    }

});