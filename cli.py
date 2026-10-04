import requests
import shutil

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

#Session
client = requests.Session()

#Set console width
console = Console(width=max(shutil.get_terminal_size().columns, 100))

BASE_URL = "http://127.0.0.1:5000"

#Admin login
def login():
    while True:
        username = input("Username: ")
        password = input("Password: ")

        response = client.post(f"{BASE_URL}/login",json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            console.print(
                Panel("Login successful! Welcome, Admin.")
            )
            return True
        
        console.print(
            Panel("Invalid username or password. Try again.")
        )

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            console.print("[bold red] Invalid input. Please enter a number.[/bold red]")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            console.print(
                "[bold red] Invalid input. Please enter a whole number.[/bold red]"
            )

#View all inventory
def view_inventory():
    response = client.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        items = response.json()

        table = Table(title=" Current Inventory", expand=False)

        table.add_column("ID", style="cyan", justify="center",width=4)
        table.add_column("Product", style="green",max_width=18)
        table.add_column("Category", style="yellow",max_width=12)
        table.add_column("Price", style="blue",width=8)
        table.add_column("Stock", style="magenta", justify="center", width=8)

        for item in items:
            table.add_row(
                str(item["id"]),
                str(item["name"]),
                str(item.get("category", "")),
                str(item.get("price", "")),
                str(item.get("stock", "")),
            )

        console.print(table)

    else:
        console.print(
            f"[bold red] Error: {response.status_code}[/bold red]"
        )

#View one inventory item
def view_item(item_id):
    response = client.get(f"{BASE_URL}/inventory/{item_id}")

    if response.status_code == 200:
        item = response.json()

        console.print(
            Panel(
                f"[bold]Product:[/bold] {item['name']}\n"
                f"[bold]Category:[/bold] {item.get('category', '')}\n"
                f"[bold]Price:[/bold] {item.get('price', '')}\n"
                f"[bold]Stock:[/bold] {item.get('stock', '')}",
                title=f" Item #{item['id']}",
                border_style="cyan",
            )
        )

    else:
        console.print(
            f"[bold red] Error: {response.status_code}[/bold red]"
        )

#Add inventory item
def add_item():
    name = input("Enter item name: ")
    category = input("Enter item category: ")
    price = get_float("Enter item price: ")
    stock = get_int("Enter item stock: ")

    data = {
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
    }

    response = client.post(f"{BASE_URL}/inventory", json=data)

    if response.status_code == 201:
        item = response.json()

        console.print(
            Panel(
                f"[bold green]✓ Item added successfully![/bold green]\n\n"
                f"Product: {item['name']}\n"
                f"Category: {item['category']}\n"
                f"Price: {item['price']}\n"
                f"Stock: {item['stock']}",
                title=" New Inventory Item",
                border_style="green",
            )
        )

    else:
        console.print(
            f"[bold red] Error: {response.status_code}[/bold red]"
        )

#Update inventory item
def update_item(item_id):
    price = input("Enter new price (leave blank to keep current): ")
    stock = input("Enter new stock (leave blank to keep current): ")

    data = {}

    if price:
        try:
            data["price"] = float(price)
        except ValueError:
            console.print(
                "[bold red] Invalid price. Please enter a number.[/bold red]"
            )
            return

    if stock:
        try:
            data["stock"] = int(stock)
        except ValueError:
            console.print(
                "[bold red] Invalid stock. Please enter a whole number.[/bold red]"
            )
            return

    response = client.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data,
    )

    if response.status_code == 200:
        item = response.json()

        console.print(
            Panel(
                f"[bold green]✓ Item updated successfully![/bold green]\n\n"
                f"Product: {item['name']}\n"
                f"Price: {item['price']}\n"
                f"Stock: {item['stock']}",
                title=f" Updated Item #{item['id']}",
                border_style="yellow",
            )
        )

    else:
        console.print(
            f"[bold red] Error: {response.status_code}[/bold red]"
        )

#Delete inventory item
def delete_item(item_id):
    response = client.delete(f"{BASE_URL}/inventory/{item_id}")

    if response.status_code == 200:
        console.print(
            Panel(
                "[bold green]✓ Item deleted successfully![/bold green]",
                title=" Inventory",
                border_style="red",
            )
        )

    else:
        console.print(
            f"[bold red] Error: {response.status_code}[/bold red]"
        )

