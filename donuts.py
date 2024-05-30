# breads.py

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import csv
from PIL import Image, ImageTk
import os
import button  # Import button module for navigation to pemilihan

bg_color = "#FFEFE8"
text_color = "#FF7A8A"
button_color = "#FFADA1"
menu_color = "#FFD9CC"
font_title = ("Baskerville Old Face", 30, "bold")
font_subtitle = ("Arial", 20, "bold")
font_text = ("Arial", 12)

selected_count_label = None
total_cost_label = None
selected_products = []
total_cost = 0

def update_display():
    global selected_count_label, total_cost_label
    selected_count_label.configure(text=f"Jumlah produk yang dipilih: {len(selected_products)}")
    total_cost_label.configure(text=f"Rp {total_cost}")

def load_cart_from_csv():
    global selected_products, total_cost
    cart_path = 'database/cart.csv'
    selected_products = []
    total_cost = 0

    # Check if cart.csv exists
    if not os.path.exists(cart_path):
        # Create the file with a header if it doesn't exist
        with open(cart_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'price'])
    
    # Load cart if it exists and is not empty
    if os.stat(cart_path).st_size > 0:
        with open(cart_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                selected_products.append({
                    'name': row[0],
                    'price': int(row[1])
                })
                total_cost += int(row[1])
    else:
        # If cart.csv is empty, set default values
        selected_products = []
        total_cost = 0

def save_cart_to_csv():
    with open('database/cart.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'price'])  # Write header
        for product in selected_products:
            writer.writerow([product['name'], product['price']])

def buat_donuts_page(app):

    load_cart_from_csv()
    # update_display()

    def load_products(file_path):
        products = []
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                products.append({
                    'name': row['name'],
                    'image': os.path.join('images', row['image']),
                    'price': int(row['price'])
                })
        return products

    def select_product(product):
        global selected_products, total_cost
        selected_products.append(product)
        total_cost += product['price']
        update_display()

    # def go_back():
    #     save_cart_to_csv()
    #     for widget in app.winfo_children():
    #         widget.destroy()
    #     os.system('python homepage.py')

    def go_back():
        save_cart_to_csv()  # Save cart to CSV before going back
        app.destroy()
        os.system('python homepage.py')

    def display_menu(csv_file):

        load_cart_from_csv()

        products = load_products(os.path.join('database', csv_file))
        
        product_frame = ctk.CTkFrame(app)
        product_frame.grid(row=1, column=0, columnspan=3, pady=18, padx=12, sticky="nsew")
        
        for index, product in enumerate(products):
            row = index // 5
            column = index % 5

            product_card = ctk.CTkFrame(product_frame)
            product_card.grid(row=row, column=column, padx=18, pady=12)

            image = Image.open(product['image'])
            image = image.resize((150, 150), Image.LANCZOS) ## kalo error ganti jadi Image.Resampling.LANCZOS
            img = ImageTk.PhotoImage(image)

            img_label = ctk.CTkLabel(product_card, image=img, text="")
            img_label.image = img
            img_label.grid(row=0, column=0, pady=(0, 10))

            button = ctk.CTkButton(product_card, text=f"Rp {product['price']}", command=lambda p=product: select_product(p), fg_color=button_color)
            button.grid(row=1, column=0)

    header_frame = ctk.CTkFrame(app)
    header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

    back_button = ctk.CTkButton(header_frame, text="Back", command=go_back, fg_color=button_color)
    back_button.grid(row=0, column=0, padx=10, pady=10)

    title_label = ctk.CTkLabel(header_frame, text="DONUTS", justify="center", font=font_title)
    title_label.grid(row=0, column=1, pady=15)

    display_menu('donuts.csv')

    bottom_frame = ctk.CTkFrame(app)
    bottom_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

    global selected_count_label, total_cost_label
    selected_count_label = ctk.CTkLabel(bottom_frame, text="Jumlah produk yang dipilih: 0")
    selected_count_label.grid(row=0, column=0, padx=20, sticky="w")

    total_cost_label = ctk.CTkLabel(bottom_frame, text="Rp 0")
    total_cost_label.grid(row=0, column=2, padx=20, sticky="e")

    action_frame = ctk.CTkFrame(bottom_frame)
    action_frame.grid(row=0, column=1, pady=10)

    takeaway_button = ctk.CTkButton(action_frame, text="TAKEAWAY", fg_color=button_color, command=lambda: button.menuju_ke_pemilihan(app, "TAKEAWAY", selected_products))
    takeaway_button.grid(row=0, column=0, padx=5, pady=5)
    delivery_button = ctk.CTkButton(action_frame, text="DELIVERY", fg_color=button_color, command=lambda: button.menuju_ke_pemilihan(app, "DELIVERY", selected_products))
    delivery_button.grid(row=0, column=1, padx=5, pady=5)
    dinein_button = ctk.CTkButton(action_frame, text="DINE IN", fg_color=button_color, command=lambda: button.menuju_ke_pemilihan(app, "DINE IN", selected_products))
    dinein_button.grid(row=0, column=2, padx=5, pady=5)

     # Initialize selected_count_label and total_cost_label
    update_display()

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Cakeshop - Donuts")
    app.geometry("900x500")
    buat_donuts_page(app)
    app.mainloop()
