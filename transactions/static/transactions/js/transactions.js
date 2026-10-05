const transactionTableBody =
    document.getElementById("transactionTableBody");


// =====================================================
// LOAD CUSTOMERS
// =====================================================

async function loadCustomers() {

    try {

        const response = await fetch("/api/customers/");

        if (!response.ok) {
            throw new Error("Failed to fetch customers");
        }

        const customers = await response.json();

        const senderSelect =
            document.getElementById("sender");

        const receiverSelect =
            document.getElementById("receiver");

        customers.forEach(customer => {

            // Sender option
            const senderOption =
                document.createElement("option");

            senderOption.value = customer.id;

            senderOption.textContent =
                `${customer.customer_id} - ${customer.full_name}`;

            senderSelect.appendChild(senderOption);


            // Receiver option
            const receiverOption =
                document.createElement("option");

            receiverOption.value = customer.id;

            receiverOption.textContent =
                `${customer.customer_id} - ${customer.full_name}`;

            receiverSelect.appendChild(receiverOption);

        });

    } catch (error) {

        console.error(
            "Error loading customers:",
            error
        );

    }
}


// =====================================================
// LOAD TRANSACTIONS
// =====================================================

async function loadTransactions() {

    try {

        const response =
            await fetch("/api/transactions/");

        if (!response.ok) {
            throw new Error(
                "Failed to fetch transactions"
            );
        }

        const transactions =
            await response.json();

        displayTransactions(transactions);

    } catch (error) {

        console.error(
            "Error loading transactions:",
            error
        );

    }
}


// =====================================================
// DISPLAY TRANSACTIONS
// =====================================================

function displayTransactions(transactions) {

    transactionTableBody.innerHTML = "";

    transactions.forEach(transaction => {

        const row =
            document.createElement("tr");

        row.innerHTML = `

            <td>
                ${transaction.transaction_id}
            </td>

            <td>
                ${transaction.sender_customer_id}
                -
                ${transaction.sender_name}
            </td>

            <td>
                ${transaction.receiver_customer_id}
                -
                ${transaction.receiver_name}
            </td>

            <td>
                ₹${transaction.amount}
            </td>

            <td>
                ${transaction.transaction_type}
            </td>

            <td>
                ${transaction.transaction_date}
            </td>

            <td>
                ${transaction.status}
            </td>

            <td>

                <button
                    class="view-btn"
                    data-id="${transaction.id}"
                >
                    View
                </button>

            </td>
        `;

        transactionTableBody.appendChild(row);

    });
}


// =====================================================
// VIEW TRANSACTION
// =====================================================

document.addEventListener(
    "click",
    function (event) {

        if (
            event.target.classList.contains(
                "view-btn"
            )
        ) {

            const transactionId =
                event.target.dataset.id;

            window.location.href =
                `/dashboard/transactions/${transactionId}/`;
        }

    }
);


// =====================================================
// ADD TRANSACTION MODAL
// =====================================================

const addTransactionBtn =
    document.getElementById(
        "addTransactionBtn"
    );

const transactionModal =
    document.getElementById(
        "transactionModal"
    );

const closeTransactionModalBtn =
    document.getElementById(
        "closeTransactionModalBtn"
    );

const cancelTransactionBtn =
    document.getElementById(
        "cancelTransactionBtn"
    );


// Open modal

addTransactionBtn.addEventListener(
    "click",
    function () {

        transactionModal.style.display =
            "flex";

    }
);


// Close modal using X

closeTransactionModalBtn.addEventListener(
    "click",
    function () {

        transactionModal.style.display =
            "none";

    }
);


// Close modal using Cancel

cancelTransactionBtn.addEventListener(
    "click",
    function () {

        transactionModal.style.display =
            "none";

    }
);


// =====================================================
// ADD TRANSACTION FORM
// =====================================================

const transactionForm =
    document.getElementById(
        "transactionForm"
    );


transactionForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // ---------------------------------------------
        // GET FORM VALUES
        // ---------------------------------------------

        const transactionId =
            document
                .getElementById("transaction_id")
                .value
                .trim();

        const sender =
            document
                .getElementById("sender")
                .value;

        const receiver =
            document
                .getElementById("receiver")
                .value;

        const amount =
            document
                .getElementById("amount")
                .value;

        const transactionType =
            document
                .getElementById("transaction_type")
                .value;

        const transactionDate =
            document
                .getElementById("transaction_date")
                .value;

        const description =
            document
                .getElementById("description")
                .value
                .trim();

        const transactionStatus =
            document
                .getElementById("status")
                .value;


        // ---------------------------------------------
        // FRONTEND VALIDATION
        // ---------------------------------------------

        // Transaction ID

        if (!transactionId) {

            alert(
                "Transaction ID is required."
            );

            return;
        }


        // Sender

        if (!sender) {

            alert(
                "Please select a sender."
            );

            return;
        }


        // Receiver

        if (!receiver) {

            alert(
                "Please select a receiver."
            );

            return;
        }


        // Sender and receiver cannot be same

        if (sender === receiver) {

            alert(
                "Sender and receiver cannot be the same customer."
            );

            return;
        }


        // Amount

        if (
            !amount ||
            Number(amount) <= 0
        ) {

            alert(
                "Transaction amount must be greater than 0."
            );

            return;
        }


        // Transaction date

        if (!transactionDate) {

            alert(
                "Transaction date is required."
            );

            return;
        }


        // Future date validation

        const selectedDate =
            new Date(transactionDate);

        const currentDate =
            new Date();

        if (
            selectedDate >
            currentDate
        ) {

            alert(
                "Transaction date cannot be in the future."
            );

            return;
        }


        // ---------------------------------------------
        // CREATE TRANSACTION DATA
        // ---------------------------------------------

        const transactionData = {

            transaction_id:
                transactionId.toUpperCase(),

            sender:
                Number(sender),

            receiver:
                Number(receiver),

            amount:
                Number(amount),

            transaction_type:
                transactionType,

            transaction_date:
                transactionDate,

            description:
                description,

            status:
                transactionStatus
        };


        // ---------------------------------------------
        // GET CSRF TOKEN
        // ---------------------------------------------

        const csrfToken =
            document.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value;


        // ---------------------------------------------
        // SEND POST REQUEST
        // ---------------------------------------------

        try {

            const response =
                await fetch(
                    "/api/transactions/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json",

                            "X-CSRFToken":
                                csrfToken
                        },

                        body:
                            JSON.stringify(
                                transactionData
                            )
                    }
                );


            const data =
                await response.json();


            // -----------------------------------------
            // API ERROR
            // -----------------------------------------

            if (!response.ok) {

                console.error(
                    "API Error:",
                    data
                );

                alert(
                    "Failed to create transaction:\n" +
                    JSON.stringify(data)
                );

                return;
            }


            // -----------------------------------------
            // SUCCESS
            // -----------------------------------------

            alert(
                "Transaction created successfully!"
            );


            // Close modal

            transactionModal.style.display =
                "none";


            // Clear form

            transactionForm.reset();


            // Reload transaction table

            loadTransactions();

        } catch (error) {

            console.error(
                "Error creating transaction:",
                error
            );

            alert(
                "Something went wrong while creating the transaction."
            );
        }

    }
);


// =====================================================
// INITIAL LOAD
// =====================================================

loadCustomers();

loadTransactions();