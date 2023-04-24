import tkinter as tk
from tkinter import ttk
from conn import DatabaseConnection
from tkinter import messagebox
import mysql.connector


class StoreWindows:
    """
    Třída StoreWindows poskytuje metody pro správu obchodů v aplikaci

    """
    @staticmethod
    def show_store_management(parent):
        """
        Metoda pro zobrazení správy obchodů v hlavním okně aplikace.

        :param parent: rodičovský widget, ve kterém budou umístěny tlačítka pro správu obchodů
        """
        for widget in parent.winfo_children():
            widget.destroy()

        edit_store_button = ttk.Button(parent, text="Úprava obchodů", command=StoreWindows.edit_store_window)
        edit_store_button.pack(pady=(20, 10))

        add_store_button = ttk.Button(parent, text="Přidání obchodů", command=StoreWindows.add_store_window)
        add_store_button.pack(pady=(10, 10))

        delete_store_button = ttk.Button(parent, text="Smazání obchodů", command=StoreWindows.delete_store_window)
        delete_store_button.pack(pady=(10, 10))

        show_stores_button = ttk.Button(parent, text="Zobrazit obchody", command=StoreWindows.show_stores)
        show_stores_button.pack(pady=(10, 0))

    @staticmethod
    def set_window_geometry(window, width, height):
        """
        Metoda pro nastavení geometrie okna (šířka, výška a pozice na obrazovce).

        :param window: okno, jehož geometrii chceme nastavit
        :param width: šířka okna
        :param height: výška okna
        """
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (width / 2))
        y_coordinate = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    @staticmethod
    def edit_store_window():
        """
        Metoda pro zobrazení okna pro úpravu obchodů.
         """
        edit_store_win = tk.Toplevel()
        edit_store_win.title("Úprava obchodů")
        StoreWindows.set_window_geometry(edit_store_win, 400, 300)
        edit_store_win.config(background="#B0B0E0")

        main_frame = tk.Frame(edit_store_win, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.config(background="#B0B0E0")

        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()

        cursor.execute("SELECT id, nazev FROM obchod")
        stores = [(row[0], row[1]) for row in cursor.fetchall()]

        store_label = ttk.Label(main_frame, text="Vyberte obchod k úpravě:")
        store_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        store_label.config(background="#B0B0E0")

        store_var = tk.IntVar()
        store_combobox = ttk.Combobox(main_frame, textvariable=store_var, values=[s[1] for s in stores],
                                      state="readonly")
        store_combobox.grid(row=0, column=1, padx=20, pady=10)

        name_label = ttk.Label(main_frame, text="Nový název:")
        name_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        name_label.config(background="#B0B0E0")

        name_entry = ttk.Entry(main_frame)
        name_entry.grid(row=1, column=1, padx=20, pady=10)

        address_label = ttk.Label(main_frame, text="Nová adresa:")
        address_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        address_label.config(background="#B0B0E0")

        address_entry = ttk.Entry(main_frame)
        address_entry.grid(row=2, column=1, padx=20, pady=10)

        def update_store():
            """
            Metoda pro aktualizaci vybraného obchodu v databázi s novým názvem a adresou.
            """
            selected_store_index = store_combobox.current()

            if selected_store_index == -1:
                messagebox.showwarning("Varování", "Vyberte obchod, který chcete upravit.")
                return

            new_name = name_entry.get().strip()
            new_address = address_entry.get().strip()

            if len(new_name) < 3 or len(new_address) < 3:
                messagebox.showwarning("Varování", "Název a adresa obchodu musí mít minimálně 3 znaky.")
                return

            selected_store_id, selected_store_name = stores[selected_store_index]

            try:
                cursor.execute("UPDATE obchod SET nazev = %s, adresa = %s WHERE id = %s",
                               (new_name, new_address, selected_store_id))
                db_connection.commit()
                messagebox.showinfo("Úspěch", f"Obchod '{selected_store_name}' byl úspěšně upraven.")
                store_combobox.delete(0, 'end')
                cursor.execute("SELECT id, nazev FROM obchod")
                new_stores = [(row[0], row[1]) for row in cursor.fetchall()]
                store_combobox.config(values=[s[1] for s in new_stores])
                stores[:] = new_stores
            except mysql.connector.Error:
                messagebox.showerror("Chyba při úpravě obchodu: {err}")
                db_connection.rollback()

        update_button = ttk.Button(main_frame, text="Aktualizovat obchod", command=update_store)
        update_button.grid(row=3, column=0, columnspan=2, pady=20)

    @staticmethod
    def add_store_window():
        """
        Metoda pro zobrazení okna, které umožňuje přidání nového obchodu.
        Obsahuje formulář pro zadání názvu a adresy obchodu a tlačítko pro přidání obchodu.
        """
        def add_store():
            store_name = store_name_entry.get().strip()
            store_address = store_address_entry.get().strip()

            if len(store_name) < 3 or len(store_address) < 3:
                messagebox.showwarning("Varování", "Jméno a adresa obchodu musí mít minimálně 3 znaky.")
                return

            try:
                cursor.execute("INSERT INTO obchod (nazev, adresa) VALUES (%s, %s)", (store_name, store_address))
                db_connection.commit()
                messagebox.showinfo("Úspěch", f"Obchod '{store_name}' byl úspěšně přidán.")
                store_name_entry.delete(0, 'end')
                store_address_entry.delete(0, 'end')
            except mysql.connector.Error as err:
                messagebox.showerror("Chyba", f"Chyba při přidávání obchodu: {err}")
                db_connection.rollback()

        add_store_win = tk.Toplevel()
        add_store_win.title("Přidání obchodu")
        StoreWindows.set_window_geometry(add_store_win, 400, 250)
        add_store_win.config(background="#B0B0E0")

        main_frame = tk.Frame(add_store_win, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.config(background="#B0B0E0")

        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()

        store_name_label = ttk.Label(main_frame, text="Jméno obchodu:")
        store_name_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        store_name_label.config(background="#B0B0E0")

        store_name_entry = ttk.Entry(main_frame)
        store_name_entry.grid(row=0, column=1, padx=20, pady=10)

        store_address_label = ttk.Label(main_frame, text="Adresa obchodu:")
        store_address_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        store_address_label.config(background="#B0B0E0")

        store_address_entry = ttk.Entry(main_frame)
        store_address_entry.grid(row=1, column=1, padx=20, pady=10)

        add_store_button = ttk.Button(main_frame, text="Přidat obchod", command=add_store)
        add_store_button.grid(row=2, column=0, columnspan=2, pady=(10, 20))

    @staticmethod
    def delete_store_window():
        """
        Metoda pro zobrazení okna, které umožňuje smazání obchodu.
        Obsahuje rozbalovací nabídku pro výběr obchodu a tlačítko pro smazání vybraného obchodu.
        """
        delete_store_win = tk.Toplevel()
        delete_store_win.title("Smazání obchodů")
        StoreWindows.set_window_geometry(delete_store_win, 400, 250)
        delete_store_win.config(background="#B0B0E0")
        main_frame = tk.Frame(delete_store_win, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.config(background="#B0B0E0")

        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()

        cursor.execute("SELECT id, nazev FROM obchod")
        stores = [(row[0], row[1]) for row in cursor.fetchall()]

        store_label = ttk.Label(main_frame, text="Vyberte obchod ke smazání:")
        store_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        store_label.config(background="#B0B0E0")

        stores_var = tk.IntVar()
        store_combobox = ttk.Combobox(main_frame, textvariable=stores_var, values=[s[1] for s in stores],
                                      state="readonly")
        store_combobox.grid(row=0, column=1, padx=20, pady=10)

        def delete_store():
            selected_store_index = store_combobox.current()

            if selected_store_index == -1:
                messagebox.showwarning("Varování", "Vyberte obchod, který chcete smazat.")
                return

            selected_store_id, selected_store_name = stores[selected_store_index]

            if messagebox.askyesno("Potvrzení", f"Opravdu chcete smazat obchod '{selected_store_name}'?"):
                try:
                    cursor.execute("INSERT INTO sklad_produkt (sklad_id, produkt_id, mnozstvi) "
                                   "SELECT 1, produkt_id, SUM(mnozstvi) "
                                   "FROM obchod_produkt "
                                   "WHERE obchod_id = %s "
                                   "GROUP BY produkt_id "
                                   "ON DUPLICATE KEY UPDATE mnozstvi = mnozstvi + VALUES(mnozstvi)",
                                   (selected_store_id,))

                    cursor.execute("DELETE FROM obchod_produkt WHERE obchod_id = %s", (selected_store_id,))
                    cursor.execute("DELETE FROM obchod WHERE id = %s", (selected_store_id,))
                    db_connection.commit()
                    messagebox.showinfo("Úspěch", f"Obchod '{selected_store_name}' byl úspěšně smazán.")
                    store_combobox.delete(0, 'end')
                    cursor.execute("SELECT id, nazev FROM obchod")
                    new_stores = [(row[0], row[1]) for row in cursor.fetchall()]
                    store_combobox.config(values=[s[1] for s in new_stores])
                    stores[:] = new_stores
                except mysql.connector.Error as err:
                    messagebox.showerror("Chyba", f"Chyba při mazání obchodu: {err}")
                    db_connection.rollback()

        delete_button = ttk.Button(main_frame, text="Smazat obchod", command=delete_store)
        delete_button.grid(row=1, columnspan=2, pady=(10, 20))

    @staticmethod
    def show_stores():
        """
        Metoda pro zobrazení okna se seznamem všech obchodů.
        Zobrazuje ID, název a adresu každého obchodu v tabulce. Obsahuje tlačítko pro zavření okna.
        """
        def close_stores_window():
            stores_win.destroy()

        stores_win = tk.Toplevel()
        stores_win.title("Obchody")
        StoreWindows.set_window_geometry(stores_win, 800, 600)
        stores_win.config(background="#B0B0E0")

        main_frame = tk.Frame(stores_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        content_frame = tk.Frame(main_frame, bg="#B0B0E0")
        content_frame.pack(fill=tk.BOTH, expand=True)

        tree_scrollbar = ttk.Scrollbar(content_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM obchod")
        stores = cursor.fetchall()

        style = ttk.Style()
        style.configure("Custom.Treeview", background="#B0B0E0", foreground="black", rowheight=25
                        )
        style.configure("Custom.Treeview.Heading", font=("Helvetica", 12), foreground="black")
        style.map("Custom.Treeview.Heading", background=[("active", "#C0C0E0")])

        tree = ttk.Treeview(content_frame, columns=("id", "nazev", "adresa"), show="headings", style="Custom.Treeview",
                            yscrollcommand=tree_scrollbar.set)
        tree.column("id", width=50, anchor="center")
        tree.column("nazev", width=250, anchor="center")
        tree.column("adresa", width=400, anchor="center")
        tree.heading("id", text="ID")
        tree.heading("nazev", text="Název")
        tree.heading("adresa", text="Adresa")
        # Iteruje přes seznam 'stores', který obsahuje informace o obchodech (ID, název a adresa)
        # Pro každý obchod vloží do stromového zobrazení (ttk.Treeview) řádek s hodnotami ID, názvem a adresou obchodu
        for store in stores:
            tree.insert("", "end", values=(store[0], store[1], store[2]))

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=tree.yview)

        close_button = ttk.Button(main_frame, text="Zavřít", command=close_stores_window)
        close_button.pack(pady=(10, 20), side="bottom", anchor="e")
        