from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from conn import DatabaseConnection


class ProductWindows:
    """
     Třída pro správu oken souvisejících s produkty, obsahuje metody pro zobrazení tlačítek správy produktů,
     přidání produktu do skladu a vytvoření okna pro přidání produktu.
     """

    def __init__(self, content_frame):
        """
        Inicializuje instanci třídy ProductWindows s odkazem na obsahový rámec (content_frame).

        :param content_frame: odkaz na obsahový rámec
        """
        self.content_frame = content_frame

    def clear_content(self):
        """
        Odstraní všechny widgety z obsahového rámce.
        """

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    @staticmethod
    def set_window_center(window, width, height):
        """
        Nastaví pozici okna na střed obrazovky s danou šířkou a výškou.

        :param window: okno, které chcete vycentrovat
        :param width: šířka okna
        :param height: výška okna
        """

        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    def show_product_management_buttons(self):
        """
        Zobrazí tlačítka pro správu produktů v obsahovém rámci.
        """
        self.clear_content()
        self.products_button_frame = tk.Frame(self.content_frame, bg="#B0B0E0")

        add_product_button = ttk.Button(self.products_button_frame, text="Přidat produkt",
                                            command=lambda: ProductWindows.add_product_window(self.content_frame))
        add_product_button.pack(pady=(10, 0))

        move_product_button = ttk.Button(self.products_button_frame, text="Přesunout produkt",
                                             command=lambda: ProductWindows.move_product_window(self.content_frame))
        move_product_button.pack(pady=(10, 0))

        remove_product_button = ttk.Button(self.products_button_frame, text="Odebrat produkt",
                                               command=lambda: ProductWindows.remove_product_window(self.content_frame))
        remove_product_button.pack(pady=(10, 0))

        self.products_button_frame.pack(anchor='n', pady=10)

    @staticmethod
    def add_product_to_warehouse(warehouse_id, product_id, quantity):
        """
        Přidá zadané množství produktu s daným ID produktu do skladu s daným ID skladu.

        :param warehouse_id: ID skladu, do kterého se má přidat produkt
        :param product_id: ID produktu, který se má přidat
        :param quantity: množství produktu k přidání
        """
        db_connection = DatabaseConnection()
        conn = db_connection.connect_to_database()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO sklad_produkt (sklad_id, produkt_id, mnozstvi) "
            "VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE mnozstvi = mnozstvi + %s",
            (warehouse_id, product_id, quantity, quantity)
        )

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def add_product_window(parent):
        """
        Vytvoří okno pro přidání produktu, které umožňuje uživateli vybrat produkt, sklad a zadané množství.

        :param parent: odkaz na nadřazený widget
        """
        db_connection = DatabaseConnection()
        conn = db_connection.connect_to_database()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nazev FROM sklad")
        warehouses = cursor.fetchall()

        cursor.execute("SELECT id, nazev FROM produkt")
        products = cursor.fetchall()

        conn.close()

        add_product_win = tk.Toplevel(parent)
        add_product_win.title("Přidat produkt")
        add_product_win.minsize(400, 300)
        add_product_win.configure(bg="#B0B0E0")

        ProductWindows.set_window_center(add_product_win, 400, 300)

        product_label = tk.Label(add_product_win, text="Produkt:", bg="#B0B0E0")
        product_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        product_var = tk.StringVar(add_product_win)
        product_dropdown = ttk.Combobox(add_product_win, textvariable=product_var)
        product_dropdown['values'] = [f"{product[0]} - {product[1]}" for product in products]
        product_dropdown.grid(row=0, column=1, padx=20, pady=20)

        warehouse_label = tk.Label(add_product_win, text="Sklad:", bg="#B0B0E0")
        warehouse_label.grid(row=1, column=0, padx=20, pady=20, sticky="e")

        warehouse_var = tk.StringVar(add_product_win)
        warehouse_dropdown = ttk.Combobox(add_product_win, textvariable=warehouse_var)
        warehouse_dropdown['values'] = [f"{warehouse[0]} - {warehouse[1]}" for warehouse in warehouses]
        warehouse_dropdown.grid(row=1, column=1, padx=20, pady=20)

        quantity_label = tk.Label(add_product_win, text="Množství:", bg="#B0B0E0")
        quantity_label.grid(row=2, column=0, padx=20, pady=20, sticky="e")

        quantity_entry = tk.Entry(add_product_win)
        quantity_entry.grid(row=2, column=1, padx=20, pady=20)

        def add_product_to_warehouse():
            try:
                selected_warehouse = warehouse_var.get().split(" - ")[0]
                warehouse_id = int(selected_warehouse)
                selected_product = product_var.get().split(" - ")[0]
                product_id = int(selected_product)
                quantity = int(quantity_entry.get())

                if quantity <= 0:
                    messagebox.showerror("Chyba", "Množství musí být kladné číslo.")
                    return

                ProductWindows.add_product_to_warehouse(warehouse_id, product_id, quantity)
                messagebox.showinfo("Úspěch", "Produkt byl úspěšně přidán do skladu.")
            except ValueError:
                messagebox.showerror("Chyba", "Zadejte platná čísla pro ID produktu a množství.")

            product_dropdown.set('')
            warehouse_dropdown.set('')
            quantity_entry.delete(0, tk.END)

        add_product_button = ttk.Button(add_product_win, text="Přidat produkt", command=add_product_to_warehouse)
        add_product_button.grid(row=3, column=0, columnspan=2, pady=(10, 20))

        product_dropdown.set('')
        warehouse_dropdown.set('')
        quantity_entry.delete(0, tk.END)

    @staticmethod
    def move_product_window(parent):
        """
        Vytvoří okno pro přesun produktů mezi sklady a obchody, které umožňuje uživateli vybrat zdrojové a cílové místo,
        produkt a zadané množství.

        :param parent: odkaz na nadřazený widget
        """
        def get_warehouses_and_shops():
            """
            Načte seznam skladů a obchodů z databáze a vrátí jej jako tuple (sklady, obchody).
            """
            cursor.execute("SELECT id, nazev FROM sklad")
            warehouses = cursor.fetchall()

            cursor.execute("SELECT id, nazev FROM obchod")
            shops = cursor.fetchall()

            return warehouses, shops

        def get_products():
            """
            Načte seznam produktů z databáze a vrátí jej.
            """
            cursor.execute("SELECT id, nazev FROM produkt")
            return cursor.fetchall()

        db_connection = DatabaseConnection()
        conn = db_connection.connect_to_database()
        cursor = conn.cursor()

        warehouses, shops = get_warehouses_and_shops()
        products = get_products()

        conn.close()

        move_product_win = tk.Toplevel(parent)
        move_product_win.title("Přesunout produkt")
        move_product_win.minsize(400, 300)
        move_product_win.configure(bg="#B0B0E0")

        ProductWindows.set_window_center(move_product_win, 400, 300)

        from_label = tk.Label(move_product_win, text="Z:", bg="#B0B0E0")
        from_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        from_var = tk.StringVar(move_product_win)
        from_dropdown = ttk.Combobox(move_product_win, textvariable=from_var)
        from_dropdown['values'] = [f"{warehouse[0]} - Sklad - {warehouse[1]}" for warehouse in warehouses] + \
                                  [f"{shop[0]} - Obchod - {shop[1]}" for shop in shops]
        from_dropdown.grid(row=0, column=1, padx=20, pady=20)

        to_label = tk.Label(move_product_win, text="Do:", bg="#B0B0E0")
        to_label.grid(row=1, column=0, padx=20, pady=20, sticky="e")

        to_var = tk.StringVar(move_product_win)
        to_dropdown = ttk.Combobox(move_product_win, textvariable=to_var)
        to_dropdown['values'] = [f"{warehouse[0]} - Sklad - {warehouse[1]}" for warehouse in warehouses] + \
                                [f"{shop[0]} - Obchod - {shop[1]}" for shop in shops]
        to_dropdown.grid(row=1, column=1, padx=20, pady=20)

        product_label = tk.Label(move_product_win, text="Produkt:", bg="#B0B0E0")
        product_label.grid(row=2, column=0, padx=20, pady=20, sticky="e")

        product_var = tk.StringVar(move_product_win)
        product_dropdown = ttk.Combobox(move_product_win, textvariable=product_var)
        product_dropdown['values'] = [f"{product[0]} - {product[1]}" for product in products]
        product_dropdown.grid(row=2, column=1, padx=20, pady=20)

        quantity_label = tk.Label(move_product_win, text="Množství:", bg="#B0B0E0")
        quantity_label.grid(row=3, column=0, padx=20, pady=20, sticky="e")

        quantity_entry = tk.Entry(move_product_win)
        quantity_entry.grid(row=3, column=1, padx=20, pady=20)

        def move_product():
            try:
                # Získání informací o zdrojovém a cílovém místě, ID produktu a množství
                from_id, from_type, _ = from_var.get().split(" - ")
                to_id, to_type, _ = to_var.get().split(" - ")
                from_id, to_id = int(from_id), int(to_id)
                product_id = int(product_var.get().split(" - ")[0])
                quantity = int(quantity_entry.get())
                # Kontrola, zda je zadané množství kladné číslo
                if quantity <= 0:
                    messagebox.showerror("Chyba", "Množství musí být kladné číslo.")
                    return
                # Kontrola, zda zdrojové a cílové místo nejsou stejné
                if from_id == to_id and from_type == to_type:
                    messagebox.showerror("Chyba", "Nelze přesunout produkt na stejné místo.")
                    return
                # Připojení k databázi
                db_connection = DatabaseConnection()
                conn = db_connection.connect_to_database()
                cursor = conn.cursor()
                # Příprava názvů tabulek pro dotazy
                from_table = f"{from_type.lower()}_produkt"
                to_table = f"{to_type.lower()}_produkt"
                # Získání aktuálního množství produktu na zdrojovém místě
                cursor.execute(f"SELECT mnozstvi FROM {from_table} WHERE {from_type.lower()}"
                               f"_id = %s AND produkt_id = %s",
                               (from_id, product_id))
                from_quantity = cursor.fetchone()
                # Kontrola zda je dostatek produktu k přesunu
                if from_quantity is None or from_quantity[0] < quantity:
                    messagebox.showerror("Chyba", "Nedostatečné množství produktu k přesunu.")
                    return
                # Snížení množství produktu na zdrojovém místě
                cursor.execute(
                    f"UPDATE {from_table} SET mnozstvi = mnozstvi - %s WHERE {from_type.lower()}"
                    f"_id = %s AND produkt_id = %s",
                    (quantity, from_id, product_id))
                # Získání aktuálního množství produktu na cílovém místě
                cursor.execute(f"SELECT mnozstvi FROM {to_table} WHERE {to_type.lower()}"
                               f"_id = %s AND produkt_id = %s",
                               (to_id, product_id))
                to_quantity = cursor.fetchone()
                # Přidání produktu na cílové místo (pokud tam již existuje) nebo vložení nového záznamu
                if to_quantity is None:
                    cursor.execute(
                        f"INSERT INTO {to_table} ({to_type.lower()}_id, produkt_id, mnozstvi) VALUES (%s, %s, %s)",
                        (to_id, product_id, quantity))
                else:
                    cursor.execute(
                        f"UPDATE {to_table} SET mnozstvi = mnozstvi + %s WHERE {to_type.lower()}"
                        f"_id = %s AND produkt_id = %s",
                        (quantity, to_id, product_id))

                conn.commit()
                conn.close()
                messagebox.showinfo("Úspěch", "Produkt úspěšně přesunut.")

            except ValueError:
                messagebox.showerror("Chyba", "Neplatná hodnota vstupu.")
            except Exception as e:
                messagebox.showerror("Chyba", f"Nastala neočekávaná chyba: {str(e)}")

        move_product_button = ttk.Button(move_product_win, text="Přesunout produkt", command=move_product)
        move_product_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

    @staticmethod
    def remove_product_window(parent):
        """
        Tato metoda vytváří okno pro odebrání produktu ze skladu nebo obchodu.

        :param:
        parent (tkinter.Tk nebo tkinter.Toplevel): Rodičovské okno, kterému okno pro odebrání produktu patří.
        """
        def get_warehouses_and_shops():
            """
            Tato funkce získává seznam skladů a obchodů z databáze.

            :return:
            tuple: Návratová hodnota obsahuje dva seznamy - seznam skladů a seznam obchodů.
            """
            cursor.execute("SELECT id, nazev FROM sklad")
            warehouses = cursor.fetchall()

            cursor.execute("SELECT id, nazev FROM obchod")
            shops = cursor.fetchall()

            return warehouses, shops

        def get_products():
            """
            Tato funkce získává seznam produktů z databáze.

            :return:
            list: Seznam produktů získaných z databáze.
            """
            cursor.execute("SELECT id, nazev FROM produkt")
            return cursor.fetchall()

        db_connection = DatabaseConnection()
        conn = db_connection.connect_to_database()
        cursor = conn.cursor()

        warehouses, shops = get_warehouses_and_shops()
        products = get_products()

        conn.close()
        # Vytvoření a konfigurace okna pro odebrání produktu
        remove_product_win = tk.Toplevel(parent)
        remove_product_win.title("Odebrat produkt")
        remove_product_win.minsize(400, 300)
        remove_product_win.configure(bg="#B0B0E0")

        ProductWindows.set_window_center(remove_product_win, 400, 300)

        location_label = tk.Label(remove_product_win, text="Umístění:", bg="#B0B0E0")
        location_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        location_var = tk.StringVar(remove_product_win)
        location_dropdown = ttk.Combobox(remove_product_win, textvariable=location_var)
        location_dropdown['values'] = [f"{warehouse[0]} - Sklad - {warehouse[1]}" for warehouse in warehouses] + \
                                      [f"{shop[0]} - Obchod - {shop[1]}" for shop in shops]
        location_dropdown.grid(row=0, column=1, padx=20, pady=20)

        product_label = tk.Label(remove_product_win, text="Produkt:", bg="#B0B0E0")
        product_label.grid(row=1, column=0, padx=20, pady=20, sticky="e")

        product_var = tk.StringVar(remove_product_win)
        product_dropdown = ttk.Combobox(remove_product_win, textvariable=product_var)
        product_dropdown['values'] = [f"{product[0]} - {product[1]}" for product in products]
        product_dropdown.grid(row=1, column=1, padx=20, pady=20)

        quantity_label = tk.Label(remove_product_win, text="Množství:", bg="#B0B0E0")
        quantity_label.grid(row=2, column=0, padx=20, pady=20, sticky="e")

        quantity_entry = tk.Entry(remove_product_win)
        quantity_entry.grid(row=2, column=1, padx=20, pady=20)

        def remove_product():
            """
            Tato funkce je volána po stisknutí tlačítka "Odebrat produkt" a zajišťuje odebrání produktu ze zvoleného skladu nebo obchodu.
            """
            try:
                # Získání informací o umístění ID produktu a množství
                location_id, location_type, _ = location_var.get().split(" - ")
                location_id = int(location_id)
                product_id = int(product_var.get().split(" - ")[0])
                quantity = int(quantity_entry.get())
                # Kontrola, zda je zadané množství kladné číslo
                if quantity <= 0:
                    messagebox.showerror("Chyba", "Množství musí být kladné číslo.")
                    return
                # Připojení k databázi a aktualizace množství produktu na zvoleném umístění
                db_connection = DatabaseConnection()
                conn = db_connection.connect_to_database()
                cursor = conn.cursor()

                location_table = f"{location_type.lower()}_produkt"

                cursor.execute(
                    f"SELECT mnozstvi FROM {location_table} WHERE {location_type.lower()}_id = %s AND produkt_id = %s",
                    (location_id, product_id))
                current_quantity = cursor.fetchone()
                # Zobrazení výsledku operace
                if current_quantity is None or current_quantity[0] < quantity:
                    messagebox.showerror("Chyba", f"Nedostatek produktů na {location_type.lower()} pro odebrání.")
                else:
                    new_quantity = current_quantity[0] - quantity
                    if new_quantity == 0:
                        cursor.execute(
                            f"DELETE FROM {location_table} WHERE {location_type.lower()}_id = %s AND produkt_id = %s",
                            (location_id, product_id))
                    else:
                        cursor.execute(
                            f"UPDATE {location_table} SET mnozstvi = %s WHERE {location_type.lower()}"
                            f"_id = %s AND produkt_id = %s",
                            (new_quantity, location_id, product_id))

                    conn.commit()
                    messagebox.showinfo("Úspěch", f"{quantity} ks produktu bylo odebráno z {location_type.lower()}.")

                conn.close()
            except ValueError:
                messagebox.showerror("Chyba", "Množství musí být číslo.")
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        # Vytvoření tlačítka pro odebrání produktu a přiřazení funkce remove_product
        remove_button = ttk.Button(remove_product_win, text="Odebrat produkt", command=remove_product)
        remove_button.grid(row=3, column=0, columnspan=2, pady=20)
