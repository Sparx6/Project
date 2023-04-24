import tkinter as tk
from tkinter import ttk, messagebox
from conn import DatabaseConnection
class CustomerWindows:
    """
    Třída CustomerWindows obsahuje metody pro práci se zákazníky(přidání úprava odstranění a zobrazení)
    """
    @staticmethod
    def show_customer_management_buttons(content_frame, clear_content_callback):
        """
        Metoda zobrazuje tlačítka pro správu zákazníků a volá funkci clear_content_callback,
        která čistí obsah content_frame.
        """
        clear_content_callback()

        customer_button_frame = tk.Frame(content_frame, bg="#B0B0E0")

        add_customer_button = ttk.Button(customer_button_frame, text="Přidat zákazníka",
                                        command=lambda: CustomerWindows.add_customer_window(content_frame))
        add_customer_button.pack(pady=(10, 0))

        edit_customer_button = ttk.Button(customer_button_frame, text="Upravit zákazníka",
                                         command=lambda: CustomerWindows.edit_customer_window(content_frame))
        edit_customer_button.pack(pady=(10, 0))

        delete_customer_button = ttk.Button(customer_button_frame, text="Smazat zákazníka",
                                            command=lambda: CustomerWindows.delete_customer())
        delete_customer_button.pack(pady=(10, 0))

        view_customers_button = ttk.Button(customer_button_frame, text="Zobrazit zákazníky",
                                          command=lambda: CustomerWindows.view_customers_window(content_frame))
        view_customers_button.pack(pady=(10, 0))

        customer_button_frame.pack(anchor='n', pady=10)

    @staticmethod
    def add_customer_window(content_frame):
        """
        Metoda vytváří okno pro přidání nového zákazníka a odesílá zadané údaje do databáze.
        :param content_frame
        """
        def submit_customer():
            # Získání hodnot z formuláře
            jmeno = name_entry.get()
            prijmeni = surname_entry.get()
            email = email_entry.get()
            body = loyalty_points_entry.get()
            # Kontrola délky zadaných hodnot
            if len(jmeno) < 3 or len(prijmeni) < 3 or len(email) < 3:
                messagebox.showerror("Chyba", "Jméno, příjmení a email musí obsahovat alespoň 3 znaky.")
                return
            # Připojení k databázi a vložení zákazníka
            db_connection = DatabaseConnection().connect_to_database()
            cursor = db_connection.cursor()

            try:
                cursor.execute("INSERT INTO zakaznik (jmeno, prijmeni, email, vernostni_body) VALUES (%s, %s, %s, %s)",
                               (jmeno, prijmeni, email, body))
                db_connection.commit()
                messagebox.showinfo("Úspěch", "Zákazník úspěšně přidán.")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při přidávání zákazníka: {e}")
            finally:
                cursor.close()
                db_connection.close()
                add_customer_win.destroy()

        # Vytvoření okna pro přidání zákazníka
        add_customer_win = tk.Toplevel(content_frame)
        add_customer_win.title("Přidat zákazníka")
        add_customer_win.configure(bg="#B0B0E0")

        add_customer_win.geometry("400x300")
        add_customer_win.update_idletasks()
        screen_width = add_customer_win.winfo_screenwidth()
        screen_height = add_customer_win.winfo_screenheight()
        x = (screen_width // 2) - (add_customer_win.winfo_width() // 2)
        y = (screen_height // 2) - (add_customer_win.winfo_height() // 2)
        add_customer_win.geometry(f"+{x}+{y}")
        # Vytvoření a umístění widgetů formuláře
        name_label = tk.Label(add_customer_win, text="Jméno:", bg="#B0B0E0")
        name_label.grid(row=0, column=0, padx=10, pady=10)

        name_entry = tk.Entry(add_customer_win)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        surname_label = tk.Label(add_customer_win, text="Příjmení:", bg="#B0B0E0")
        surname_label.grid(row=1, column=0, padx=10, pady=10)

        surname_entry = tk.Entry(add_customer_win)
        surname_entry.grid(row=1, column=1, padx=10, pady=10)

        email_label = tk.Label(add_customer_win, text="Email:", bg="#B0B0E0")
        email_label.grid(row=2, column=0, padx=10, pady=10)

        email_entry = tk.Entry(add_customer_win)
        email_entry.grid(row=2, column=1, padx=10, pady=10)

        loyalty_points_label = tk.Label(add_customer_win, text="Věrnostní body:", bg="#B0B0E0")
        loyalty_points_label.grid(row=3, column=0, padx=10, pady=10)

        loyalty_points_entry = tk.Entry(add_customer_win)
        loyalty_points_entry.grid(row=3, column=1, padx=10, pady=10)
        # Tlačítko pro potvrzení
        add_customer_button = ttk.Button(add_customer_win, text="Přidat zákazníka", command=submit_customer)
        add_customer_button.grid(row=4, column=0, columnspan=2, pady=10)

    @staticmethod
    def edit_customer_window(content_frame):
        """
            Metoda pro vytvoření okna pro úpravu zákazníka.
           :param content_frame
        """
        def load_customers():
            """
                Metoda pro načtení zákazníků z databáze.
            """
            db_connection = DatabaseConnection().connect_to_database()
            cursor = db_connection.cursor()
            cursor.execute("SELECT id, jmeno, prijmeni FROM zakaznik")
            customers = cursor.fetchall()
            cursor.close()
            db_connection.close()
            return customers

        def submit_changes():
            """
                Metoda pro odeslání změn upraveného zákazníka.
            """
            customer = customer_var.get()
            new_email = email_entry.get()
            new_points = loyalty_points_entry.get()

            if not new_email or len(new_email) < 3:
                messagebox.showerror("Chyba", "Email musí obsahovat alespoň 3 znaky.")
                return

            customer_id = int(customer.split(" - ")[0])

            db_connection = DatabaseConnection().connect_to_database()
            cursor = db_connection.cursor()

            try:
                cursor.execute("UPDATE zakaznik SET email = %s, vernostni_body = %s WHERE id = %s", (new_email, new_points, customer_id))
                db_connection.commit()
                messagebox.showinfo("Úspěch", "Zákazník úspěšně upraven.")
            except Exception as e:
                messagebox.showerror("Chyba", f"Chyba při úpravě zákazníka: {e}")
            finally:
                cursor.close()
                db_connection.close()
                edit_customer_win.destroy()

        # Vytvoření a konfigurace okna pro úpravu zákazníka
        edit_customer_win = tk.Toplevel(content_frame)
        edit_customer_win.title("Upravit zákazníka")
        edit_customer_win.geometry("400x250")
        edit_customer_win.config(background="#B0B0E0")

        window_width = 400
        window_height = 250
        screen_width = edit_customer_win.winfo_screenwidth()
        screen_height = edit_customer_win.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        edit_customer_win.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # Vytvoření a umístění widgetů formuláře
        main_frame = tk.Frame(edit_customer_win, padx=20, pady=20, background="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        customers = load_customers()
        customer_var = tk.StringVar()
        if customers:
            customer_var.set(f"{customers[0][0]} - {customers[0][1]} {customers[0][2]}")
        else:
            customer_var.set("Žádní zákazníci")
        customer_dropdown = ttk.Combobox(main_frame, textvariable=customer_var)
        # Seznam n-tic kde každá obsahuje záznam
        customer_dropdown["values"] = [f"{c[0]} - {c[1]} {c[2]}" for c in customers]
        customer_dropdown.current(0)
        customer_dropdown.pack(pady=(10, 20))
        form_frame = tk.Frame(main_frame, background="#B0B0E0")
        form_frame.pack()

        email_label = tk.Label(form_frame, text="Nový email:", bg="#B0B0E0")
        email_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        email_entry = ttk.Entry(form_frame)
        email_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        loyalty_points_label = tk.Label(form_frame, text="Nové věrnostní body:", bg="#B0B0E0")
        loyalty_points_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        loyalty_points_entry = ttk.Entry(form_frame)
        loyalty_points_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        update_button = ttk.Button(main_frame, text="Upravit zákazníka", command=submit_changes)
        update_button.pack(pady=(10, 20))

    @staticmethod
    def delete_customer():
        """
        Metoda pro smazání vybraného zákazníka z databáze.
        """
        def delete_selected_customer():
            """
            Funkce pro smazání zákazníka z databáze podle vybraného záznamu v Comboboxu.
            """
            # získává ID zákazníka ze StringVar proměnné customer_var a převádí toto ID na celé číslo
            selected_customer = int(customer_var.get().split(" - ")[0])

            cursor = db_connection.cursor()
            delete_query = "DELETE FROM zakaznik WHERE id = %s"
            cursor.execute(delete_query, (selected_customer,))
            db_connection.commit()
            # Aktualizuje hodnoty v rozevíracím seznamu 'customer_dropdown' tak aby byla odstraněna
            # položka začínající na 'selected_customer -'. Tím se zajistí že smazaný zákazník
            # již nebude v rozevíracím seznamu.
            customer_dropdown["values"] = [s for s in customer_dropdown["values"] if
                                           not s.startswith(f"{selected_customer} -")]
            customer_dropdown.set("")

            messagebox.showinfo("Úspěch", "Zakaznik byl úspěšně smazán.")

        delete_customer_win = tk.Toplevel()
        delete_customer_win.title("Smazat zakaznika")
        delete_customer_win.geometry("400x200")
        delete_customer_win.config(background="#B0B0E0")

        window_width = 400
        window_height = 200
        screen_width = delete_customer_win.winfo_screenwidth()
        screen_height = delete_customer_win.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        delete_customer_win.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # Vytvoření hlavního rámečku 'main_frame' a nastavení jeho rozložení a pozadí
        main_frame = tk.Frame(delete_customer_win, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.config(background="#B0B0E0")
        # Připojení k databázi a selectnutí zákazníků
        db_connection = DatabaseConnection().connect_to_database()
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM zakaznik")
        customers = cursor.fetchall()
        # Vytvoření proměnné pro uchování vybraného zákazníka a rozevíracího seznamu 'customer_dropdown'
        customer_var = tk.StringVar()
        customer_dropdown = ttk.Combobox(main_frame, textvariable=customer_var)
        # Nastavení hodnot rozevíracího seznamu na základě načtených zákazníků
        customer_dropdown["values"] = [f"{s[0]} - {s[1]}" for s in customers]
        customer_dropdown.current(0)
        customer_dropdown.pack(pady=(10, 20))
        # Vytvoření tlačítka 'delete_button' pro smazání vybraného zákazníka a jeho umístění
        delete_button = ttk.Button(main_frame, text="Smazat zakaznika", command=delete_selected_customer)
        delete_button.pack(pady=(10, 20))

    @staticmethod
    def view_customers_window(content_frame):
        """
        Statická metoda pro vytvoření okna pro zobrazení seznamu zákazníků.
        :param content_frame
        """
        def load_customers():
            """
            Načte zákazníky z databáze a vrátí je jako seznam n-tic.
            """

            db_connection = DatabaseConnection().connect_to_database()
            cursor = db_connection.cursor()
            cursor.execute("SELECT id, jmeno, prijmeni, email, vernostni_body FROM zakaznik")
            customers = cursor.fetchall()
            cursor.close()
            db_connection.close()
            return customers

        # Vytvoření okna pro zobrazení zákazníků
        view_customers_win = tk.Toplevel(content_frame)
        view_customers_win.title("Zobrazit zákazníky")
        # Nastavení rozměrů a umístění okna
        width = 800
        height = 600
        screen_width = view_customers_win.winfo_screenwidth()
        screen_height = view_customers_win.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        view_customers_win.geometry("%dx%d+%d+%d" % (width, height, x, y))
        # Nastavení pozadí okna
        view_customers_win.config(background="#B0B0E0")
        # Vytvoření hlavního rámu
        main_frame = tk.Frame(view_customers_win, padx=20, pady=20, bg="#B0B0E0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoření rámu pro obsah
        content_frame = tk.Frame(main_frame, bg="#B0B0E0")
        content_frame.pack(fill=tk.BOTH, expand=True)
        # Vytvoření posuvníku pro stromový pohled
        tree_scrollbar = ttk.Scrollbar(content_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Načtení zákazníků
        customers = load_customers()
        # Nastavení stylu pro stromový pohled
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#B0B0E0", foreground="black", rowheight=25,
                        fieldbackground="#B0B0E0")
        style.configure("Custom.Treeview.Heading", font=("Helvetica", 12), background="#B0B0E0", foreground="black")
        style.map("Custom.Treeview.Heading", background=[("active", "#C0C0E0")])
        # Vytvoření stromového pohledu pro zobrazení zákazníků
        tree = ttk.Treeview(content_frame, columns=("id", "jmeno", "prijmeni", "email", "body"), show="headings",
                            style="Custom.Treeview", yscrollcommand=tree_scrollbar.set)
        tree.column("id", width=50, anchor="center")
        tree.column("jmeno", width=150, anchor="center")
        tree.column("prijmeni", width=150, anchor="center")
        tree.column("email", width=250, anchor="center")
        tree.column("body", width=100, anchor="center")
        tree.heading("id", text="ID")
        tree.heading("jmeno", text="Jméno")
        tree.heading("prijmeni", text="Příjmení")
        tree.heading("email", text="Email")
        tree.heading("body", text="Body")
        # Vložení zákazníků do stromového pohledu
        for customer in customers:
            tree.insert("", "end", values=(customer[0], customer[1], customer[2], customer[3], customer[4]))
        # Umístění stromového pohledu a konfigurace posuvníku
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=tree.yview)

        # Definice funkce pro zavření okna zákazníků
        def close_customers_window():
            view_customers_win.destroy()
            # Vytvoření tlačítka pro zavření okna a jeho umístění
            close_button = ttk.Button(main_frame, text="Zavřít", command=close_customers_window)
            close_button.pack(pady=(10, 20), side="bottom", anchor="e")