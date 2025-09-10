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

📂 Raw Data Files
 ├── 📄 PDFs (RBI Reports, Budgets, etc.)
 ├── 📊 CSVs (G-Sec Auctions, State Indicators)

➡ Data Processing Backend (/notebooks)
 ├── 🧠 RAG Pipeline → data_ingestion_and_cleaning.ipynb
 ├── 🗄️ SQL Pipeline → structured_data_sql.ipynb, add_auction_data_to_db.ipynb
 ├── 📈 Forecasting Pipeline → create_forecasting_dataset.ipynb, build_forecasting_model.ipynb

➡ Processed Assets
 ├── 📦 /data/processed
 └── 📂 /vector_store

➡ Databases & Tools
 ├── 🧠 Chroma Vector Store
 ├── 🗃️ SQLite Database → esd_indicators.sqlite
 └── 📊 Forecasting Dataset → final_forecasting_dataset.csv

➡ Frontend & Logic (app.py)
 ├── 🎨 Streamlit UI (Chat Interface)
 ├── 🧠 LangChain AgentExecutor (The Brain)
 └── 🛠️ Tools → PDF Search, SQL Query, Forecasting

## 📂 Folder Structure


