📊 Personal Finance Dashboard
A full-stack web application built with Python and Flask that allows users to track income and expenses, set budgets, and visualize their financial data. The dashboard is interactive, allowing users to filter data and export reports.

Live Demo: [--> Add the Link to your deployed application here when ready! <--]

✨ Features
✅ Secure User Authentication: Users can sign up, log in, and manage their own private accounts with hashed passwords (via Werkzeug).

✅ Full CRUD Functionality: Easily Create, Read, Update, and Delete financial transactions.

✅ Interactive Dashboard: Visualize spending by category with a dynamic pie chart and monitor income vs. expense trends over the last 6 months with a bar chart.

✅ Dynamic Date Filtering: Filter all dashboard data by month and year to explore historical records.

✅ Budget Management: Set and manage monthly budgets for different spending categories on a dedicated page.

✅ Visual Budget Tracking: The dashboard displays real-time progress with intuitive progress bars against set budgets.

✅ Data Export/Import: Export transactions as CSV files and bulk-import transactions for easier management.

⚙️ Project Architecture & Workflow
The application follows the Model-View-Controller (MVC) pattern, where Flask handles the routing and controller logic, connecting the user-facing templates with the backend database models.

🌐 User's Browser
 └── 📄 Renders HTML Templates (/templates)
      └── User interacts with forms (e.g., adds a transaction)
           └── ➡ Sends HTTP Request to Flask
                └── 🔁 Flask Routes (app/routes.py)
                     └── Processes the request
                          └── ✅ Validates user input using Forms (app/forms.py)
                               └── 🔄 Interacts with Database Models (app/models.py)
                                    ├── Performs CRUD operations (Create, Read, Update, Delete)
                                    └── 💾 Database (PostgreSQL / SQLite)
                                         └── Stores user data, transactions, and budgets
                                              └── 🔁 Returns data to the Flask Route
                                                   └── 📄 Renders a new HTML template with the updated data


🛠️ Tech Stack
Backend:
Python

Flask & Flask-SQLAlchemy

Werkzeug (Password Hashing)

Gunicorn (Production Server)

Frontend:
HTML5

Pico.css (for styling)

JavaScript

Chart.js (for data visualization)

Database:
PostgreSQL (Production)

SQLite (Development)

📸 Screenshots
Important: Take screenshots of your running application and add them here!

Dashboard View:
(Replace this line with your dashboard screenshot)

Budgets Page:
(Replace this line with your budgets page screenshot)

🚀 Setup & Local Installation
To run this project on your own machine, follow these steps:

Clone the repository:

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

Create and activate a Python virtual environment:

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt

Run the application:

python run.py

Open your browser and navigate to http://127.0.0.1:5000.
