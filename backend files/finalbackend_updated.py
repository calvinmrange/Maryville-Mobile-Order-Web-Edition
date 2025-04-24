import json
import flask
from flask_cors import CORS
app = flask.Flask(__name__)  
CORS(app)

from flask import Flask, request, jsonify
CORS(app, resources={r"/pastaorder": {"origins": "http://127.0.0.1:5500"}})
from flask_cors import cross_origin


import os
import os
import sqlite3
def MR_DB():
    connection = sqlite3.connect('MRDining.db', check_same_thread=False)

    cursor = connection.cursor()

    # Restaurants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Restaurants (
            restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Location TEXT NOT NULL
        )
    ''')

    # Menu table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Menu (
            Item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Item_Name TEXT NOT NULL,
            Description TEXT NOT NULL,
            Price REAL NOT NULL,
            restaurant_id INTEGER,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id) ON DELETE CASCADE
        )
    ''')

    # Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Student_Name TEXT NULL,
            Price REAL NULL,
            restaurant_id INTEGER,
            Menu_Item_Details TEXT,  -- Store JSON or ordered items' details as text
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id) ON DELETE CASCADE

        )
    ''')

    # Customization Types (E.g., "Size", "Toppings", "Protein")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customizations (
            customization_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Item_ID INTEGER NOT NULL,
            Customization_Type TEXT NOT NULL,  
            FOREIGN KEY (Item_ID) REFERENCES Menu(Item_ID) ON DELETE CASCADE
        )
    ''')

    # Customization Options (Holds Actual Choices)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customization_Options (
            option_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customization_id INTEGER NOT NULL,
            Option_Name TEXT NOT NULL,  
            FOREIGN KEY (customization_id) REFERENCES Customizations(customization_id) ON DELETE CASCADE
        )
    ''')

    # Order Customizations (Tracks Selected Customizations for Each Order)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Order_Customizations (
            order_customization_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Order_ID INTEGER NOT NULL,
            customization_id INTEGER NOT NULL,
            option_id INTEGER NOT NULL,
            FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID) ON DELETE CASCADE,
            FOREIGN KEY (customization_id) REFERENCES Customizations(customization_id) ON DELETE CASCADE,
            FOREIGN KEY (option_id) REFERENCES Customization_Options(option_id) ON DELETE CASCADE
        )
    ''')

    # Allergies Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Allergies (
            allergy_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Allergy_Name TEXT NOT NULL UNIQUE
        )
    ''')

    # Item-Allergy Mapping Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item_Allergies (
            item_allergy_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Item_ID INTEGER NOT NULL,
            allergy_id INTEGER NOT NULL,
            FOREIGN KEY (Item_ID) REFERENCES Menu(Item_ID) ON DELETE CASCADE,
            FOREIGN KEY (allergy_id) REFERENCES Allergies(allergy_id) ON DELETE CASCADE
        )
    ''')

    # Check if Restaurants table is empty before inserting
    cursor.execute("SELECT COUNT(*) FROM Restaurants")
    if cursor.fetchone()[0] == 0:
        Restaurant_Data = [
            ("Mozzie's Handcrafted Pizza", "Gander Dining Hall"),
            ("Urban Hen", "Gander Dining Hall"),
            ("Sushi by Faith", "Gander Dining Hall"),
            ("Rice It Up", "Gander Dining Hall"),
            ("Epic Eats", "Gander Dining Hall"),
            ("Louie's", "DUC"),
            ("Starbucks", "Library")
        ]
        cursor.executemany("INSERT INTO Restaurants (Name, Location) VALUES (?, ?)", Restaurant_Data)
        connection.commit()

    cursor.execute("SELECT restaurant_id FROM Restaurants WHERE Name = ?", ("Urban Hen",))
    urban_hen_id = cursor.fetchone()

    if urban_hen_id:
        urban_hen_id = urban_hen_id[0]

        # Insert menu items if Urban Hen's menu is empty
        cursor.execute("SELECT COUNT(*) FROM Menu WHERE restaurant_id = ?", (urban_hen_id,))
        if cursor.fetchone()[0] == 0:
            menu_items = [
                ("Chicken Strips", "Crispy, golden-brown chicken tenders, perfectly seasoned and served with a side of your favorite dipping sauce.", 6.25, urban_hen_id),
                ("Grilled Cheese", "A warm, toasted sandwich filled with gooey melted cheese, offering the perfect balance of crispy and creamy.", 4.50, urban_hen_id),
                ("Smash Burger", "Juicy, hand-pressed beef patty, smashed to perfection and topped with crispy chicken tenders and a sweet honey mustard sauce.", 7.90, urban_hen_id),
                ("Veggie Burger", "A hearty, plant-based patty made with black beans, fresh avocado, and a kick of chipotle mayo, served on a toasted bun.", 8.55, urban_hen_id),
                ("Cheese Burger", "A hearty, plant-based patty made with black beans, fresh avocado, and a kick of chipotle mayo, served on a toasted bun.", 8.55, urban_hen_id),
            ]
            cursor.executemany("INSERT INTO Menu (Item_Name, Description, Price, restaurant_id) VALUES (?, ?, ?, ?)", menu_items)
            connection.commit()

    cursor.execute("SELECT restaurant_id FROM Restaurants WHERE Name = ?", ("Epic Eats",))
    epic_eats_id = cursor.fetchone()

    if epic_eats_id:
        epic_eats_id = epic_eats_id[0]

        # Insert menu items if Epic Eats menu is empty
        cursor.execute("SELECT COUNT(*) FROM Menu WHERE restaurant_id = ?", (epic_eats_id,))
        if cursor.fetchone()[0] == 0:
            menu_items = [
                ("2 Tacos", "Two soft tortillas filled with perfectly seasoned crispy chicken tenders, topped with fresh veggies and served with a side of your choice of dipping sauce.", 5.95, epic_eats_id),
                ("Burrito", "A hearty burrito wrapped in a warm tortilla, filled with seasoned rice, beans, and gooey melted cheese, all topped with your choice of protein and a zesty salsa.", 9.85, epic_eats_id),
                ("Quesadilla", "A crispy tortilla filled with a melty blend of cheese and your choice of protein, grilled to perfection and served with a side of guacamole and sour cream.", 9.55, epic_eats_id),
            ]
            cursor.executemany("INSERT INTO Menu (Item_Name, Description, Price, restaurant_id) VALUES (?, ?, ?, ?)", menu_items)
            connection.commit()

    # Check if Louie's restaurant ID exists
    cursor.execute("SELECT restaurant_id FROM Restaurants WHERE Name = ?", ("Louie's",))
    louies_id = cursor.fetchone()

    if louies_id:
        louies_id = louies_id[0]

    # Insert menu items if Louie's menu is empty
        cursor.execute("SELECT COUNT(*) FROM Menu WHERE restaurant_id = ?", (louies_id,))
        if cursor.fetchone()[0] == 0:
            menu_items = [
                ("Toasted Ravioli (6)", "Crispy, golden-brown breaded ravioli stuffed with savory beef, served with a side of marinara sauce for dipping. A perfect balance of crunchy and cheesy goodness!", 6.65, louies_id),
                ("Cheese Sticks (6)", "Warm, gooey mozzarella cheese sticks coated in a light, crispy breading. Served with a zesty marinara dipping sauce to complement the melt-in-your-mouth experience.", 6.65, louies_id),
                ("Grilled Cheese", "A classic comfort dish with perfectly toasted bread enclosing a melted layer of cheddar cheese. Served with a side of crispy fries and a choice of dipping sauce for an extra burst of flavor.", 4.50, louies_id),
            ]
            cursor.executemany("INSERT INTO Menu (Item_Name, Description, Price, restaurant_id) VALUES (?, ?, ?, ?)", menu_items)
            connection.commit()
    cursor.execute("SELECT restaurant_id FROM Restaurants WHERE Name = ?", ("Starbucks",))
    starbucks_id = cursor.fetchone()

    if starbucks_id:
        starbucks_id = starbucks_id[0]

    # Insert menu items if Starbucks menu is empty
        cursor.execute("SELECT COUNT(*) FROM Menu WHERE restaurant_id = ?", (starbucks_id,))
        if cursor.fetchone()[0] == 0:
            menu_items = [
                ("Cappucino", "A rich and aromatic espresso topped with a frothy layer of steamed milk and dusted with a hint of cocoa. A classic Italian favorite with a smooth, velvety texture.", 4.85, starbucks_id),
                ("Vanilla Bean Creme Frappucino", "A creamy and indulgent blend of vanilla bean, ice, and milk, topped with whipped cream for a sweet and refreshing treat. Perfect for a cool, creamy pick-me-up!", 5.75, starbucks_id),
                ("Espresso", "A strong, concentrated coffee shot made from finely ground beans, delivering a bold and full-bodied flavor. Ideal for those who crave an intense coffee experience.", 2.95, starbucks_id),
                ("Caffe Americano", "A simple yet bold coffee made by diluting rich espresso with hot water, creating a smooth, robust flavor with a touch of strength. A perfect option for coffee purists.", 5.35, starbucks_id),
            ]
            cursor.executemany("INSERT INTO Menu (Item_Name, Description, Price, restaurant_id) VALUES (?, ?, ?, ?)", menu_items)
            connection.commit()

    # Mozzies Pizza Restaurant
    cursor.execute("SELECT restaurant_id FROM Restaurants WHERE Name = ?", ("Mozzie's Handcrafted Pizza",))
    mozzie_id = cursor.fetchone()

    if mozzie_id:
        mozzie_id = mozzie_id[0]

        # Insert menu items if Mozzie's menu is empty
        cursor.execute("SELECT COUNT(*) FROM Menu WHERE restaurant_id = ?", (mozzie_id,))
        if cursor.fetchone()[0] == 0:
            menu_items = [
                ("Build Your Own Pasta", "Customize your own pasta dish with a variety of sauces and toppings.", 11.25, mozzie_id),
                ("Build Your Own Pizza", "Create your perfect pizza with fresh ingredients.", 9.45, mozzie_id),
                ("Build Your Own Gluten-Free Pizza", "A gluten-free option with the same great taste.", 11.45, mozzie_id),
                ("Mac & Cheese", "Classic cheesy goodness made fresh.", 11.25, mozzie_id),
            ]
            cursor.executemany("INSERT INTO Menu (Item_Name, Description, Price, restaurant_id) VALUES (?, ?, ?, ?)", menu_items)
            connection.commit()

        # Get Item ID for Pasta
        cursor.execute("SELECT Item_ID FROM Menu WHERE Item_Name = 'Build Your Own Pasta'")
        pasta_id = cursor.fetchone()

        if pasta_id:
            pasta_id = pasta_id[0]

            # Insert customization types
            cursor.execute("SELECT COUNT(*) FROM Customizations WHERE Item_ID = ?", (pasta_id,))
            if cursor.fetchone()[0] == 0:
                customization_types = ["Portion Size", "Sauce", "Toppings", "Garlic Bread Option", "Pasta Type"]
                for ctype in customization_types:
                    cursor.execute("INSERT INTO Customizations (Item_ID, Customization_Type) VALUES (?, ?)", (pasta_id, ctype))
                    connection.commit()

            # Fetch customization IDs and types
            cursor.execute("SELECT customization_id, Customization_Type FROM Customizations WHERE Item_ID = ?", (pasta_id,))
            pasta_customizations = cursor.fetchall()

            # Define customization options
            customization_options = {
                "Portion Size": ["Small", "Large"],
                "Sauce": ["No Sauce", "Pesto", "Alfredo Sauce", "Red Sauce", "Rose Sauce"],
                "Toppings": [
                    "Grilled Chicken", "Mushrooms", "Spinach", "Extra Cheese",
                    "Artichoke Hearts", "Banana Peppers", "Black Olives",
                    "Chopped Garlic", "No Toppings", "Onions", "Tomatoes", "Pineapple"
                ],
                "Garlic Bread Option": ["None", "Regular Garlic Bread"],
                "Pasta Type": ["Chefs Choice Pasta"]
            }

            # Insert options for each customization type
            for customization_id, ctype in pasta_customizations:
                if ctype in customization_options:
                    cursor.executemany(
                        "INSERT INTO Customization_Options (customization_id, Option_Name) VALUES (?, ?)",
                        [(customization_id, option) for option in customization_options[ctype]]
                    )
                    connection.commit()

            # Insert allergies only if the table is empty
            cursor.execute("SELECT COUNT(*) FROM Allergies")
            if cursor.fetchone()[0] == 0:
                allergies = [
                    ("No Allergies",),
                    ("Dairy Allergy",),
                    ("Egg Allergy",),
                    ("Fish Allergy",),
                    ("Gluten Allergy",),
                    ("Peanut Allergy",),
                    ("Sesame Allergy",),
                    ("Shellfish Allergy",),
                    ("Soy Allergy",),
                    ("Tree Nut Allergy",),
                    ("Wheat Allergy",)
                ]
                cursor.executemany("INSERT INTO Allergies (Allergy_Name) VALUES (?)", allergies)
                connection.commit()

            # Map all allergies to Pasta (for demo purposes)
            cursor.execute("SELECT allergy_id FROM Allergies")
            allergy_ids = cursor.fetchall()
            cursor.executemany(
                "INSERT INTO Item_Allergies (Item_ID, allergy_id) VALUES (?, ?)",
                [(pasta_id, allergy_id[0]) for allergy_id in allergy_ids]
            )
            connection.commit()

    connection.close()

