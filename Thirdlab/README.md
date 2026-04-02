# Thirdlab

MVC web application for Lab 3.

Use the Flask server in `app/controllers.py` and the business logic in `app/business_logic`.
Data stored in a SQLite database (`tickets.db`).

## Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Populate the database** (optional):
   ```bash
   python -m app.generate_data data.csv
   ```
3. **Run the web server**:
   ```bash
   python -m app.controllers
   ```
   Then open http://localhost:5000 in your browser.

