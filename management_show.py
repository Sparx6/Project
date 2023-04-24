import tkinter as tk
from tkinter import ttk
from dataoperation import DataOperations
class ManagementShow:
    def __init__(self, content_frame, db_connection, employee_dict):
        """
        Inicializace třídy pro zobrazení různých typů dat.

        :param:

        content_frame : tk.Frame
         Frame pro obsah třídy.
        db_connection : objekt
         Objekt připojení k databázi.
        employee_dict : dict
         Slovník obsahující informace o zaměstnanci.
        """
        self.content_frame = content_frame
        self.db_connection = db_connection
        self.employee_dict = employee_dict
        self.data_operations = DataOperations()


    def clear_content_frame(self):
        """
        Metoda pro smazání obsahu frame.
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_products(self):
        """
        Metoda pro zobrazení všech produktů z databáze.
        """
        self.clear_content_frame()
        canvas = tk.Canvas(self.content_frame, bg="#B0B0E0", bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#B0B0E0")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        products = self.db_connection.get_all_products()

        for product in products:
            product_label = tk.Label(self.scrollable_frame, text=f"ID: {product['id']}\n"
                                                                 f"Název: {product['nazev']}\n"
                                                                 f"Popis: {product['popis']}\n"
                                                                 f"Cena: {product['cena']} Kč",
                                     font=("Helvetica", 14), bg="#B0B0E0", width=70)
            product_label.pack(padx=20, pady=20)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_stock_status(self):
        """
        Metoda pro zobrazení stavu skladu z databáze.
        """
        self.clear_content_frame()

        canvas = tk.Canvas(self.content_frame, bg="#B0B0E0", bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#B0B0E0")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        stocks = self.data_operations.get_stock_status()

        for stock in stocks:
            stock_label = tk.Label(self.scrollable_frame, text=f"Sklad: {stock['nazev']}\n"
                                                               f"Adresa: {stock['adresa']}\n"
                                                               f"Produkt ID: {stock['produkt_id']}\n"
                                                               f"Název produktu: {stock['nazev_produktu']}\n"
                                                               f"Množství: {stock['mnozstvi']}",
                                   font=("Helvetica", 14), bg="#B0B0E0", width=70)
            stock_label.pack(fill=tk.X, padx=20, pady=20)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_store_status(self):
        """
        Metoda pro zobrazeni informaci o poctu produktu na obchodech

        """
        # Smaže aktuální obsah frame.
        self.clear_content_frame()
        # Vytvoří canvas pro zobrazení scrollbaru.
        canvas = tk.Canvas(self.content_frame, bg="#B0B0E0", bd=0, highlightthickness=0)
        # Vytvoří scrollbar.
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        # Vytvoří frame, do kterého se vloží záznamy z databáze.
        self.scrollable_frame = tk.Frame(canvas, bg="#B0B0E0")
        # Nastaví scrollbar pro canvas.
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        # Získá záznamy o stavu skladu z databáze.
        stores = self.data_operations.get_store_status()
        # Vytvoří labely pro každý záznam ze skladu.
        for store in stores:
            store_label = tk.Label(self.scrollable_frame, text=f"Obchod: {store['nazev']}\n"
                                                               f"Adresa: {store['adresa']}\n"
                                                               f"Produkt ID: {store['produkt_id']}\n"
                                                               f"Název produktu: {store['nazev_produktu']}\n"
                                                               f"Množství: {store['mnozstvi']}",
                                   font=("Helvetica", 14), bg="#B0B0E0", width=70)
            store_label.pack(fill=tk.X, padx=20, pady=20)
        # Umístí canvas na levou stranu, aby se zobrazil scrollbar.
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # Umístí canvas na levou stranu, aby se zobrazil scrollbar.
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_employee_info(self):
        """
        Metoda pro zobrazeni informací o zaměstnanci
        Nejdříve se vyčistí content frame a pak zobrazí obsah
        """
        self.clear_content_frame()

        info_label = tk.Label(self.content_frame, text=f"ID: {self.employee_dict['id']}\n"
                                                       f"Jméno: {self.employee_dict['jmeno']}\n"
                                                       f"Příjmení: {self.employee_dict['prijmeni']}\n"
                                                       f"Uživatelské jméno: {self.employee_dict['uzivatelske_jmeno']}",
                              font=("Helvetica", 14), bg="#B0B0E0")
        info_label.pack(padx=20, pady=20)

