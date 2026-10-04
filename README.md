# Inventory Management System API

This is a Flask-based inventory management system. It provides a REST API for managing inventory and integrates with the **OpenFoodFacts API** to retrieve product information using a product barcode or product name.

## Features

* Flask REST API
* Full CRUD operations for inventory
* Get all inventory items
* Get a single inventory item by ID
* Add new inventory items
* Update inventory items
* Delete inventory items
* Mock inventory data
* OpenFoodFacts API integration
* Search products by **barcode**
* Search products by **name**
* Add an OpenFoodFacts product directly to the inventory
* Session-based administrator authentication
* Login and logout
* Interactive command-line interface (CLI)
* CLI inventory management
* CLI product lookup and search
* CLI integration with OpenFoodFacts
* Rich-formatted CLI interface
* Input validation
* API and CLI error handling
* Automated testing with pytest

## Technologies

* Python
* Flask
* Requests
* Rich
* Pytest
* OpenFoodFacts API
* Git and GitHub

## Dependencies

The project uses the following Python packages:

* **Flask** — REST API development
* **Requests** — communication with the OpenFoodFacts API
* **Rich** — formatting and styling the command-line interface
* **Pytest** — automated testing

All project dependencies are included in `requirements.txt`.

## Project Structure

```text
inventory-management-system-api/

│
├── app.py
├── cli.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── inventory.py
│
├── services/
│   └── openfoodfacts.py
│
└── tests/
    ├── test_api.py
    ├── test_cli.py
    └── test_openfoodfacts.py
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/modidi/inventory-management-system-api.git

cd inventory-management-system-api
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs Flask, Requests, Rich, Pytest, and the other required dependencies.

## Running the Flask API

Start the Flask application:

```bash
python3 app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## API Routes

### Authentication Routes

| Method | Endpoint  | Description                   |
| ------ | --------- | ----------------------------- |
| POST   | `/login`  | Log in as administrator       |
| POST   | `/logout` | Log out and clear the session |

### Inventory Routes

| Method | Endpoint          | Description              |
| ------ | ----------------- | ------------------------ |
| GET    | `/inventory`      | Get all inventory items  |
| GET    | `/inventory/<id>` | Get one inventory item   |
| POST   | `/inventory`      | Add a new inventory item |
| PATCH  | `/inventory/<id>` | Update an inventory item |
| DELETE | `/inventory/<id>` | Delete an inventory item |

### OpenFoodFacts Routes

| Method | Endpoint                            | Description                                                |
| ------ | ----------------------------------- | ---------------------------------------------------------- |
| GET    | `/product/barcode/<barcode>`        | Find a product using its barcode                           |
| GET    | `/product/name/<name>`              | Search for products by name                                |
| POST   | `/inventory/from-product/<barcode>` | Fetch a product from OpenFoodFacts and add it to inventory |

## Authentication

The API uses Flask sessions for administrator authentication.

### Login

```text
POST /login
```

Use the following administrator credentials:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

A successful login creates an authenticated session.

### Logout

```text
POST /logout
```

This clears the administrator session.

### Protected Routes

The following inventory routes require an authenticated session:

* `GET /inventory`
* `GET /inventory/<id>`
* `POST /inventory`
* `PATCH /inventory/<id>`
* `DELETE /inventory/<id>`
* `POST /inventory/from-product/<barcode>`

If a user tries to access a protected route without logging in, the API returns:

```json
{
  "error": "Login required"
}
```

with HTTP status `401`.

The OpenFoodFacts product search routes remain publicly accessible.

## Inventory CRUD

The REST API supports all four main CRUD operations.

### Create

Add a new inventory item:

```text
POST /inventory
```

Example request:

```json
{
  "name": "Milk",
  "category": "Dairy",
  "price": 150,
  "stock": 20
}
```

### Read

View all inventory items:

```text
GET /inventory
```

View one inventory item:

```text
GET /inventory/1
```

### Update

Update an existing inventory item:

```text
PATCH /inventory/1
```

Example:

```json
{
  "price": 200,
  "stock": 25
}
```

### Delete

Delete an inventory item:

```text
DELETE /inventory/1
```

## Mock Inventory Data

The project uses a simulated in-memory inventory stored in:

```text
data/inventory.py
```

The mock inventory provides sample products that can be viewed, updated, and deleted through the REST API and CLI.

Each inventory item has a unique ID.

Example:

```json
{
  "id": 1,
  "barcode": null,
  "name": "Vanilla Yoghurt",
  "brand": "Brookside",
  "category": "Dairy",
  "quantity": "500 g",
  "ingredients_text": "Milk, Sugar, Vanilla Extract",
  "price": 200,
  "stock": 70
}
```

## OpenFoodFacts API Integration

The system integrates with the **OpenFoodFacts API** to retrieve product information.

The integration supports:

* Product lookup by barcode
* Product search by name
* Adding OpenFoodFacts products to the inventory

The application retrieves product information such as:

* Barcode
* Product name
* Brand
* Category
* Quantity

