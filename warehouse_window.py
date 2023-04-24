import tkinter as tk
from tkinter import ttk
from conn import DatabaseConnection
from tkinter import messagebox
import mysql.connector


class WarehouseWindows:
    """
    Obsahuje metody pro vytváření oken a manipulaci s daty v databázi
    """
    @staticmethod
    def show_warehouse_management(parent):
        """
        Zobrazí hlavní nabídku pro správu skladů a dodavatelů.

        :param
        parent (tkinter.Frame): Rám, ve kterém se zobrazí tlačítka.
        """
        for widget in parent.winfo_children():
            widget.destroy()

        edit_warehouse_button = ttk.Button(parent, text="Úprava skladů", command=WarehouseWindows.edit_warehouse_window)
        edit_warehouse_button.pack(pady=(20, 10))

        add_warehouse_button = ttk.Button(parent, text="Přidání skladů", command=WarehouseWindows.add_warehouse_window)
        add_warehouse_button.pack(pady=(10, 10))

        delete_warehouse_button = ttk.Button(parent, text="Smazání skladů",
                                             command=WarehouseWindows.delete_warehouse_window)
        delete_warehouse_button.pack(pady=(10, 10))

        show_warehouses_button = ttk.Button(parent, text="Zobrazit sklady",
                                            command=WarehouseWindows.show_warehouses)
        show_warehouses_button.pack(pady=(10, 10))

        add_supplier_button = ttk.Button(parent, text="Přidat dodavatele ke skladu",
                                         command=lambda: WarehouseWindows.add_supplier_to_warehouse())
        add_supplier_button.pack(pady=(10, 10))

    @staticmethod
    def set_window_geometry(window, width, height):
        """
        Nastaví okno do prostřed obrazovky

        :param
        window (tkinter.Toplevel): Okno které se centruje.
        width (int): Šířka okna.
        height (int): Výška okna.
        """
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    @staticmethod
    def edit_warehouse_window():
        """
        Otevře okno pro úpravu skladů, kde uživatel může změnit název a adresu skladu.
        """
        # Vytvoření okna
        edit_warehouse_win = tk.Toplevel()
        edit_warehouse_win.title("Úprava skladů")
        WarehouseWindows.set_window_geometry(edit_warehouse_win, 400, 250)
        # Vytvoření rámečku
        main_frame = tk.Frame(edit_warehouse_win, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.config(bg="#B0B0E0")
        # Připojení k databázi
        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()
        # Načtení názvů skladů z databáze
        cursor.execute("SELECT nazev FROM sklad")
        warehouses = [row[0] for row in cursor.fetchall()]
        # Vytvoření labelu a comboboxu pro výběr skladu
        warehouse_label = ttk.Label(main_frame, text="Vyberte sklad:")
        warehouse_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        warehouse_label.config(background="#B0B0E0")
        warehouses_var = tk.StringVar()
        warehouse_combobox = ttk.Combobox(main_frame, textvariable=warehouses_var, values=warehouses)
        warehouse_combobox.grid(row=0, column=1, padx=20, pady=10)
        warehouse_combobox.config(background="#B0B0E0")
        # Vytvoření labelu a vstupního pole pro nový název skladu
        new_name_label = ttk.Label(main_frame, text="Nový název:")
        new_name_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        new_name_label.config(background="#B0B0E0")
        new_name_entry = ttk.Entry(main_frame)
        new_name_entry.grid(row=1, column=1, padx=10, pady=10)
        # Vytvoření labelu a vstupního pole pro novou adresu skladu
        new_address_label = ttk.Label(main_frame, text="Nová adresa:")
        new_address_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        new_address_label.config(background="#B0B0E0")
        new_address_entry = ttk.Entry(main_frame)
        new_address_entry.grid(row=2, column=1, padx=10, pady=10)

        def save_changes():
            """
            Ukládá změny provedené uživatelem v okně pro úpravu skladů.

            Získá nový název a adresu ze vstupních polí a aktualizuje sklad v databázi.
            Pokud nastane chyba, zobrazí se chybová zpráva.
            """
            # Získání nového názvu a adresy ze vstupních polí
            new_name = new_name_entry.get()
            new_address = new_address_entry.get()
            # Ověření, zda jsou název a adresa dostatečně dlouhé
            if len(new_name) < 3 or len(new_address) < 3:
                messagebox.showwarning("Varování", "Zadejte alespoň 3 znaky pro název a adresu skladu.")
                return
            # Získání názvu vybraného skladu
            selected_warehouse_name = warehouses_var.get()
            if selected_warehouse_name == "":
                messagebox.showwarning("Varování", "Vyberte sklad, který chcete upravit.")
                return
            # Získání ID vybraného skladu z databáze
            cursor.execute("SELECT id FROM sklad WHERE nazev = %s", (selected_warehouse_name,))
            selected_warehouse_id = cursor.fetchone()[0]
            # Pokus o aktualizaci skladu v databázi
            try:
                update_query = """UPDATE sklad
                                         SET nazev = %s, adresa = %s
                                         WHERE id = %s"""
                cursor.execute(update_query, (new_name, new_address, selected_warehouse_id))
                db_connection.commit()
                messagebox.showinfo("Informace", "Sklad úspěšně upraven.")
                edit_warehouse_win.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Chyba", f"Nastala chyba při úpravě skladu: {e}")

        # Tlačítko pro uložení změn
        save_button = ttk.Button(main_frame, text="Uložit změny", command=save_changes)
        save_button.grid(row=3, columnspan=2, padx=10, pady=20)

        edit_warehouse_win.mainloop()

    @staticmethod
    def add_warehouse_window():
        """
        Otevře okno pro přidání skladu
        """
        # Vytvoření okna
        add_warehouse_win = tk.Toplevel()
        add_warehouse_win.title("Přidání skladů")
        WarehouseWindows.set_window_geometry(add_warehouse_win, 400, 250)
        add_warehouse_win.config(bg="#B0B0E0")
        # Vytvoření ohraničení rámu
        main_frame = tk.Frame(add_warehouse_win, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.config(background="#B0B0E0")
        # Vytvoření labelu a vstupního pole pro název skladu
        name_label = ttk.Label(main_frame, text="Název skladu:")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_label.config(background="#B0B0E0")
        name_entry = ttk.Entry(main_frame)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        # Vytvoření labelu a vstupního pole pro adresu skladu
        address_label = ttk.Label(main_frame, text="Adresa skladu:")
        address_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        address_label.config(background="#B0B0E0")
        address_entry = ttk.Entry(main_frame)
        address_entry.grid(row=1, column=1, padx=10, pady=10)

        def add_warehouse():
            # Načtení názvu a adresy z vstupních polí
            name = name_entry.get()
            address = address_entry.get()
            # Ověření, že název a adresa má aspoň 3 charaktery
            if len(name) < 3 or len(address) < 3:
                messagebox.showwarning("Varování", "Zadejte alespoň 3 znaky pro název a adresu skladu.")
                return
            # Přidávání nového skladu do databáze s použitím parametrizovaného dotazu
            try:
                conn = DatabaseConnection().connect_to_database()
                cursor = conn.cursor()
                insert_query = "INSERT INTO sklad (nazev, adresa) VALUES (%s, %s)"
                insert_values = (name, address)
                # Spuštění dotazu s n-ticí hodnot jako parametry
                cursor.execute(insert_query, insert_values)
                conn.commit()
                conn.close()
                messagebox.showinfo("Informace", "Sklad úspěšně přidán.")
                add_warehouse_win.destroy()
            except mysql.connector.Error as e:
                # Zobrazení chybového messageboxu s popisem chyby
                messagebox.showerror("Chyba", f"Nastala chyba při přidávání skladu: {e}")
        # Vytvoření tlačítka pro přidání skladu
        add_button = ttk.Button(main_frame, text="Přidat sklad", command=add_warehouse)
        add_button.grid(row=2, columnspan=2, padx=10, pady=20)
        # Spuštění hlavní smyčky okna
        add_warehouse_win.mainloop()

    @staticmethod
    def delete_warehouse_window():
        """
        Vytváří okno pro mazání skladů

        """
        # Vytvoření okna pro mazání skladů
        delete_warehouse_win = tk.Toplevel()
        delete_warehouse_win.title("Smazání skladů")
        WarehouseWindows.set_window_geometry(delete_warehouse_win, 400, 250)
        delete_warehouse_win.config(background="#B0B0E0")
        # Vytvoření rámečku
        main_frame = tk.Frame(delete_warehouse_win, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.config(background="#B0B0E0")
        # Připojení k databázi
        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()
        # Načtení skladů z databáze kromě prvního
        cursor.execute("SELECT id, nazev FROM sklad WHERE id != 1")
        warehouses = [(row[0], row[1]) for row in cursor.fetchall()]
        # Vytvoření popisku a rolovacího seznamu pro výběr skladu
        warehouse_label = ttk.Label(main_frame, text="Vyberte sklad ke smazání:")
        warehouse_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        warehouse_label.config(background="#B0B0E0")
        warehouses_var = tk.IntVar()
        warehouse_combobox = ttk.Combobox(main_frame, textvariable=warehouses_var, values=[w[1] for w in warehouses],
                                          state="readonly")
        warehouse_combobox.grid(row=0, column=1, padx=20, pady=10)

        def delete_warehouse():
            """
            Funkce pro mazaní skladů

            """
            # Získání indexu a ID vybraného skladu
            selected_warehouse_index = warehouse_combobox.current()

            if selected_warehouse_index == -1:
                messagebox.showwarning("Varování", "Vyberte sklad, který chcete smazat.")
                return

            selected_warehouse_id, selected_warehouse_name = warehouses[selected_warehouse_index]
            # Potvrzení smazání skladů
            confirmation = messagebox.askyesno("Potvrzení", f"Opravdu chcete smazat sklad '{selected_warehouse_name}'?")
            if not confirmation:
                return
            # Přesun produktů ze skladu do prvního skladu
            try:
                conn = DatabaseConnection().connect_to_database()
                cursor = conn.cursor()
                transfer_query = """
                    INSERT INTO sklad_produkt (sklad_id, produkt_id, mnozstvi)
                    SELECT 1, sp.produkt_id, sp.mnozstvi
                    FROM sklad_produkt AS sp
                    WHERE sp.sklad_id = %s
                    ON DUPLICATE KEY UPDATE mnozstvi = sklad_produkt.mnozstvi + VALUES(mnozstvi)
                """
                cursor.execute(transfer_query, (selected_warehouse_id,))
                conn.commit()
            except mysql.connector.Error as e:
                messagebox.showerror("Chyba", f"Nastala chyba při přesouvání produktů ze skladu: {e}")
                return
            # Smazání produktů ze skladu
            try:
                delete_products_query = "DELETE FROM sklad_produkt WHERE sklad_id = %s"
                cursor.execute(delete_products_query, (selected_warehouse_id,))
                conn.commit()
            except mysql.connector.Error as e:
                messagebox.showerror("Chyba", f"Nastala chyba při mazání produktů ze skladu: {e}")
                return
            # Smazání skladu
            try:
                delete_query = "DELETE FROM sklad WHERE id = %s"
                cursor.execute(delete_query, (selected_warehouse_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Informace", "Sklad úspěšně smazán.")
                delete_warehouse_win.destroy()
            except mysql.connector.Error as e:
                messagebox.showerror("Chyba", f"Nastala chyba při mazání skladu: {e}")

        # Vytvoření tlačítka pro smazání skladu
        delete_warehouse_button = ttk.Button(main_frame, text="Smazat sklad", command=delete_warehouse)
        delete_warehouse_button.grid(row=1, columnspan=2, pady=20)


    @staticmethod
    def show_warehouses():
        # Definuje funkci pro zavření okna se seznamem skladů
        def close_warehouses_window():
            warehouses_win.destroy()

        # Vytvoří okno se seznamem skladů
        warehouses_win = tk.Toplevel()
        warehouses_win.title("Sklady")
        WarehouseWindows.set_window_geometry(warehouses_win, 800, 600)
        warehouses_win.config(background="#B0B0E0")
        # Vytvoří hlavní rámeček okna
        main_frame = tk.Frame(warehouses_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoří rámeček pro obsah
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoří scrollbar
        tree_scrollbar = ttk.Scrollbar(content_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Připojí se k databázi a načte data o skladech
        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM sklad")
        warehouses = cursor.fetchall()
        # Nastaví styl Treeview widgetu
        style = ttk.Style()
        style.configure("Custom.Treeview", foreground="black", rowheight=25
                         )
        style.configure("Custom.Treeview.Heading", font=("Helvetica", 12), background="#B0B0E0", foreground="black")
        style.map("Custom.Treeview.Heading", background=[("active", "#C0C0E0")])
        # Vytvoří Treeview widget pro zobrazení skladů
        tree = ttk.Treeview(content_frame, columns=("id", "nazev", "adresa"), show="headings", style="Custom.Treeview",
                            yscrollcommand=tree_scrollbar.set)
        tree.column("id", width=50, anchor="center")
        tree.column("nazev", width=250, anchor="center")
        tree.column("adresa", width=400, anchor="center")
        tree.heading("id", text="ID")
        tree.heading("nazev", text="Název")
        tree.heading("adresa", text="Adresa")
        # Naplní Treeview widget daty o skladech
        for warehouse in warehouses:
            tree.insert("", "end", values=(warehouse[0], warehouse[1], warehouse[2]))
        # Umístí Treeview widget a nastaví jeho scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=tree.yview)
        # Vytvoří tlačítko pro zavření okna se seznamem skladů
        close_button = ttk.Button(main_frame, text="Zavřít", command=close_warehouses_window)
        close_button.pack(pady=(10, 20), side="bottom", anchor="e")

    @staticmethod
    def add_supplier_to_warehouse():

        def submit_supplier_warehouse():
            """
            Funkce pro zpracování odeslání vybraného dodavatele a skladu

            """
            # Přiřazení dodavatele ke skladu
            selected_warehouse_name = warehouse_var.get()
            selected_supplier_name = supplier_var.get()
            if selected_warehouse_name and selected_supplier_name:
                try:
                    selected_warehouse_id = warehouse_name_to_id[selected_warehouse_name]
                    selected_supplier_id = supplier_name_to_id[selected_supplier_name]

                    db_connection = DatabaseConnection().connect_to_database()
                    cursor = db_connection.cursor()
                    cursor.execute("INSERT INTO dodavatel_sklad (dodavatel_id, sklad_id) VALUES (%s, %s)",
                                   (selected_supplier_id, selected_warehouse_id))
                    db_connection.commit()
                    db_connection.close()
                    add_supplier_win.destroy()
                    messagebox.showinfo("Úspěch", "Dodavatel byl úspěšně přidán ke skladu.")
                except Exception as e:
                    messagebox.showerror("Chyba", f"Nepodařilo se přidat dodavatele ke skladu: {str(e)}")

        # Vytvoření okna pro přidání dodavatele ke skladu
        add_supplier_win = tk.Toplevel()
        add_supplier_win.title("Přidat dodavatele ke skladu")
        add_supplier_win.configure(bg="#B0B0E0")
        # Nastavení velikosti a pozice okna
        add_supplier_win.update_idletasks()
        screen_width = add_supplier_win.winfo_screenwidth()
        screen_height = add_supplier_win.winfo_screenheight()
        window_width = 400
        window_height = 300
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        add_supplier_win.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        # Vytvoření hlavního rámečku
        main_frame = tk.Frame(add_supplier_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Připojení k databázi a získání skladů a dodavatelů
        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()

        cursor.execute("SELECT id, nazev FROM sklad")
        warehouses = cursor.fetchall()

        cursor.execute("SELECT id, nazev FROM dodavatel")
        suppliers = cursor.fetchall()
        # Převod názvů skladů a dodavatelů na jejich ID
        warehouse_name_to_id = {warehouse[1]: warehouse[0] for warehouse in warehouses}
        supplier_name_to_id = {supplier[1]: supplier[0] for supplier in suppliers}
        # Vytvoření možností pro výběr skladu a dodavatele
        warehouse_options = list(warehouse_name_to_id.keys())
        supplier_options = list(supplier_name_to_id.keys())
        # Vytvoření proměnných pro uložení vybraných hodnot
        warehouse_var = tk.StringVar()
        supplier_var = tk.StringVar()
        # rozbalovacího menu pro výběr skladu
        warehouse_label = tk.Label(main_frame, text="Sklad:", bg="#B0B0E0")
        warehouse_label.pack()
        warehouse_dropdown = ttk.Combobox(main_frame, textvariable=warehouse_var, values=warehouse_options)
        warehouse_dropdown.pack(pady=(0, 10))
        # Vytvoření popisku a rozbalovacího menu pro výběr dodavatele
        supplier_label = tk.Label(main_frame, text="Dodavatel:", bg="#B0B0E0")
        supplier_label.pack()
        supplier_dropdown = ttk.Combobox(main_frame, textvariable=supplier_var, values=supplier_options)
        supplier_dropdown.pack(pady=(0, 10))
        # Vytvoření tlačítka pro odeslání vybraných hodnot
        submit_button = ttk.Button(main_frame, text="Potvrdit", command=submit_supplier_warehouse)
        submit_button.pack(pady=(10, 20))