#Search by barcode
def find_product_by_barcode(barcode):
    response = client.get(
        f"{BASE_URL}/product/barcode/{barcode}"
    )

    if response.status_code == 200:
        product = response.json()

        if not product:
            console.print("[bold red]Product not found.[/bold red]")
            return

        console.print(
            Panel(
                f"[bold]Name:[/bold] {product.get('name', '')}\n"
                f"[bold]Brand:[/bold] {product.get('brand', '')}\n"
                f"[bold]Category:[/bold] {product.get('category', '')}\n"
                f"[bold]Quantity:[/bold] {product.get('quantity', '')}\n"
                f"[bold]Barcode:[/bold] {product.get('barcode', '')}",
                title=" OpenFoodFacts Product",
                border_style="blue",
            )
        )

    else:
        console.print(
            f"[bold red] Error: {response.status_code}[/bold red]"
        )

#Search by name
def find_products_by_name(name):
    response = client.get(
        f"{BASE_URL}/product/name/{name}"
    )

    if response.status_code == 200:
        products = response.json()

        if not products:
            console.print(
                "[bold yellow] No products found.[/bold yellow]"
            )
            return

        table = Table(title=f" Products matching '{name}'")

        table.add_column("Name", style="green")
        table.add_column("Brand", style="cyan")
        table.add_column("Category", style="yellow")
        table.add_column("Quantity", style="magenta")

        for product in products:
            table.add_row(
                str(product.get("name", "")),
                str(product.get("brand", "")),
                str(product.get("category", "")),
                str(product.get("quantity", "")),
            )

        console.print(table)

    else:
        console.print(
            f"[bold red] Error: {response.status_code}[/bold red]"
        )

#Add API product
def add_product_from_api():
    barcode = input("Enter product barcode: ")
    price = get_float("Enter item price: ")
    stock = get_int("Enter item stock: ")

    data = {
        "price": price,
        "stock": stock,
    }

    response = client.post(
        f"{BASE_URL}/inventory/from-product/{barcode}",
        json=data,
    )

    if response.status_code == 201:
        item = response.json()

        console.print(
            Panel(
                f"[bold green]✓ Product added to inventory![/bold green]\n\n"
                f"Name: {item['name']}\n"
                f"Brand: {item['brand']}\n"
                f"Category: {item['category']}\n"
                f"Price: {item['price']}\n"
                f"Stock: {item['stock']}",
                title=" OpenFoodFacts → Inventory",
                border_style="green",
            )
        )

    else:
        console.print(
            f"[bold red] Error: {response.status_code}[/bold red]"
        )

#Main Menu
def menu():
    while True:
        console.print(
            Panel.fit(
                " INVENTORY MANAGEMENT SYSTEM[bold cyan] ",
                title="Welcome",
                border_style="cyan",
            )
        )

        console.print("[bold cyan] 1.[/bold cyan] View Inventory")
        console.print("[bold cyan] 2.[/bold cyan] View One Item")
        console.print("[bold green] 3.[/bold green] Add Item")
        console.print("[bold yellow] 4.[/bold yellow] Update Item")
        console.print("[bold red] 5.[/bold red] Delete Item")
        console.print("[bold magenta] 6.[/bold magenta] Find Product by Barcode")
        console.print("[bold magenta] 7.[/bold magenta] Find Products by Name")
        console.print("[bold blue] 8.[/bold blue] Add Product from OpenFoodFacts")
        console.print("[bold white] 9.[/bold white] Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            item_id = get_int("Enter item ID to view: ")
            view_item(item_id)

        elif choice == "3":
            add_item()

        elif choice == "4":
            item_id = get_int("Enter item ID to update: ")
            update_item(item_id)

        elif choice == "5":
            item_id = get_int("Enter item ID to delete: ")
            delete_item(item_id)

        elif choice == "6":
            barcode = input("Enter product barcode: ")
            find_product_by_barcode(barcode)

        elif choice == "7":
            name = input("Enter product name: ")
            find_products_by_name(name)

        elif choice == "8":
            add_product_from_api()

        elif choice == "9":
            client.post(f"{BASE_URL}/logout")

            console.print(
                Panel.fit(
                    " Logged out successfully",
                    border_style="cyan",
                )
            )
            return

        else:
            console.print(
                "[bold red] Invalid choice. Please try again.[/bold red]"
            )

#Start CLI
if __name__ == "__main__":
    while True:
        login()
        menu()
    