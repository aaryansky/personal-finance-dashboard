# 💰 Personal Finance Dashboard

An advanced full-stack web application built with **Python** and **Flask** to help users track their income and expenses, set budgets, and visualize their financial data. The platform integrates secure authentication, data visualization, and import/export functionalities to streamline personal finance management.

---

## 🚀 Core Features

The application is powered by Flask and designed to offer seamless interaction with user data across multiple functionalities:

### 1. ✅ Secure User Authentication
- **Functionality:** Users can sign up, log in, and manage accounts securely with hashed passwords using `Werkzeug`.
- **How it Works:** User credentials are safely stored and verified before granting access to personalized financial data.

### 2. 📊 Interactive Dashboard
- **Functionality:** Visualize spending by category with pie charts and track income vs. expenses over time with bar charts.
- **How it Works:** Data is dynamically updated using `Chart.js` based on user input and filtering.

### 3. 📅 Date Filtering & Budget Management
- **Functionality:** Filter data by month and year; set budgets for categories with real-time tracking progress bars.
- **How it Works:** Budgets are compared against actual transactions, and feedback is provided through visual cues.

### 4. 📥 Data Export/Import
- **Functionality:** Export transaction data to CSV files and import bulk transactions for easier management.
- **How it Works:** Transactions are processed and validated before being stored or retrieved from the database.

---

## ⚙️ Project Architecture & Workflow

The project follows the **Model-View-Controller (MVC)** architecture, with Flask handling routing and logic, and user interfaces interacting with backend models.

## 🌐 User Interaction Flow

```mermaid
graph TD

    A[🌐 User's Browser] --> B[📄 Renders HTML Templates\n(/templates)]
    B --> B1[💡 User interacts with forms\n(e.g., adds a transaction)]

    A --> C[➡ Sends HTTP Request to Flask]
    C --> C1[🔁 Flask Routes\n(app/routes.py)]
    C1 --> C2[⚙️ Processes the request]
    C1 --> C3[✅ Validates user input using Forms\n(app/forms.py)]
    C1 --> C4[🔄 Interacts with Database Models\n(app/models.py)]

    C4 --> C5[📂 Performs CRUD operations\n(Create, Read, Update, Delete)]
    C4 --> C6[💾 Database\n(PostgreSQL / SQLite)]
    C6 --> C7[🗄️ Stores user data, transactions, and budgets]
    C6 --> C8[🔁 Returns data to the Flask Route]

    A --> D[📄 Renders a new HTML template\nwith the updated data]

