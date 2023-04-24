import tkinter as tk
from tkinter import ttk
from conn import DatabaseConnection
from tkinter import messagebox
from info_customer import InformationWin
class InformationDisplays:
    @staticmethod
    def show_info_frame(content_frame):
        """
        Tato metoda vytvoří tlačítka pro zobrazení různých typů informací o skladu a objednávkách. Po kliknutí na tlačítko se zobrazí
        příslušné informace.

        :param content_frame: Frame, do kterého se vloží tlačítka pro zobrazení informací.
        """
        # Odstranění starých widgetů v obsahovém framu, aby se načetly nové informace.
        for widget in content_frame.winfo_children():
            widget.destroy()
        # Tlačítko pro zobrazení skladů a jejich dodavatelů
        warehouses_suppliers_button = ttk.Button(content_frame, text="Zobrazení skladů a jejich dodavatelů",
                                                 command=InformationDisplays.display_warehouses_and_suppliers)
        warehouses_suppliers_button.pack(pady=(10, 10))
        # Tlačítko pro zobrazení stavu produktů na skladech
        product_stock_status_button = ttk.Button(content_frame, text="Zobrazení stavu produktů na skladech",
                                                 command=InformationDisplays.display_product_stock_status)
        product_stock_status_button.pack(pady=(10, 10))
        # Tlačítko pro zobrazení stavu produktů v obchodech
        product_stock_status_in_stores_button = ttk.Button(content_frame, text="Zobrazení stavu produktů v obchodech",
                                                           command=InformationDisplays.display_product_stock_status_in_stores)
        product_stock_status_in_stores_button.pack(pady=(10, 10))
        # Tlačítko pro zobrazení všech zaměstnanců
        employee_show_status_button = ttk.Button(content_frame, text="Zobrazení všech zaměstnanců",
                                                 command=InformationDisplays.display_employees)
        employee_show_status_button.pack(pady=(10, 10))
        # Tlačítko pro zobrazení zákazníků
        view_customers_button = ttk.Button(content_frame, text="Zobrazit zákazníky",
                                           command=InformationDisplays.display_customers)
        view_customers_button.pack(pady=(10, 0), padx=(0, 10))
        # Tlačítko pro zobrazení objednávek
        view_orders_button = ttk.Button(content_frame, text="Zobrazit objednávky",
                                        command=InformationWin.display_orders)
        view_orders_button.pack(pady=(10, 0), padx=(0, 10))
    @staticmethod
    def display_warehouses_and_suppliers():
        """
        Třída která se stará o zobrazení seznamu skladů a jejich dodavatelů v novém okně aplikace.
        """
        def fetch_warehouses_and_suppliers(order_by=None):
            """
            Metoda pro načtení dat o skladech a jejich dodavatelích z databáze.

            :param order_by: (str) Název sloupce, podle kterého se mají data seřadit.
            :return: Tuple[list] Seznam skladišť a jejich dodavatelů.
            """

            try:
                # Připojení k databázi
                db_connection = DatabaseConnection().connect_to_database()
                cursor = db_connection.cursor()
                # Sestavení dotazu pro načtení dat o skladech a jejich dodavatelích
                query = """
                SELECT sklad.id AS sklad_id, sklad.nazev AS sklad_nazev, sklad.adresa AS sklad_adresa, dodavatel.nazev AS dodavatel_nazev
                FROM sklad
                JOIN dodavatel_sklad ON sklad.id = dodavatel_sklad.sklad_id
                JOIN dodavatel ON dodavatel_sklad.dodavatel_id = dodavatel.id
                """
                # Přidání řazení podle sloupce, pokud je definován
                if order_by:
                    query += f"ORDER BY {order_by}"
                # Spuštění dotazu
                cursor.execute(query)
                # Vrácení výsledků
                return cursor.fetchall()
            except Exception as e:
                # Vypsání chyby, pokud dojde k ní při načítání dat
                messagebox.showerror("Chyba", f"Nepodařilo se načíst data ze serveru: {str(e)}")

        def refresh_tree(tree, order_by=None):
            """
            Metoda pro aktualizaci zobrazených dat v Treeview.

            :param tree: (ttk.Treeview) Treeview widget, který se má aktualizovat.
            :param order_by: (str) Název sloupce, podle kterého se mají data seřadit.
            :return: None
            """
            # Smazání všech položek v tabulce(rozbaluje seznam a předava jako argumenty)
            tree.delete(*tree.get_children())
            # Načtení nových dat z databáze
            data = fetch_warehouses_and_suppliers(order_by)
            # Vložení nových dat do Treeview
            for item in data:
                tree.insert("", "end", values=item)

        # Vytvoření nového okna pro zobrazení seznamu skladů a jejich dodavatelů
        warehouse_suppliers_win = tk.Toplevel()
        warehouse_suppliers_win.title("Sklady a jejich dodavatelé")
        warehouse_suppliers_win.configure(bg="#B0B0E0")
        warehouse_suppliers_win.geometry("800x600")

        main_frame = tk.Frame(warehouse_suppliers_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        content_frame = tk.Frame(main_frame, bg="#B0B0E0")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tree_scrollbar = ttk.Scrollbar(content_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(content_frame, columns=("Sklad ID", "Sklad", "Adresa", "Dodavatel"), show="headings",
                            yscrollcommand=tree_scrollbar.set)
        tree.heading("Sklad ID", text="Sklad ID")
        tree.heading("Sklad", text="Sklad")
        tree.heading("Adresa", text="Adresa")
        tree.heading("Dodavatel", text="Dodavatel")
        tree.column("Sklad ID", width=100, anchor="center")
        tree.column("Sklad", width=200, anchor="center")
        tree.column("Adresa", width=200, anchor="center")
        tree.column("Dodavatel", width=200, anchor="center")

        refresh_tree(tree)
        tree_scrollbar.config(command=tree.yview)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        buttons_frame = tk.Frame(main_frame, bg="#B0B0E0")
        buttons_frame.pack(side="top", pady=(10, 0))

        sort_by_id = ttk.Button(buttons_frame, text="Seřadit podle ID skladů",
                                command=lambda: refresh_tree(tree, "sklad.id"))
        sort_by_id.pack(side="left", padx=(10, 0))

        sort_by_sklad_nazev = ttk.Button(buttons_frame, text="Seřadit podle názvu skladu",
                                    command=lambda: refresh_tree(tree, "sklad.nazev"))
        sort_by_sklad_nazev.pack(side="left", padx=(10, 0))

        sort_by_dodavatel_nazev = ttk.Button(buttons_frame, text="Seřadit podle názvu dodavatele",
                                             command=lambda: refresh_tree(tree, "dodavatel.nazev"))
        sort_by_dodavatel_nazev.pack(side="left", padx=(10, 0))

        close_button = ttk.Button(main_frame, text="Zavřít", command=warehouse_suppliers_win.destroy)
        close_button.pack(pady=(10, 0), side="bottom", anchor="s")

        warehouse_suppliers_win.update_idletasks()
        width, height = warehouse_suppliers_win.winfo_width(), warehouse_suppliers_win.winfo_height()
        x = (warehouse_suppliers_win.winfo_screenwidth() // 2) - (width // 2)
        y = (warehouse_suppliers_win.winfo_screenheight() // 2) - (height // 2)
        warehouse_suppliers_win.geometry(f"{width}x{height}+{x}+{y}")
    @staticmethod
    def display_product_stock_status():
        """
        Metoda pro zobrazení stavu produktů na skladech v tabulce.
        """
        def fetch_product_stock_data(order_by=None):
            """
            Vnitřní metoda pro načtení dat o stavech produktů na skladech z databáze.
            :param order_by: sloupec pro řazení výsledků (volitelné)
            :return: seznam n-tic obsahujících informace o stavech produktů na skladech
            """
            try:
                db_connection = DatabaseConnection().connect_to_database()
                cursor = db_connection.cursor()

                query = """
                SELECT sklad.id AS sklad_id, sklad.nazev AS sklad_nazev, produkt.nazev AS produkt_nazev, sklad_produkt.mnozstvi
                FROM sklad
                JOIN sklad_produkt ON sklad.id = sklad_produkt.sklad_id
                JOIN produkt ON sklad_produkt.produkt_id = produkt.id
                """

                if order_by:
                    query += f"ORDER BY {order_by}"

                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se načíst data ze serveru: {str(e)}")

        def refresh_tree(tree, order_by=None):
            """
            Vnitřní metoda pro aktualizaci obsahu tabulky se stavy produktů na skladech.
            :param tree: objekt Ttk.Treeview reprezentující tabulku
            :param order_by: sloupec pro řazení výsledků (volitelné)
            """
            # Smazání všech položek v tabulce(rozbaluje seznam a předava jako argumenty)
            tree.delete(*tree.get_children())
            # Načtení dat o produktech na skladech a jejich řazení podle zadaného kritéria (pokud je poskytnuto)
            data = fetch_product_stock_data(order_by)
            # Vložení načtených dat o zaměstnancích do tabulky
            for item in data:
                tree.insert("", "end", values=item)

        # Vytvoření nového okna pro zobrazení tabulky
        product_stock_win = tk.Toplevel()
        product_stock_win.title("Stav produktů na skladech")
        product_stock_win.configure(bg="#B0B0E0")
        product_stock_win.geometry("800x600")
        # Vytvoření hlavního rámečku pro okno
        main_frame = tk.Frame(product_stock_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoření objektů pro zobrazení tabulky a scrollbaru
        scrollbar = tk.Scrollbar(main_frame)
        scrollbar.pack(side="right", fill="y")
        # Vytvoření tabulky (Treeview) pro zobrazení stavu produktů na skladech
        tree = ttk.Treeview(main_frame, columns=("Sklad ID", "Sklad", "Produkt", "Množství"), show="headings",
                            yscrollcommand=scrollbar.set)
        tree.heading("Sklad ID", text="Sklad ID")
        tree.heading("Sklad", text="Sklad")
        tree.heading("Produkt", text="Produkt")
        tree.heading("Množství", text="Množství")
        tree.column("Sklad ID", width=100, anchor="center")
        tree.column("Sklad", width=200, anchor="center")
        tree.column("Produkt", width=200, anchor="center")
        tree.column("Množství", width=100, anchor="center")
        # Aktualizace tabulky a přidání scrollbaru
        refresh_tree(tree)
        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)
        # Vytvoření rámečku pro tlačítka
        buttons_frame = tk.Frame(main_frame, bg="#B0B0E0")
        buttons_frame.pack(side="top", pady=(10, 0))
        # Tlačítko pro seřazení podle počtu produktů (max)
        sort_by_stock = ttk.Button(buttons_frame, text="Seřadit podle počtu produktů(max)",
                                   command=lambda: refresh_tree(tree, "sklad_produkt.mnozstvi DESC"))
        sort_by_stock.pack(side="left")
        # Tlačítko pro seřazení podle počtu produktů (min)
        sort_by_least_stock = ttk.Button(buttons_frame, text="Seřadit podle počtu produktů (min)",
                                         command=lambda: refresh_tree(tree, "sklad_produkt.mnozstvi ASC"))
        sort_by_least_stock.pack(side="left", padx=(10, 0))
        # Tlačítko pro seřazení podle ID skladů
        sort_by_id = ttk.Button(buttons_frame, text="Seřadit podle ID skladů",
                                command=lambda: refresh_tree(tree, "sklad.id"))
        sort_by_id.pack(side="left", padx=(10, 0))
        # Vytvoření rámečku pro tlačítko Zavřít
        close_button_frame = tk.Frame(main_frame, bg="#B0B0E0")
        close_button_frame.pack(side="bottom", pady=(10, 0))
        # Tlačítko pro zavření okna se stavem produktů na skladech
        close_button = ttk.Button(close_button_frame, text="Zavřít", command=product_stock_win.destroy)
        close_button.pack(side="bottom", pady=(10, 0))
        # Aktualizace a nastavení centrování okna
        product_stock_win.update_idletasks()
        width, height = product_stock_win.winfo_width(), product_stock_win.winfo_height()
        x = (product_stock_win.winfo_screenwidth() // 2) - (width // 2)
        y = (product_stock_win.winfo_screenheight() // 2) - (height // 2)
        product_stock_win.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def display_product_stock_status_in_stores():
        """
        Statická metoda pro zobrazení stavu produktů v obchodech.
        """
        def fetch_products_in_stores(order_by=None):
            """
            Funkce pro načtení stavu produktů v obchodech z databáze.
            :param order_by: sloupec pro řazení výsledků (volitelné)
            :return: seznam n-tic s údaji o stavu produktů v obchodech
            """
            try:
                query = """
                SELECT obchod.id AS obchod_id, obchod.nazev AS obchod_nazev, produkt.id AS produkt_id, produkt.nazev AS 
                produkt_nazev, obchod_produkt.mnozstvi AS mnozstvi
                FROM obchod_produkt
                JOIN obchod ON obchod_produkt.obchod_id = obchod.id
                JOIN produkt ON obchod_produkt.produkt_id = produkt.id
                """

                if order_by:
                    query += f"ORDER BY {order_by}"

                db_connection = DatabaseConnection().connect_to_database()
                cursor = db_connection.cursor()
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se načíst data ze serveru: {str(e)}")

        def update_tree(tree, order_by=None):
            """
            Funkce pro aktualizaci obsahu stromu s daty produktů v obchodech.
            :param tree: objekt Ttk.Treeview reprezentující tabulku
            :param order_by: sloupec pro řazení výsledků (volitelné)
            """
            tree.delete(*tree.get_children())
            data = fetch_products_in_stores(order_by)
            for item in data:
                tree.insert("", "end", values=item)

        def sort_by_store_id():
            update_tree(tree, "obchod_id")

        def sort_by_product_count():
            update_tree(tree, "mnozstvi DESC")

        store_product_status_win = tk.Toplevel()
        store_product_status_win.title("Stav produktů v obchodech")
        store_product_status_win.configure(bg="#B0B0E0")

        width = 800
        height = 600
        screen_width = store_product_status_win.winfo_screenwidth()
        screen_height = store_product_status_win.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        store_product_status_win.geometry("%dx%d+%d+%d" % (width, height, x, y))
        # Vytvoření hlavního rámečku pro umístění ostatních prvků
        main_frame = tk.Frame(store_product_status_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoření stromového zobrazení se sloupci a nastavením vlastností
        tree = ttk.Treeview(main_frame, columns=("Obchod ID", "Obchod", "Produkt ID", "Produkt", "Množství"), show="headings")
        tree.heading("Obchod ID", text="Obchod ID")
        tree.heading("Obchod", text="Obchod")
        tree.heading("Produkt ID", text="Produkt ID")
        tree.heading("Produkt", text="Produkt")
        tree.heading("Množství", text="Množství")
        tree.column("Obchod ID", width=100, anchor="center")
        tree.column("Obchod", width=200, anchor="center")
        tree.column("Produkt ID", width=100, anchor="center")
        tree.column("Produkt", width=200, anchor="center")
        tree.column("Množství", width=100, anchor="center")
        # Aktualizace stromového zobrazení dat z databáze
        update_tree(tree)
        # Umístění stromového zobrazení do hlavního rámečku
        tree.pack(fill=tk.BOTH, expand=True)
        # Vytvoření rámečku pro tlačítka seřazení
        sort_buttons_frame = tk.Frame(main_frame, bg="#B0B0E0")
        sort_buttons_frame.pack(pady=(10, 0))
        # Vytvoření tlačítek pro seřazení a jejich umístění do rámu pro tlačítka
        sort_by_store_id_button = ttk.Button(sort_buttons_frame, text="Seřadit podle ID obchodu", command=sort_by_store_id)
        sort_by_store_id_button.pack(side=tk.LEFT, padx=(0, 10))

        sort_by_product_count_button = ttk.Button(sort_buttons_frame, text="Seřadit podle počtu produktů", command=sort_by_product_count)
        sort_by_product_count_button.pack(side=tk.LEFT, padx=(0, 10))

        sort_by_min_product_count_button = ttk.Button(sort_buttons_frame, text="Seřadit podle počtu produktů (min)", command=lambda: update_tree(tree, "mnozstvi"))
        sort_by_min_product_count_button.pack(side=tk.LEFT)
        # Vytvoření tlačítka pro zavření okna a jeho umístění do hlavního rámu
        close_button = ttk.Button(main_frame, text="Zavřít", command=store_product_status_win.destroy)
        close_button.pack(pady=(20, 10))
    @staticmethod
    def display_employees():
        """Zobrazí okno se seznamem zaměstnanců.

        Tato metoda zobrazí okno se seznamem zaměstnanců načtených z databáze.
        Umožňuje uživateli seřadit zaměstnance podle ID nebo jména.
        """
        def fetch_employees(order_by=None):
            """Načte zaměstnance z databáze.

                :arg:
                    order_by (str, optional): Sloupec, podle kterého se mají data seřadit.

                :return:
                    list: Seznam zaměstnanců.
                """
            try:
                query = """
                   SELECT id, jmeno, prijmeni
                   FROM zamestnanec
                   """

                if order_by:
                    query += f"ORDER BY {order_by}"

                db_connection = DatabaseConnection().connect_to_database()
                cursor = db_connection.cursor()
                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se načíst data ze serveru: {str(e)}")

        def update_tree(tree, order_by=None):
            """Aktualizuje stromové zobrazení daty o zaměstnancích.

                :arg:
                tree (ttk.Treeview): Stromové zobrazení pro zobrazení zaměstnanců.
                order_by (str, optional): Sloupec, podle kterého se mají data seřadit.
            """
            # Smazání všech položek v tabulce(rozbaluje seznam a předava jako argumenty)
            tree.delete(*tree.get_children())
            # Načtení dat o zaměstnancích a jejich řazení podle zadaného kritéria (pokud je poskytnuto)
            data = fetch_employees(order_by)
            # Vložení načtených dat o zaměstnancích do tabulky
            for item in data:
                tree.insert("", "end", values=item)
        # Vytvoření okna pro zobrazení zaměstnanců
        employees_win = tk.Toplevel()
        employees_win.title("Zaměstnanci")
        employees_win.configure(bg="#B0B0E0")

        screen_width = employees_win.winfo_screenwidth()
        screen_height = employees_win.winfo_screenheight()
        window_width, window_height = 600, 400
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        employees_win.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        # Vytvoření hlavního rámečku pro umístění ostatních prvků
        main_frame = tk.Frame(employees_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoření stromového zobrazení s potřebnými sloupci a nastavením vlastností
        tree = ttk.Treeview(main_frame, columns=("ID", "Jméno", "Příjmení"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Jméno", text="Jméno")
        tree.heading("Příjmení", text="Příjmení")
        tree.column("ID", width=100, anchor="center")
        tree.column("Jméno", width=200, anchor="center")
        tree.column("Příjmení", width=200, anchor="center")
        # Aktualizace stromového zobrazení dat z databáze
        update_tree(tree)
        # Vytvoření posuvníku pro stromové zobrazení
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Umístění stromového zobrazení do hlavního rámečku
        tree.pack(fill=tk.BOTH, expand=True)
        # Vytvoření rámečku pro tlačítka
        buttons_frame = tk.Frame(main_frame, bg="#B0B0E0")
        buttons_frame.pack(pady=(10, 0))
        # Vytvoření tlačítek pro seřazení a jejich umístění do rámečku pro tlačítka
        sort_by_name_button = ttk.Button(buttons_frame, text="Seřadit podle jména",
                                         command=lambda: update_tree(tree, "jmeno"))
        sort_by_name_button.pack(side=tk.LEFT, padx=(0, 10))

        sort_by_id_button = ttk.Button(buttons_frame, text="Seřadit podle ID",
                                       command=lambda: update_tree(tree, "id"))
        sort_by_id_button.pack(side=tk.LEFT)
        # Vytvoření tlačítka pro zavření okna a jeho umístění do hlavního rámečku
        close_button = ttk.Button(main_frame, text="Zavřít", command=employees_win.destroy)
        close_button.pack(pady=(20, 10))

    @staticmethod
    def display_customers():
        """
        Metoda která volá metodu display_customers ze třídy InformationWin
        :return:
        """
        InformationWin.display_customers()