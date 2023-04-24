import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from conn import DatabaseConnection
class InformationWin:
    @staticmethod
    def display_customers():
        """
        Funkce pro zobrazení okna se seznamem zákazníků.
        """
        def fetch_customers(order_by=None):
            """
            Funkce pro načítání zákazníků z databáze.
            """
            try:
                db_connection = DatabaseConnection().connect_to_database()
                cursor = db_connection.cursor()

                query = """
                SELECT id, jmeno, prijmeni, email, vernostni_body
                FROM zakaznik
                """

                if order_by:
                    query += f"ORDER BY {order_by}"

                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se načíst data ze serveru: {str(e)}")

        def refresh_tree(tree, order_by=None):
            """
            Funkce pro obnovení obsahu stromu s daty zákazníků.
            """
            tree.delete(*tree.get_children())
            data = fetch_customers(order_by)
            for item in data:
                tree.insert("", "end", values=item)

        # Vytvoření okna pro zobrazení zákazníků
        customers_win = tk.Toplevel()
        customers_win.title("Zákazníci")
        customers_win.configure(bg="#B0B0E0")
        customers_win.geometry("800x600")
        # Vytvoření hlavního rámu v okně
        main_frame = tk.Frame(customers_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoření rámečku pro zobrazení obsahu
        content_frame = tk.Frame(main_frame, bg="#B0B0E0")
        content_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoření scrollbaru
        tree_scrollbar = ttk.Scrollbar(content_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Vytvoření stromového zobrazení pro data zákazníků
        tree = ttk.Treeview(content_frame, columns=("ID", "Jméno", "Příjmení", "E-mail", "Věrnostní body"),
                            show="headings", yscrollcommand=tree_scrollbar.set)
        tree.heading("ID", text="ID")
        tree.heading("Jméno", text="Jméno")
        tree.heading("Příjmení", text="Příjmení")
        tree.heading("E-mail", text="E-mail")
        tree.heading("Věrnostní body", text="Věrnostní body")
        tree.column("ID", width=50, anchor="center")
        tree.column("Jméno", width=150, anchor="center")
        tree.column("Příjmení", width=150, anchor="center")
        tree.column("E-mail", width=250, anchor="center")
        tree.column("Věrnostní body", width=150, anchor="center")
        # Načtení dat do stromového zobrazení
        refresh_tree(tree)
        tree_scrollbar.config(command=tree.yview)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Vytvoření rámečku pro tlačítka
        buttons_frame = tk.Frame(main_frame, bg="#B0B0E0")
        buttons_frame.pack(side="top", pady=(10, 0))
        # Vytvoření tlačítek pro řazení dat
        sort_by_id = ttk.Button(buttons_frame, text="Seřadit podle ID",
                                command=lambda: refresh_tree(tree, "id"))
        sort_by_id.pack(side="left", padx=(10, 0))

        sort_by_jmeno = ttk.Button(buttons_frame, text="Seřadit podle jména",
                                   command=lambda: refresh_tree(tree, "jmeno"))
        sort_by_jmeno.pack(side="left", padx=(10, 0))

        sort_by_prijmeni = ttk.Button(buttons_frame, text="Seřadit podle příjmení",
                                      command=lambda: refresh_tree(tree, "prijmeni"))
        sort_by_prijmeni.pack(side="left", padx=(10, 0))
        sort_by_vernost_nejmene = ttk.Button(buttons_frame, text="Seřadit podle bodů(min) ",
                                             command=lambda: refresh_tree(tree, "vernostni_body"))
        sort_by_vernost_nejmene.pack(side="left", padx=(10, 0))
        sort_by_vernost_nejvice = ttk.Button(buttons_frame, text="Seřadit podle bodů (max)",
                                             command=lambda: refresh_tree(tree, "vernostni_body DESC"))
        sort_by_vernost_nejvice.pack(side="left", padx=(10, 0))
        # Vytvoření tlačítka pro zavření okna
        close_button = ttk.Button(main_frame, text="Zavřít", command=customers_win.destroy)
        close_button.pack(pady=(10, 0), side="bottom", anchor="s")
        # Nastavení pozice okna na střed obrazovky
        customers_win.update_idletasks()
        width, height = customers_win.winfo_width(), customers_win.winfo_height()
        x = (customers_win.winfo_screenwidth() // 2) - (width // 2)
        y = (customers_win.winfo_screenheight() // 2) - (height // 2)
        customers_win.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def display_orders():
        """
        Funkce pro zobrazení okna se seznamem objednávek.
        """
        def fetch_orders(order_by=None):
            """
            Funkce pro načítání objednávek z databáze.

            :param order_by: specifikuje, podle jakého sloupce budou objednávky seřazeny (pokud je uvedeno).
            :return: seznam objednávek z databáze, seřazených podle sloupce uvedeného v parametru order_by (pokud je uveden), jinak seřazených podle data vytvoření objednávky.
            """
            try:
                db_connection = DatabaseConnection().connect_to_database()
                cursor = db_connection.cursor()

                query = """
                SELECT o.id, z.jmeno, z.prijmeni, p.nazev, op.mnozstvi, o.stav
                FROM objednavka o
                JOIN zakaznik z ON o.zakaznik_id = z.id
                JOIN objednavka_produkt op ON o.id = op.objednavka_id
                JOIN produkt p ON op.produkt_id = p.id
                """

                if order_by:
                    query += f"ORDER BY {order_by}"

                cursor.execute(query)
                return cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodařilo se načíst data ze serveru: {str(e)}")

        def refresh_tree(tree, order_by=None):
            """
            Funkce pro obnovení obsahu stromu s daty objednávek.
            :param tree: instance stromového zobrazení (Treeview), které má být aktualizováno
            :param order_by: volitelný řetězec, který určuje sloupec, podle kterého se mají data řadit;
             pokud není poskytnut, data nebudou řazena
            """
            # Odstranění všech řádků ze stromového zobrazení (tree)
            tree.delete(*tree.get_children())
            # Načtení dat objednávek z databáze podle zvoleného řazení (order_by)
            data = fetch_orders(order_by)
            # Procházení načtených dat a vložení každého záznamu (item) do stromového zobrazení (tree)
            for item in data:
                tree.insert("", "end", values=item)


        orders_win = tk.Toplevel()
        orders_win.title("Objednávky")
        orders_win.configure(bg="#B0B0E0")
        orders_win.geometry("1000x600")
        # Vytvoření okna pro zobrazení objednávek
        main_frame = tk.Frame(orders_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoření rámečku pro zobrazení obsahu
        content_frame = tk.Frame(main_frame, bg="#B0B0E0")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tree_scrollbar = ttk.Scrollbar(content_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Vytvoření stromového zobrazení pro data objednávek
        tree = ttk.Treeview(content_frame, columns=("ID", "Jméno", "Příjmení", "Produkt", "Množství", "Stav"),
                            show="headings", yscrollcommand=tree_scrollbar.set)
        tree.heading("ID", text="ID")
        tree.heading("Jméno", text="Jméno")
        tree.heading("Příjmení", text="Příjmení")
        tree.heading("Produkt", text="Produkt")
        tree.heading("Množství", text="Množství")
        tree.heading("Stav", text="Stav")
        tree.column("ID", width=50, anchor="center")
        tree.column("Jméno", width=150, anchor="center")
        tree.column("Příjmení", width=150, anchor="center")
        tree.column("Produkt", width=250, anchor="center")
        tree.column("Množství", width=150, anchor="center")
        tree.column("Stav", width=150, anchor="center")
        # Načtení dat do stromového zobrazení
        refresh_tree(tree)
        tree_scrollbar.config(command=tree.yview)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Vytvoření rámu pro tlačítka
        buttons_frame = tk.Frame(main_frame, bg="#B0B0E0")
        buttons_frame.pack(side="top", pady=(10, 0))
        # Vytvoření tlačítek pro řazení dat
        sort_by_id = ttk.Button(buttons_frame, text="Seřadit podle ID",
                                command=lambda: refresh_tree(tree, "o.id"))
        sort_by_id.pack(side="left", padx=(10, 0))

        sort_by_zakaznik = ttk.Button(buttons_frame, text="Seřadit podle zákazníka",
                                      command=lambda: refresh_tree(tree, "z.jmeno, z.prijmeni"))
        sort_by_zakaznik.pack(side="left", padx=(10, 0))

        sort_by_produkt = ttk.Button(buttons_frame, text="Seřadit podle produktu",
                                     command=lambda: refresh_tree(tree, "p.nazev"))
        sort_by_produkt.pack(side="left", padx=(10, 0))
        # Vytvoření tlačítka pro zavření okna
        close_button = ttk.Button(main_frame, text="Zavřít", command=orders_win.destroy)
        close_button.pack(pady=(10, 0), side="bottom", anchor="s")
        # Nastavení pozice okna na střed obrazovky
        orders_win.update_idletasks()
        width, height = orders_win.winfo_width(), orders_win.winfo_height()
        x = (orders_win.winfo_screenwidth() // 2) - (width // 2)
        y = (orders_win.winfo_screenheight() // 2) - (height // 2)
        orders_win.geometry(f"{width}x{height}+{x}+{y}")
