
# Billing System

## Project Description
This is a simple billing system built with Django and PostgreSQL. The system allows users to:
1. Add and manage products in the database.
2. Generate bills dynamically based on customer purchases.
3. Calculate and display balance denominations.
4. View previous purchases of a customer.

## Installation

1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd Billing-System-App
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database and update the `settings.py` file with your credentials.

4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
1. Navigate to the admin panel to add products.
2. Use the billing page to generate bills and view past transactions.

## Notes
- Ensure your PostgreSQL server is running before starting the project.
- Adjust email settings in `settings.py` for invoice emailing.

