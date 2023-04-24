from conn import DatabaseConnection
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ProductData:
    def __init__(self):
        """
        Inicializuje instanci třídy ProductData a naváže spojení s databází.
        """
        self.db_connection = DatabaseConnection().connect_to_database()

    def show_products_buttons(self, content_frame):
        """
        Zobrazuje tlačítka pro přidání a úpravu produktů v zadaném rámcovém widgetu.

        :param:
        content_frame (tkinter.Frame): Rámcový widget, ve kterém se mají zobrazit tlačítka.
        """
        for widget in content_frame.winfo_children():
            widget.destroy()
        products_button_frame = tk.Frame(content_frame, bg="#B0B0E0")

        add_product_button = ttk.Button(products_button_frame, text="Přidat produkt",
                                        command=self.add_product)
        add_product_button.pack(pady=(10, 0))

        edit_product_button = ttk.Button(products_button_frame, text="Upravit produkt",
                                         command=self.edit_product)
        edit_product_button.pack(pady=(10, 0))

        products_button_frame.pack(anchor='n', pady=10)
        products_button_frame.pack(anchor='n', pady=10)

    def get_all_products(self):
        """
        Získává všechny produkty z databáze.

        :return:
        list: Seznam všech produktů z databáze jako slovníky.
        """
        cursor = self.db_connection.cursor(dictionary=True)
        query = "SELECT * FROM produkt"
        cursor.execute(query)
        products = cursor.fetchall()
        cursor.close()
        return products

    def center_window(self, window, width, height):
        """
        Centruje zadané okno na střed obrazovky.

        :param:
        window (tkinter.Toplevel): Okno, které chceme vycentrovat.
        width (int): Šířka okna.
        height (int): Výška okna.
        """
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    def add_product(self):
        """
        Tato metoda vytváří okno pro přidání produktu a zpracovává vstup uživatele.
        """
        def submit():
            nazev = name_entry.get()
            popis = description_entry.get()
            cena = price_entry.get()

            if not nazev or not cena:
                messagebox.showerror("Chyba", "Název a cena jsou povinné položky.")
                return

            try:
                float(cena)
            except ValueError:
                messagebox.showerror("Chyba", "Cena musí být číslo.")
                return

            cursor = self.db_connection.cursor()
            query = "INSERT INTO produkt (nazev, popis, cena) VALUES (%s, %s, %s)"
            cursor.execute(query, (nazev, popis, cena))
            self.db_connection.commit()
            cursor.close()
            add_product_window.destroy()

        add_product_window = tk.Toplevel()
        add_product_window.title("Přidat produkt")
        add_product_window.configure(bg="#B0B0E0")
        self.center_window(add_product_window, 400, 300)

        name_label = tk.Label(add_product_window, text="Název:", bg="#B0B0E0")
        name_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
        name_entry = tk.Entry(add_product_window)
        name_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 0))

        description_label = tk.Label(add_product_window, text="Popis:", bg="#B0B0E0")
        description_label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))
        description_entry = tk.Entry(add_product_window)
        description_entry.grid(row=1, column=1, padx=(0, 10), pady=(10, 0))

        price_label = tk.Label(add_product_window, text="Cena:", bg="#B0B0E0")
        price_label.grid(row=2, column=0, padx=(10, 0), pady=(10, 0))
        price_entry = tk.Entry(add_product_window)
        price_entry.grid(row=2, column=1, padx=(0, 10), pady=(10, 0))

        submit_button = ttk.Button(add_product_window, text="Přidat", command=submit)
        submit_button.grid(row=3, columnspan=2, pady=(10, 0))


    def edit_product(self):
        """
        Tato metoda vytváří okno pro úpravu produktu a zpracovává vstup uživatele.
        """
        def submit():
            product_id = id_entry.get()
            nazev = name_entry.get()
            popis = description_entry.get()
            cena = price_entry.get()

            if not product_id or not nazev or not cena:
                messagebox.showerror("Chyba", "ID, název a cena jsou povinné položky.")
                return

            try:
                int(product_id)
                float(cena)
            except ValueError:
                messagebox.showerror("Chyba", "ID musí být celé číslo a cena musí být číslo.")
                return

            cursor = self.db_connection.cursor()
            query = "UPDATE produkt SET nazev = %s, popis = %s, cena = %s WHERE id = %s"
            cursor.execute(query, (nazev, popis, cena, product_id))
            self.db_connection.commit()
            cursor.close()
            edit_product_window.destroy()

        edit_product_window = tk.Toplevel()
        edit_product_window.title("Upravit produkt")
        edit_product_window.configure(bg="#B0B0E0")
        self.center_window(edit_product_window, 400, 300)
        id_label = tk.Label(edit_product_window, text="ID:", bg="#B0B0E0")
        id_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
        id_entry = tk.Entry(edit_product_window)
        id_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 0))

        name_label = tk.Label(edit_product_window, text="Název:", bg="#B0B0E0")
        name_label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0))
        name_entry = tk.Entry(edit_product_window)
        name_entry.grid(row=1, column=1, padx=(0, 10), pady=(10, 0))

        description_label = tk.Label(edit_product_window, text="Popis:", bg="#B0B0E0")
        description_label.grid(row=2, column=0, padx=(10, 0), pady=(10, 0))
        description_entry = tk.Entry(edit_product_window)
        description_entry.grid(row=2, column=1, padx=(0, 10), pady=(10, 0))

        price_label = tk.Label(edit_product_window, text="Cena:", bg="#B0B0E0")
        price_label.grid(row=3, column=0, padx=(10, 0), pady=(10, 0))
        price_entry = tk.Entry(edit_product_window)
        price_entry.grid(row=3, column=1, padx=(0, 10), pady=(10, 0))

        submit_button = ttk.Button(edit_product_window, text="Upravit", command=submit)
        submit_button.grid(row=4, columnspan=2, pady=(10, 0))