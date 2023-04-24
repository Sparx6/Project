import tkinter as tk
from tkinter import ttk
from conn import DatabaseConnection
from tkinter import messagebox

class SupplierManagement:
    """
    Třída pro správu dodavatelů.
    """


    @staticmethod
    def show_supplier_management(content_frame):
        """
        Zobrazit hlavní okno správy dodavatelů.

        :arg:
        content_frame (tk.Frame): Frame, do kterého budou vloženy widgety.
        """
        # Odstranit všechny widgety v content_frame
        for widget in content_frame.winfo_children():
            widget.destroy()
        # Vytvoření tlačítek
        edit_button = ttk.Button(content_frame, text="Upravit dodavatele",
                                 command=SupplierManagement.show_edit_supplier_window)
        edit_button.pack(pady=(10, 10))

        add_button = ttk.Button(content_frame, text="Přidat dodavatele",
                                command=SupplierManagement.show_add_supplier_window)
        add_button.pack(pady=(10, 10))

        delete_button = ttk.Button(content_frame, text="Smazat dodavatele",
                                   command=SupplierManagement.delete_supplier)
        delete_button.pack(pady=(10, 10))

        show_button = ttk.Button(content_frame, text="Zobrazit dodavatele",
                                 command=SupplierManagement.show_suppliers)
        show_button.pack(pady=(10, 10))

        add_supplier_product_button = ttk.Button(content_frame, text="Přidat produkt k dodavateli",
                                                 command=SupplierManagement.show_add_supplier_product_window)
        add_supplier_product_button.pack(pady=(10, 0))



    @staticmethod
    def show_edit_supplier_window():
        """
        Zobrazení okna pro úpravu dodavatele.
        """
        def update_supplier():
            """
            Aktualizuje dodavatele v databázi.
            """
            # Získání hodnot z formuláře
            name = entry_vars["Název"].get()
            address = entry_vars["Adresa"].get()
            phone = entry_vars["Tel. Číslo"].get()
            email = entry_vars["E-mail"].get()
            item_type = entry_vars["Druh zboží"].get()
            # Kontrola zadávaných hodnot do formuláře
            if len(name) < 3 or len(address) < 3 or len(item_type) < 3:
                tk.messagebox.showerror("Chyba", "Název, adresa a druh zboží musí obsahovat alespoň 3 znaky.")
                return

            if len(phone) < 9:
                tk.messagebox.showerror("Chyba", "Telefonní číslo musí obsahovat alespoň 9 znaků.")
                return

            if "@" not in email or "." not in email:
                tk.messagebox.showerror("Chyba", "E-mailová adresa není platná.")
                return
            # Aktualizace dodavatele v databázi
            selected_supplier = int(supplier_var.get().split(" - ")[0])
            cursor = db_connection.cursor()
            update_query = "UPDATE dodavatel SET nazev = %s, adresa = %s, kontakt_telefon = %s, kontakt_email = %s," \
                           " druh_zbozi = %s WHERE id = %s"
            cursor.execute(update_query, (name, address, phone, email, item_type, selected_supplier))
            db_connection.commit()
            # Aktualizace výběru dodavatelů
            cursor.execute("SELECT * FROM dodavatel")
            suppliers = cursor.fetchall()
            supplier_dropdown["values"] = [f"{s[0]} - {s[1]}" for s in suppliers]
            supplier_dropdown.set(f"{selected_supplier} - {name}")
            messagebox.showinfo("Úspěch", "Dodavatel úspěšně aktualizován.")

        # Vytvoření okna pro úpravu dodavatele
        edit_supplier_win = tk.Toplevel()
        edit_supplier_win.title("Upravit dodavatele")
        edit_supplier_win.geometry("500x400")
        edit_supplier_win.config(background="#B0B0E0")
        # Vycentrování okna doprostřed obrazovky
        window_width = 500
        window_height = 400
        screen_width = edit_supplier_win.winfo_screenwidth()
        screen_height = edit_supplier_win.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        edit_supplier_win.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # Vytvoření hlavního framu
        main_frame = tk.Frame(edit_supplier_win, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.config(background="#B0B0E0")
        # Připojení k databázi
        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM dodavatel")
        suppliers = cursor.fetchall()
        # Vytvoření výběru dodavatelů
        supplier_var = tk.StringVar()
        supplier_dropdown = ttk.Combobox(main_frame, textvariable=supplier_var)
        supplier_dropdown["values"] = [f"{s[0]} - {s[1]}" for s in suppliers]
        supplier_dropdown.current(0)
        supplier_dropdown.pack(pady=(10, 20))
        # Vytvoření formuláře
        form_frame = tk.Frame(main_frame, background="#B0B0E0")
        form_frame.pack()

        fields = ["Název", "Adresa", "Tel. Číslo", "E-mail", "Druh zboží"]
        entry_vars = {field: tk.StringVar() for field in fields}
        # Vytvoření polí formuláře
        for idx, field in enumerate(fields):
            label = ttk.Label(form_frame, text=f"{field}:", background="#B0B0E0")
            label.grid(row=idx, column=0, sticky=tk.W, pady=5)

            entry = ttk.Entry(form_frame, textvariable=entry_vars[field])
            entry.grid(row=idx, column=1, sticky=tk.W, pady=5)
        # Vytvoření tlačítka pro aktualizaci dodavatele
        update_button = ttk.Button(main_frame, text="Upravit dodavatele", command=update_supplier)
        update_button.pack(pady=(10, 20))

    @staticmethod
    def show_add_supplier_window():
        """
        Zobrazení okna pro přidání nového dodavatele.

        """
        def add_supplier():
            """
            Přidá nového dodavatele do databáze na základě vstupů uživatele.
            """
            values = {field: var.get().strip() for field, var in entry_vars.items()}

            for field, value in values.items():
                if field == "Tel. Číslo" and len(value) < 9:
                    messagebox.showerror("Chyba", f"Telefonní číslo musí mít alespoň 9 znaků.")
                    return
                if len(value) < 3:
                    messagebox.showerror("Chyba", f"Pole {field} musí mít alespoň 3 znaky.")
                    return

            db_connection = DatabaseConnection().connect_to_database()
            cursor = db_connection.cursor()

            insert_query = f"""
            INSERT INTO dodavatel (nazev, adresa, kontakt_telefon, kontakt_email, druh_zbozi)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, tuple(values.values()))
            db_connection.commit()

            messagebox.showinfo("Úspěch", "Dodavatel byl úspěšně přidán.")

        # Vytvoření okna pro přidání dodavatele
        add_supplier_win = tk.Toplevel()
        add_supplier_win.title("Přidat dodavatele")
        add_supplier_win.geometry("500x400")
        add_supplier_win.config(background="#B0B0E0")
        # Centrování okna uprostřed obrazovky
        window_width = 500
        window_height = 400
        screen_width = add_supplier_win.winfo_screenwidth()
        screen_height = add_supplier_win.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        add_supplier_win.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # Vytvoření hlavního framu
        main_frame = tk.Frame(add_supplier_win, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.config(background="#B0B0E0")
        # Vytvoření formuláře
        form_frame = tk.Frame(main_frame, background="#B0B0E0")
        form_frame.pack()
        # Vytvoření seznamu polí formuláře
        fields = ["Název", "Adresa", "Tel. Číslo", "E-mail", "Druh zboží"]
        entry_vars = {field: tk.StringVar() for field in fields}
        # Iterace přes seznam 'fields' a získání indexu a hodnoty každého prvku
        for idx, field in enumerate(fields):
            # Vytvoření a umístění popisku pro aktuální pole formuláře
            label = ttk.Label(form_frame, text=f"{field}:", background="#B0B0E0")
            label.grid(row=idx, column=0, sticky=tk.W, pady=5)
            # Vytvoření a umístění vstupního pole pro aktuální pole formuláře
            entry = ttk.Entry(form_frame, textvariable=entry_vars[field])
            entry.grid(row=idx, column=1, sticky=tk.W, pady=5)
        # Vytvoření a umístění tlačítka Přidat dodavatele
        add_button = ttk.Button(main_frame, text="Přidat dodavatele", command=add_supplier)
        add_button.pack(pady=(10, 20))

    @staticmethod
    def delete_supplier():
        """
        Metoda pro smazání vybraného dodavatele z databáze.
        """
        def delete_selected_supplier():
            """
            Metoda pro smazání vybraného dodavatele z databáze a aktualizaci rozbalovací nabídky.
            """

            selected_supplier = int(supplier_var.get().split(" - ")[0])

            cursor = db_connection.cursor()
            delete_query = "DELETE FROM dodavatel WHERE id = %s"
            cursor.execute(delete_query, (selected_supplier,))
            db_connection.commit()

            supplier_dropdown["values"] = [s for s in supplier_dropdown["values"] if
                                           not s.startswith(f"{selected_supplier} -")]
            supplier_dropdown.set("")

            messagebox.showinfo("Úspěch", "Dodavatel byl úspěšně smazán.")

        delete_supplier_win = tk.Toplevel()
        delete_supplier_win.title("Smazat dodavatele")
        delete_supplier_win.geometry("400x200")
        delete_supplier_win.config(background="#B0B0E0")

        window_width = 400
        window_height = 200
        screen_width = delete_supplier_win.winfo_screenwidth()
        screen_height = delete_supplier_win.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        delete_supplier_win.geometry(f"{window_width}x{window_height}+{x}+{y}")

        main_frame = tk.Frame(delete_supplier_win, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.config(background="#B0B0E0")

        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM dodavatel")
        suppliers = cursor.fetchall()

        supplier_var = tk.StringVar()
        supplier_dropdown = ttk.Combobox(main_frame, textvariable=supplier_var)
        supplier_dropdown["values"] = [f"{s[0]} - {s[1]}" for s in suppliers]
        supplier_dropdown.current(0)
        supplier_dropdown.pack(pady=(10, 20))

        delete_button = ttk.Button(main_frame, text="Smazat dodavatele", command=delete_selected_supplier)
        delete_button.pack(pady=(10, 20))

    @staticmethod
    def show_suppliers():
        """
        Metoda pro zobrazení všech dodavatelů v databázi v novém okně.
        """
        def close_suppliers_window():
            """
            Metoda pro zavření okna s dodavateli.
            """
            suppliers_win.destroy()

        suppliers_win = tk.Toplevel()
        suppliers_win.title("Dodavatelé")

        width = 800
        height = 600
        screen_width = suppliers_win.winfo_screenwidth()
        screen_height = suppliers_win.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        suppliers_win.geometry("%dx%d+%d+%d" % (width, height, x, y))

        suppliers_win.config(background="#B0B0E0")

        main_frame = tk.Frame(suppliers_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        content_frame = tk.Frame(main_frame, bg="#B0B0E0")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tree_scrollbar = ttk.Scrollbar(content_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM dodavatel")
        suppliers = cursor.fetchall()

        style = ttk.Style()
        style.configure("Custom.Treeview", background="#B0B0E0", foreground="black", rowheight=25,
                        fieldbackground="#B0B0E0")
        style.configure("Custom.Treeview.Heading", font=("Helvetica", 12), background="#B0B0E0", foreground="black")
        style.map("Custom.Treeview.Heading", background=[("active", "#C0C0E0")])

        tree = ttk.Treeview(content_frame, columns=("id", "nazev", "adresa"), show="headings", style="Custom.Treeview",
                            yscrollcommand=tree_scrollbar.set)
        tree.column("id", width=50, anchor="center")
        tree.column("nazev", width=250, anchor="center")
        tree.column("adresa", width=400, anchor="center")
        tree.heading("id", text="ID")
        tree.heading("nazev", text="Název")
        tree.heading("adresa", text="Adresa")

        for supplier in suppliers:
            tree.insert("", "end", values=(supplier[0], supplier[1], supplier[2]))

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=tree.yview)

        close_button = ttk.Button(main_frame, text="Zavřít", command=close_suppliers_window)
        close_button.pack(pady=(10, 20), side="bottom", anchor="e")

    @staticmethod
    def show_add_supplier_product_window():
        """
        Metoda pro zobrazení okna pro přidání produktu k vybranému dodavateli.
        """
        def fetch_suppliers():
            """
            Metoda pro načtení dodavatelů z databáze.

            :return: seznam dodavatelů z databáze
            """
            db_connection = DatabaseConnection().connect_to_database()
            cursor = db_connection.cursor()
            cursor.execute("SELECT id, nazev FROM dodavatel")
            return cursor.fetchall()

        def fetch_products():
            """
            Metoda pro načtení produktů z databáze.

            :return: seznam produktů z databáze
            """
            db_connection = DatabaseConnection().connect_to_database()
            cursor = db_connection.cursor()
            cursor.execute("SELECT id, nazev FROM produkt")
            return cursor.fetchall()

        def add_supplier_product(add_supplier_product_win, supplier_var, product_var):
            """
            Metoda pro přidání produktu k vybranému dodavateli v databázi.

            :param add_supplier_product_win: instance okna pro přidání produktu k dodavateli
            :param supplier_var: tk.StringVar() obsahující informace o vybraném dodavateli
            :param product_var: tk.StringVar() obsahující informace o vybraném produktu
            """
            supplier_id = supplier_var.get()
            product_id = product_var.get()

            if supplier_id and product_id:
                try:
                    db_connection = DatabaseConnection().connect_to_database()
                    cursor = db_connection.cursor()
                    cursor.execute("INSERT INTO dodavatel_produkt (dodavatel_id, produkt_id) VALUES (%s, %s)",
                                   (supplier_id, product_id))
                    db_connection.commit()
                    messagebox.showinfo("Úspěch", "Produkt byl úspěšně přidán k dodavateli.")
                    add_supplier_product_win.destroy()
                except Exception as e:
                    messagebox.showerror("Chyba", f"Chyba při přidávání produktu k dodavateli: {str(e)}")
            else:
                messagebox.showwarning("Varování", "Vyberte dodavatele a produkt.")

        def on_closing(add_supplier_product_win):
            """
            Metoda pro zavření okna pro přidání produktu k dodavateli.

            :param add_supplier_product_win: instance okna pro přidání produktu k dodavateli
            """
            if messagebox.askokcancel("Zavřít", "Opravdu chcete zavřít toto okno?"):
                add_supplier_product_win.destroy()

        add_supplier_product_win = tk.Toplevel()
        add_supplier_product_win.title("Přidat produkt k dodavateli")
        add_supplier_product_win.configure(bg="#B0B0E0")
        add_supplier_product_win.geometry("400x200")
        add_supplier_product_win.protocol("WM_DELETE_WINDOW",
                                          lambda: on_closing(add_supplier_product_win))

        main_frame = tk.Frame(add_supplier_product_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        supplier_label = ttk.Label(main_frame, text="Dodavatel:")
        supplier_label.grid(row=0, column=0, padx=(0, 10), sticky="e")
        supplier_label.config(background="#B0B0E0")

        supplier_var = tk.StringVar()
        supplier_combobox = ttk.Combobox(main_frame, textvariable=supplier_var, state="readonly")
        supplier_combobox["values"] = fetch_suppliers()
        supplier_combobox.grid(row=0, column=1, sticky="w")

        product_label = ttk.Label(main_frame, text="Produkt:")
        product_label.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="e")
        product_label.config(background="#B0B0E0")
        product_var = tk.StringVar()
        product_combobox = ttk.Combobox(main_frame, textvariable=product_var, state="readonly")
        product_combobox["values"] = fetch_products()
        product_combobox.grid(row=1, column=1, pady=(10, 0), sticky="w")

        add_button = ttk.Button(main_frame, text="Přidat",
                                command=lambda: add_supplier_product(add_supplier_product_win, supplier_var,
                                                                     product_var))
        add_button.grid(row=2, column=1, pady=(20, 0), sticky="e")

        add_supplier_product_win.update_idletasks()
        width = add_supplier_product_win.winfo_width()
        height = add_supplier_product_win.winfo_height()
        x = (add_supplier_product_win.winfo_screenwidth() // 2) - (width // 2)
        y = (add_supplier_product_win.winfo_screenheight() // 2) - (height // 2)
        add_supplier_product_win.geometry(f"{width}x{height}+{x}+{y}")