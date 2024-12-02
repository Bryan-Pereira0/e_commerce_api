#E-commerce API

This application is an E-commerce CRUD API that lets you manage customers, products, orders and user accounts using a MySQL Database and SQLAlchemy.

## How to run
- Clone the repository using this in the terminal **git clone https://github.com/Bryan-Pereira0/e_commerce_api**
- Navigate to the directory containing the repo.
- Run this command to activate a virtual enviroment **python -m venv venv** and this command to activate the virtual enviroment. **venv\Scripts\activate**
- Install the required packages with this command. **pip install flask flask_sqlalchemy flask_marshmallow marshmallow mysql-connector-python**
- Make sure to make a password.py with a my_password variable that is tied to your own MySQL DB.
- Lastly run the application by typing this into the terminal. **python app.py**

## Features

- **Customer Management**
  - Add, view, update, and delete customer information.


- **User Accounts**
  - Manage customer accounts with unique usernames and passwords.


- **Product Catalog**
  - Maintain a list of products with names and prices.


- **Order Processing**
  - Handle orders linked to customers and track order dates.
 
## Usage
- Use an API client like Postman to interact with the endpoints.