## Barcode Integration

Products can be retrieved from OpenFoodFacts using their barcode.

### Example Barcode

```text
3017620422003
```

This barcode was successfully used during testing to retrieve a **Nutella** product.

Example request:

```text
GET /product/barcode/3017620422003
```

The API retrieves the product information from OpenFoodFacts.

### Add a Product Using a Barcode

The system can also use a barcode to retrieve a product and add it directly to the inventory.

Example:

```text
POST /inventory/from-product/3017620422003
```

The user supplies inventory-specific information:

```json
{
  "price": 700,
  "stock": 400
}
```

The system combines the product information retrieved from OpenFoodFacts with the supplied price and stock and adds the product to the inventory.

Example:

```json
{
  "id": 5,
  "barcode": "3017620422003",
  "name": "Nutella",
  "brand": "Nutella, Ferrero",
  "category": "en:Confectionary based spreads, ...",
  "quantity": "400 g e",
  "price": 700,
  "stock": 400
}
```

## Product Name Search

Products can also be searched using their name.

Example:

```text
GET /product/name/Nutella
```

The system searches OpenFoodFacts and returns matching products.

The results can include:

* Product name
* Brand
* Category
* Quantity
* Barcode

## Command-Line Interface

The project includes an interactive CLI for managing inventory and interacting with the OpenFoodFacts API.

Start the CLI with:

```bash
python3 cli.py
```

The CLI provides the following options:

```text
1. View Inventory
2. View One Item
3. Add Item
4. Update Item
5. Delete Item
6. Find Product by Barcode
7. Find Products by Name
8. Add Product from OpenFoodFacts
9. Logout
```

### Rich CLI Interface

The CLI uses **Rich** to provide a more user-friendly and visually appealing terminal experience.

Rich is used for:

* Formatted inventory tables
* Panels for item and product information
* Success messages
* Error messages
* Styled menu presentation
* Improved terminal readability

### CLI Authentication

When the CLI starts, the administrator must log in before accessing the inventory menu.

Example:

```text
Username: admin
Password: admin123
```

The CLI uses a session to maintain the authenticated login.

Selecting **Option 9 — Logout** ends the current session and returns to the login screen.

### CLI Inventory Management

The CLI supports:

* Viewing all inventory items
* Viewing an individual item
* Adding an inventory item
* Updating an inventory item
* Deleting an inventory item

### CLI Barcode Search

**Option 6 — Find Product by Barcode**

The user enters a product barcode:

```text
Enter product barcode: 3017620422003
```

The CLI retrieves and displays product information from OpenFoodFacts.

### CLI Product Name Search

**Option 7 — Find Products by Name**

The user enters a product name:

```text
Enter product name: Nutella
```

The CLI displays matching products from OpenFoodFacts in a formatted table.

### CLI Add Product from OpenFoodFacts

**Option 8 — Add Product from OpenFoodFacts**

The user enters:

```text
Product barcode
Item price
Item stock
```

Example:

```text
Enter product barcode: 3017620422003

Enter item price: 700

Enter item stock: 400
```

The system retrieves the product information from OpenFoodFacts and adds it to the inventory.

The imported product can then be viewed through **Option 1 — View Inventory**.

## Error Handling

The application handles common errors including:

* Inventory item not found
* Product not found through OpenFoodFacts
* External API request failures
* Invalid price input
* Invalid stock input
* Invalid CLI menu choices
* Invalid numeric input
* Unauthorized access to protected routes

## Testing

The project uses **pytest** for automated testing.

Run all tests with:

```bash
python3 -m pytest
```

### Test Coverage

Tests cover:

* Flask API routes
* Inventory CRUD operations
* Authentication
* CLI functionality
* OpenFoodFacts integration
* External API responses
* Error handling

### Current Test Result

```text
13 passed
```

All automated tests are passing.

## Git and GitHub Workflow

The project was developed using **Git and GitHub**.

Feature branches were used to develop major parts of the application separately before merging completed work into the `main` branch.

The project also used **GitHub Pull Requests** to review and merge completed feature work.

The final `main` branch contains:

* Flask REST API
* Inventory CRUD operations
* Mock inventory data
* Session-based administrator authentication
* Login and logout
* OpenFoodFacts integration
* Barcode product lookup
* Product name search
* CLI functionality
* CLI authentication
* CLI error handling
* Rich CLI interface
* Automated tests

## Example OpenFoodFacts Workflow

A typical product import workflow is:

```text
User enters barcode
        ↓
CLI sends request to Flask API
        ↓
Flask requests product data
        ↓
OpenFoodFacts API
        ↓
Product information returned
        ↓
User provides price and stock
        ↓
Product added to inventory
        ↓
Product can be viewed in inventory
```

## Example Product Search Workflow

```text
User enters product name
        ↓
CLI sends search request
        ↓
OpenFoodFacts API
        ↓
Matching products returned
        ↓
Results displayed in a Rich table
```

## Author

**Maureen Mutua**
