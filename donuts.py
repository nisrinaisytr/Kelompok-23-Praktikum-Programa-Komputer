import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import csv
from PIL import Image, ImageTk
import os

bg_color = "#FFEFE8"
text_color = "#FF7A8A"
button_color = "#FFADA1"
menu_color = "#FFD9CC"
font_title = ("Arial", 30, "bold")
font_subtitle = ("Arial", 20, "bold")
font_text = ("Arial", 12)

def buat_breads_page(app):
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

    def update_display():
        global selected_count_label, total_cost_label
        selected_count_label.configure(text=f"Jumlah produk yang dipilih: {len(selected_products)}")
        total_cost_label.configure(text=f"Rp {total_cost}")

    def go_back():
        for widget in app.winfo_children():
            widget.destroy()
        os.system('python homepage.py')

    def display_menu(csv_file):
        products = load_products(os.path.join('database', csv_file))
        
        product_frame = ctk.CTkFrame(app)
        product_frame.grid(row=1, column=0, columnspan=3, pady=18, padx=12, sticky="nsew")
        
        for index, product in enumerate(products):
            row = index // 5
            column = index % 5

            product_card = ctk.CTkFrame(product_frame)
            product_card.grid(row=row, column=column, padx=18, pady=12)

            image = Image.open(product['image'])
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(image)

            img_label = ctk.CTkLabel(product_card, image=img, text="")
            img_label.image = img
            img_label.grid(row=0, column=0, pady=(0, 10))

            button = ctk.CTkButton(product_card, text=f"Rp {product['price']}", command=lambda p=product: select_product(p), fg_color=button_color)
            button.grid(row=1, column=0)

    global selected_products, total_cost
    selected_products = []
    total_cost = 0

    header_frame = ctk.CTkFrame(app)
    header_frame.grid(row=0, column=0, sticky="ew")

    back_button = ctk.CTkButton(header_frame, text="Back", command=go_back, fg_color=button_color)
    back_button.grid(row=0, column=0, padx=10, pady=10)

    title_label = ctk.CTkLabel(header_frame, text="DONUTS", justify="center", font=font_title)
    title_label.grid(row=0, column=1, pady=15)

    display_menu('donuts.csv')

    bottom_frame = ctk.CTkFrame(app)
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)

    selected_count_label = ctk.CTkLabel(bottom_frame, text="Jumlah produk yang dipilih: 0")
    selected_count_label.grid(row=0, column=0, padx=20)

    total_cost_label = ctk.CTkLabel(bottom_frame, text="Rp 0")
    total_cost_label.grid(row=0, column=1, padx=20)

    action_frame = ctk.CTkFrame(bottom_frame)
    action_frame.grid(row=0, column=2, pady=10)

    takeaway_button = ctk.CTkButton(action_frame, text="TAKEAWAY", fg_color=button_color, command=lambda: messagebox.showinfo("Takeaway", "Takeaway option selected"))
    takeaway_button.grid(row=0, column=0, padx=5)

    delivery_button = ctk.CTkButton(action_frame, text="DELIVERY", fg_color=button_color, command=lambda: messagebox.showinfo("Delivery", "Delivery option selected"))
    delivery_button.grid(row=0, column=1, padx=5)

    dinein_button = ctk.CTkButton(action_frame, text="DINE IN", fg_color=button_color, command=lambda: messagebox.showinfo("Dine In", "Dine In option selected"))
    dinein_button.grid(row=0, column=2, padx=5)

    app.mainloop()

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Cakeshop - Donuts")
    app.geometry("900x500")
    buat_breads_page(app)
    app.mainloop()
