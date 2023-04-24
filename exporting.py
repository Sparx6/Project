import csv
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from conn import DatabaseConnection

class ExportInformation:
    """
    Tato třída poskytuje funkce pro export různých druhů dat z aplikace.
    """
    @staticmethod
    def show_export_frame(content_frame):
        """
        Zobrazí rámeček pro export dat (produkty, zákazníci, sklady, obchody, dodavatelé) v hlavním okně aplikace.

        :param
        content_frame (tk.Frame): Rámeček, do kterého se umístí tlačítka pro export různých typů dat.
        """
        # Zničí všechny existující widgety v content_frame
        for widget in content_frame.winfo_children():
            widget.destroy()
        # Vytvoří a umístí tlačítka pro export různých typů dat
        export_products_button = ttk.Button(content_frame, text="Export produktů",
                                           command=ExportInformation.export_products)
        export_products_button.pack(pady=(10, 10))

        export_customers_button = ttk.Button(content_frame, text="Export zákazníků",
                                             command=ExportInformation.export_customers)
        export_customers_button.pack(pady=(10, 10))

        export_warehouses_button = ttk.Button(content_frame, text="Export skladů",
                                              command=ExportInformation.export_warehouses)
        export_warehouses_button.pack(pady=(10, 10))

        export_stores_button = ttk.Button(content_frame, text="Export obchodů",
                                          command=ExportInformation.export_stores)
        export_stores_button.pack(pady=(10, 10))

        export_suppliers_button = ttk.Button(content_frame, text="Export dodavatelů",
                                             command=ExportInformation.export_suppliers)
        export_suppliers_button.pack(pady=(10, 10))



    @staticmethod
    def export_products():
        """
        Otevírá okno pro export produktů ze skladů a obchodů.
        """
        export_win = tk.Toplevel()
        export_win.title("Export produktů")
        export_win.configure(bg="#B0B0E0")
        export_win.geometry("300x150")

        warehouse_products_button = ttk.Button(export_win, text="Exportovat produkty na skladech",
                                               command=ExportInformation.export_products_to_csv_warehouses)
        warehouse_products_button.pack(pady=(10, 10), padx=(10, 10))

        store_products_button = ttk.Button(export_win, text="Exportovat produkty v obchodech",
                                           command=ExportInformation.export_products_to_csv_stores)
        store_products_button.pack(pady=(10, 10), padx=(10, 10))

        close_button = ttk.Button(export_win, text="Zavřít", command=export_win.destroy)
        close_button.pack(pady=(10, 20), side="bottom", anchor="s")

        export_win.update_idletasks()
        width, height = export_win.winfo_width(), export_win.winfo_height()
        x = (export_win.winfo_screenwidth() // 2) - (width // 2)
        y = (export_win.winfo_screenheight() // 2) - (height // 2)
        export_win.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def export_products_to_csv_warehouses():
        """
        Exportuje data o produktech na skladech do CSV souboru.
        """
        products_data = ExportInformation.fetch_products_from_warehouses()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialdir="exports")
        if not file_path:
            return
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Produkt ID", "Název", "Popis", "Cena", "Sklad ID", "Množství"])
            for product in products_data:
                writer.writerow(product)

    @staticmethod
    def export_products_to_csv_stores():
        """
        Exportuje data o produktech v obchodech do CSV souboru.
        """
        products_data = ExportInformation.fetch_products_from_stores()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialdir="exports")
        if not file_path:
            return
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Produkt ID", "Název", "Popis", "Cena", "Obchod ID", "Množství"])
            for product in products_data:
                writer.writerow(product)

    @staticmethod
    def fetch_products_from_warehouses():
        """
        Načte data o produktech na skladech z databáze.

        :return
        List[tuple]: Seznam n-tic obsahující informace o produktech na skladech.
        """
        try:
            db_connection = DatabaseConnection().connect_to_database()
            cursor = db_connection.cursor()

            query = """
                SELECT p.id, p.nazev, p.popis, p.cena, sp.sklad_id, sp.mnozstvi
                FROM produkt p
                JOIN sklad_produkt sp ON p.id = sp.produkt_id
                """

            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst data: {str(e)}")
            return []

    @staticmethod
    def fetch_products_from_stores():
        """
        Načte data o produktech v obchodech z databáze.

        :return
        List[tuple]: Seznam n-tic obsahující informace o produktech v obchodech.
        """
        try:
            db_connection = DatabaseConnection().connect_to_database()
            cursor = db_connection.cursor()

            query = """
                       SELECT p.id, p.nazev, p.popis, p.cena, op.obchod_id, op.mnozstvi
                       FROM produkt p
                       JOIN obchod_produkt op ON p.id = op.produkt_id
                       """

            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst data: {str(e)}")
            return []

    @staticmethod
    def export_customers():
        """
        Vytvoří okno pro export zákazníků do CSV souboru.
        """

        def export_customers_to_csv():
            """
            Exportuje data o zákaznících do CSV souboru.
            """
            # Připojení k databázi a výběr zákazníků
            try:
                db_connection = DatabaseConnection().connect_to_database()
                cursor = db_connection.cursor()

                query = """
                SELECT id, jmeno, prijmeni, email, vernostni_body
                FROM zakaznik
                """

                cursor.execute(query)
                customers = cursor.fetchall()
                # Vrací výběr uživatele. V případě zavření bez výběru vrací prázdný řetězec
                file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                         filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

                if file_path:  # Ověření, že byla zvolena cesta k souboru
                    # Otevření souboru pro zápis v režimu UTF-8
                    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                        # Vytvoření CSV writeru pro zápis do souboru
                        writer = csv.writer(csvfile)
                        # Zápis hlavičky s názvy sloupců do souboru
                        writer.writerow(["ID", "Jméno", "Příjmení", "E-mail", "Věrnostní body"])
                        for customer in customers: # Iterace přes seznam zákazníků
                            writer.writerow(customer) # Zápis údajů o zákazníkovi do souboru

            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se exportovat data: {str(e)}")

        export_customers_win = tk.Toplevel()
        export_customers_win.title("Export zákazníků")
        export_customers_win.configure(bg="#B0B0E0")
        export_customers_win.geometry("300x150")

        export_customers_button = ttk.Button(export_customers_win, text="Exportovat zákazníky",
                                             command=export_customers_to_csv)
        export_customers_button.pack(pady=(10, 10), padx=(10, 10))

        close_button = ttk.Button(export_customers_win, text="Zavřít", command=export_customers_win.destroy)
        close_button.pack(pady=(10, 20), side="bottom", anchor="s")

        export_customers_win.update_idletasks()
        width, height = export_customers_win.winfo_width(), export_customers_win.winfo_height()
        x = (export_customers_win.winfo_screenwidth() // 2) - (width // 2)
        y = (export_customers_win.winfo_screenheight() // 2) - (height // 2)
        export_customers_win.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def export_warehouses():
        """
        Vytvoří okno pro export skládů do CSV souboru.
        """
        def export_warehouses_to_csv():
            """
            Exportuje data o skladech do CSV souboru.
            """
            try:
                db_connection = DatabaseConnection().connect_to_database()
                cursor = db_connection.cursor()

                query = """
                SELECT id, nazev, adresa
                FROM sklad
                """

                cursor.execute(query)
                warehouses = cursor.fetchall()

                file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                         filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

                if file_path:
                    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["ID", "Název", "Adresa"])
                        for warehouse in warehouses:
                            writer.writerow(warehouse)

            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se exportovat data: {str(e)}")

        export_warehouses_win = tk.Toplevel()
        export_warehouses_win.title("Export skládů")
        export_warehouses_win.configure(bg="#B0B0E0")
        export_warehouses_win.geometry("300x150")

        export_warehouses_button = ttk.Button(export_warehouses_win, text="Exportovat sklady",
                                              command=export_warehouses_to_csv)
        export_warehouses_button.pack(pady=(10, 10), padx=(10, 10))

        close_button = ttk.Button(export_warehouses_win, text="Zavřít", command=export_warehouses_win.destroy)
        close_button.pack(pady=(10, 20), side="bottom", anchor="s")

        export_warehouses_win.update_idletasks()
        width, height = export_warehouses_win.winfo_width(), export_warehouses_win.winfo_height()
        x = (export_warehouses_win.winfo_screenwidth() // 2) - (width // 2)
        y = (export_warehouses_win.winfo_screenheight() // 2) - (height // 2)
        export_warehouses_win.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def export_stores():
        """
        Vytvoří okno pro export obchodů do CSV souboru.
        """
        def export_stores_to_csv():
            """
            Exportuje data o obchodech do CSV souboru.
            """
            try:
                db_connection = DatabaseConnection().connect_to_database()
                cursor = db_connection.cursor()

                query = """
                SELECT id, nazev, adresa
                FROM obchod
                """

                cursor.execute(query)
                stores = cursor.fetchall()

                file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

                if file_path:
                    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["ID", "Název", "Adresa"])
                        for store in stores:
                            writer.writerow(store)

            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se exportovat data: {str(e)}")

        export_stores_win = tk.Toplevel()
        export_stores_win.title("Export obchodů")
        export_stores_win.configure(bg="#B0B0E0")
        export_stores_win.geometry("300x150")

        export_stores_button = ttk.Button(export_stores_win, text="Exportovat obchody",
                                          command=export_stores_to_csv)
        export_stores_button.pack(pady=(10, 10), padx=(10, 10))

        close_button = ttk.Button(export_stores_win, text="Zavřít", command=export_stores_win.destroy)
        close_button.pack(pady=(10, 20), side="bottom", anchor="s")

        export_stores_win.update_idletasks()
        width, height = export_stores_win.winfo_width(), export_stores_win.winfo_height()
        x = (export_stores_win.winfo_screenwidth() // 2) - (width // 2)
        y = (export_stores_win.winfo_screenheight() // 2) - (height // 2)
        export_stores_win.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def export_suppliers():
        """
        Vytvoří okno pro export dodavatelů do CSV souboru.
        """
        def export_suppliers_to_csv():
            """
            Exportuje data o dodavatelích do CSV souboru.
            """
            file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV soubory", "*.csv")])
            if not file_name:
                return

            connection = DatabaseConnection().connect_to_database()
            cursor = connection.cursor()

            query = "SELECT * FROM dodavatel"
            cursor.execute(query)
            suppliers = cursor.fetchall()

            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'nazev', 'adresa', 'kontakt_telefon', 'kontakt_email', 'druh_zbozi'])
                for supplier in suppliers:
                    writer.writerow(supplier)

            connection.close()

        export_win = tk.Toplevel()
        export_win.title("Export dodavatelů")
        export_win.configure(bg="#B0B0E0")
        export_win.geometry("300x150")

        export_button = ttk.Button(export_win, text="Exportovat dodavatelů",
                                   command=export_suppliers_to_csv)
        export_button.pack(pady=(10, 10), padx=(10, 10))

        close_button = ttk.Button(export_win, text="Zavřít", command=export_win.destroy)
        close_button.pack(pady=(10, 20), side="bottom", anchor="s")

        export_win.update_idletasks()
        width, height = export_win.winfo_width(), export_win.winfo_height()
        x = (export_win.winfo_screenwidth() // 2) - (width // 2)
        y = (export_win.winfo_screenheight() // 2) - (height // 2)
        export_win.geometry(f"{width}x{height}+{x}+{y}")

