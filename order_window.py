import tkinter as tk
from tkinter import ttk, messagebox
from conn import DatabaseConnection


class OrderWindows:
    def __init__(self, content_frame):
        """
        Konstruktor třídy OrderWindows.

        :param:

        content_frame: Tkinter.Frame
        Rámec, na který se budou vkládat widgety třídy OrderWindows.
        """
        self.content_frame = content_frame

    def show_order_management_buttons(self):
        """
        Metoda pro zobrazení tlačítek pro správu objednávek.
        """
        # Odstranění předchozích widgetů v rámci content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        # Vytvoření rámce pro tlačítka
        order_button_frame = tk.Frame(self.content_frame, bg="#B0B0E0")
        order_button_frame.pack(pady=(10, 10))
        # Tlačítko pro zobrazení objednávek
        display_order_button = ttk.Button(order_button_frame, text="Zobrazení objednávek",
                                       command=self.view_order)
        display_order_button.pack(pady=(10, 0))
        # Tlačítko pro smazání objednávky
        delete_order_button = ttk.Button(order_button_frame, text="Smazání objednávky",
                                         command=self.delete_order_window)
        delete_order_button.pack(pady=(10, 0))
        # Tlačítko pro úpravu objednávky
        edit_order_button = ttk.Button(order_button_frame, text="Upravit objednávku",
                                       command=self.edit_order_window)  # Add a new method for edit_order_window
        edit_order_button.pack(pady=(10, 0))

    def view_order(self):
        """
        Metoda pro zobrazení okna s výpisem objednávek z databáze.
        """
        self.display_orders_window()

    def display_orders_window(self):
        """
        Metoda pro zobrazení okna s výpisem objednávek.
        """
        def close_orders_window():
            orders_window.destroy()
        # Vytvoření nového okna
        orders_window = tk.Toplevel()
        orders_window.title("Objednávky")
        orders_window.config(background="#B0B0E0")
        # Nastavení polohy a velikosti okna
        orders_window.update_idletasks()
        screen_width = orders_window.winfo_screenwidth()
        screen_height = orders_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        orders_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        # Vytvoření hlavního rámečku
        main_frame = tk.Frame(orders_window, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoření rámečku pro Treeview
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoření scrollbaru pro Treeview
        tree_scrollbar = ttk.Scrollbar(content_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Připojení k databázi a získání objednávek
        db_conn = DatabaseConnection()
        connection = db_conn.connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM objednavka")
        orders = cursor.fetchall()
        # Vytvoření stylu pro Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", foreground="black", rowheight=25)
        style.configure("Custom.Treeview.Heading", font=("Helvetica", 12), background="#B0B0E0", foreground="black")
        style.map("Custom.Treeview.Heading", background=[("active", "#C0C0E0")])
        # Vytvoření Treeview s objednávkami
        tree = ttk.Treeview(content_frame, columns=("id", "stav", "zakaznik_id"), show="headings",
                            style="Custom.Treeview",
                            yscrollcommand=tree_scrollbar.set)
        tree.column("id", width=50, anchor="center")
        tree.column("stav", width=250, anchor="center")
        tree.column("zakaznik_id", width=400, anchor="center")
        tree.heading("id", text="ID")
        tree.heading("stav", text="Stav")
        tree.heading("zakaznik_id", text="Zákazník ID")
        # Naplnění Treeview daty z databáze
        for order in orders:
            tree.insert("", "end", values=(order[0], order[1], order[2]))

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=tree.yview)
        # Tlačítko pro zavření okna
        close_button = ttk.Button(main_frame, text="Zavřít", command=close_orders_window)
        close_button.pack(pady=(10, 20), side="bottom", anchor="e")

        cursor.close()
        connection.close()

    def delete_order_window(self):
        """
        Metoda pro zobrazení okna pro smazání objednávky.
        """
        def close_delete_order_window():
            delete_order_window.destroy()

        def get_orders():
            cursor.execute("SELECT id FROM objednavka")
            return cursor.fetchall()

        def delete_order():
            selected_order_id = int(order_var.get().split()[0])
            cursor.execute("DELETE FROM objednavka WHERE id = %s", (selected_order_id,))
            connection.commit()
            order_var.set('')
            order_dropdown['values'] = [f"{order[0]}" for order in get_orders()]
            cursor.close()
            connection.close()

        db_conn = DatabaseConnection()
        connection = db_conn.connect_to_database()
        cursor = connection.cursor()

        orders = get_orders()
        # Vytvoření nového okna
        delete_order_window = tk.Toplevel()
        delete_order_window.title("Smazání objednávky")
        delete_order_window.minsize(400, 300)
        delete_order_window.configure(bg="#B0B0E0")
        # Nastavení polohy a velikosti okna
        delete_order_window.update_idletasks()
        screen_width = delete_order_window.winfo_screenwidth()
        screen_height = delete_order_window.winfo_screenheight()
        window_width = 400
        window_height = 300
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        delete_order_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        # Vytvoření labelu a Comboboxu pro výběr objednávky k smazání
        order_label = tk.Label(delete_order_window, text="ID Objednávky:", bg="#B0B0E0")
        order_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        order_var = tk.StringVar(delete_order_window)
        order_dropdown = ttk.Combobox(delete_order_window, textvariable=order_var)
        order_dropdown['values'] = [f"{order[0]}" for order in orders]
        order_dropdown.grid(row=0, column=1, padx=20, pady=20)
        # Tlačítko pro smazání objednávky
        delete_button = ttk.Button(delete_order_window, text="Smazat", command=delete_order)
        delete_button.grid(row=1, column=1, padx=20, pady=20, sticky="e")

    def edit_order_window(self):
        """
        Metoda pro zobrazení okna pro úpravu stavu objednávky.
        """
        def get_orders():
            cursor.execute("SELECT id, stav FROM objednavka")
            return cursor.fetchall()

        def save_changes():
            selected_order_info = order_var.get()
            if not selected_order_info:
                messagebox.showwarning("Varování", "Vyberte objednávku, kterou chcete upravit.")
                return

            selected_order_id = int(selected_order_info.split(" - ")[0])
            new_status = status_entry.get().strip()

            if not new_status:
                messagebox.showwarning("Varování", "Zadejte nový stav objednávky.")
                return

            try:
                cursor.execute("UPDATE objednavka SET stav = %s WHERE id = %s", (new_status, selected_order_id))
                db_connection.commit()
                messagebox.showinfo("Informace", "Stav objednávky úspěšně upraven.")
                edit_order_win.destroy()
            except Exception as e:
                messagebox.showerror("Chyba", f"Nastala chyba při úpravě objednávky: {e}")

        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()

        orders = get_orders()
        # Vytvoření nového okna
        edit_order_win = tk.Toplevel()
        edit_order_win.title("Upravit objednávku")
        edit_order_win.minsize(400, 250)
        edit_order_win.configure(bg="#B0B0E0")
        # Vytvoření labelu a Comboboxu pro výběr objednávky k úpravě
        order_label = tk.Label(edit_order_win, text="ID objednávky:", bg="#B0B0E0")
        order_label.grid(row=0, column=0, padx=20, pady=20, sticky="e")

        order_var = tk.StringVar(edit_order_win)
        order_dropdown = ttk.Combobox(edit_order_win, textvariable=order_var)
        order_dropdown['values'] = [f"{order[0]} - {order[1]}" for order in orders]
        order_dropdown.grid(row=0, column=1, padx=20, pady=20)

        status_label = tk.Label(edit_order_win, text="Nový stav:", bg="#B0B0E0")
        status_label.grid(row=1, column=0, padx=20, pady=20, sticky="e")

        status_entry = tk.Entry(edit_order_win)
        status_entry.grid(row=1, column=1, padx=20, pady=20)

        save_button = ttk.Button(edit_order_win, text="Uložit změny", command=save_changes)
        save_button.grid(row=2, columnspan=2, padx=20, pady=20)

        edit_order_win.mainloop()