def print_database():
    conn = sqlite3.connect("MRDining.db")
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\nDatabase Tables:")
    for table in tables:
        print(f"\nTable: {table[0]}")
        cursor.execute(f"SELECT * FROM {table[0]}")
        rows = cursor.fetchall()
        
        # Print column names
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = [column[1] for column in cursor.fetchall()]
        print(" | ".join(columns))

        # Print rows
        for row in rows:
            print(row)

    conn.close()
MR_DB()  # Create tables and insert initial data
print_database()  # Print database contents



app = Flask(__name__)


@app.route('/pastaorder', methods=['POST'])
@cross_origin(origin='127.0.0.1', headers=['Content-Type', 'Authorization'])
def place_order():
    # Get the JSON data from the frontend
    order_data = request.get_json()

    #Log received data
    print(f"Received order data: {order_data}")

    # Extract values from the request data
    restaurant_id = order_data.get('restaurant_id')
    menu_item = order_data.get('menu_item')
    ingredients = order_data.get('ingredients', {})
    prices = price_data.get('Prices')

    # Error Handlers
    if not restaurant_id:
        return jsonify({'error': 'Restaurant ID is required'}), 400
    if not menu_item:
        return jsonify({'error': 'Menu item is required'}), 400
    if not ingredients.get('portion_size') or not ingredients.get('sauce') or not ingredients.get('toppings'):
        return jsonify({'error': 'All ingredients (portion_size, sauce, toppings) must be provided'}), 400

    # Initialize the database connection
    connection = sqlite3.connect('MRDining.db')
    cursor = connection.cursor()

    # Check if the restaurant exists
    cursor.execute('SELECT * FROM Restaurants WHERE restaurant_id = ?', (restaurant_id,))
    restaurant = cursor.fetchone()
    if not restaurant:
        connection.close()
        return jsonify({'error': 'Restaurant not found'}), 404

    # Check if the menu item exists
    cursor.execute('SELECT * FROM Menu WHERE Item_ID = ? AND restaurant_id = ?', (menu_item, restaurant_id))
    menu_item_entry = cursor.fetchone()
    if not menu_item_entry:
        connection.close()
        return jsonify({'error': 'Menu item not found in the selected restaurant'}), 404

    # Insert the order into the Orders table
    cursor.execute('INSERT INTO Orders (restaurant_id) VALUES (?)', (restaurant_id,))
    order_id = cursor.lastrowid  # Get the ID of the newly created order
    connection.commit()

    # Handle customizations for the order
    toppings = ingredients.get('toppings', [])
    for topping in toppings:
        # Query to get the customization_id for Topping
        cursor.execute('SELECT customization_id FROM Customizations WHERE customization_type = "Topping"')
        customization = cursor.fetchone()
        if customization:
            customization_id = customization[0]
        else:
            # Handle error if customization not found
            continue
        
        # Query to get the option_id for the specific topping 
        cursor.execute('SELECT option_id FROM Customization_Options WHERE option_name = ?', (topping,))
        option = cursor.fetchone()
        if option:
            option_id = option[0]
        else:
            continue
        
        cursor.execute('''INSERT INTO Order_Customizations (Order_ID, customization_id, option_id)
                          VALUES (?, ?, ?)''', (order_id, customization_id, option_id))
        connection.commit()

    cursor.execute('UPDATE Orders SET Menu_Item_Details = ? WHERE Order_ID = ?', (menu_item, order_id))
    connection.commit()

    # Close the database connection
    connection.close()

    # Return a success response 
    return jsonify({'status': 'Order placed successfully'}), 201






# Main entry point to run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)  
