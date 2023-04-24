import tkinter as tk
from conn import DatabaseConnection
import management


class Login:
    """
    Třída zajišťuje přihlašovací proces a ovládání přihlašovacího okna.
    """
    def __init__(self, window_open):
        """
        Inicializace objektu Login.

        :param window_open: instance objektu pro otevírání a uzavírání oken
        """
        self.window_open = window_open

    def get_employee_info(self, username, password):
        """
        Získej informace o zaměstnanci podle zadaného uživatelského jména a hesla.

        :param username: uživatelské jméno
        :param password: heslo
        :return: slovník s informacemi o zaměstnanci nebo None, pokud zaměstnanec nebyl nalezen
        """
        connection = DatabaseConnection().connect_to_database()
        cursor = connection.cursor()
        query = "SELECT * FROM zamestnanec WHERE uzivatelske_jmeno = %s AND heslo = %s"
        cursor.execute(query, (username, password))
        # Získání výsledku SQL dotazu informace o zaměstnanci pokud byl nalezen
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        # Pokud nebyl zaměstnanec nalezen vrátí se None
        if result is None:
            return None
        # Vytvoření slovníku s informacemi o zaměstnanci a jeho vrácení
        employee_dict = {"id": result[0], "jmeno": result[1], "prijmeni": result[2], "uzivatelske_jmeno": result[3]}
        return employee_dict

    def verify_credentials(self, username, password):
        """
        Ověření přihlašovacích údajů zaměstnance.

        :param username: uživatelské jméno
        :param password: heslo
        :return: True, pokud jsou údaje správné, jinak False
        """
        connection = DatabaseConnection().connect_to_database()
        cursor = connection.cursor()
        query = "SELECT * FROM zamestnanec WHERE uzivatelske_jmeno = %s AND heslo = %s"
        cursor.execute(query, (username, password))
        # Získání výsledku SQL dotazu
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        # Vrací True, pokud byl nalezen zaměstnanec s daným uživatelským jménem a heslem jinak False
        return result is not None

    def create_login_window(self, root):
        """
        Vytvoření přihlašovacího okna.

        :param root: hlavní okno aplikace
        """
        # Vytvoření nového okna pro přihlášení
        login_window = tk.Toplevel(root)
        login_window.title("Přihlášení")
        login_window.attributes('-topmost', True)
        self.window_open.center_window(login_window)
        login_window.geometry("300x200")
        login_window.configure(bg="#B0B0E0")
        # Vytvoření lablu a pole pro uživatelské jméno
        username_label = tk.Label(login_window, text="Uživatelské jméno:", bg="#B0B0E0")
        username_label.pack(pady=(10, 0))
        username_entry = tk.Entry(login_window)
        username_entry.pack(pady=(0, 10))
        # Vytvoření lablu a pole pro heslo
        password_label = tk.Label(login_window, text="Heslo:", bg="#B0B0E0")
        password_label.pack(pady=(0, 0))
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack(pady=(0, 10))
        # Vytvoření a umístění tlačítka pro přihlášení
        login_button = tk.Button(login_window, text="Přihlásit se",
                                 command=lambda: self.login_attempt(username_entry, password_entry, root,
                                                                    login_window))
        login_button.pack(pady=(0, 0))
        # Navázání událostí na tlačítko pro přihlášení
        login_button.bind("<Enter>", self.on_enter)
        login_button.bind("<Leave>", self.on_leave)
        login_button.bind("<Button-1>", self.on_click)
        # Vytvoření lablu pro registraci nového účtu
        register_label = tk.Label(login_window, text="Registrovat se", bg="#B0B0E0", fg="blue", cursor="hand2")
        register_label.pack(pady=10)
        # Navázání události na popisek pro registraci která otevře registrační okno
        register_label.bind("<Button-1>", lambda event: self.window_open.open_register_window(root, login_window))

    def on_click_release(self, event):
        """
        Akce po uvolnění tlačítka myši na tlačítku.

        :param event: událost uvolnění tlačítka myši
        """
        event.widget.config(bg="SystemButtonFace", activebackground="SystemButtonFace")
        event.widget.unbind("<ButtonRelease-1>")
        event.widget.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        """
         Akce při najetí myši na tlačítko.

         :param event: událost najetí myši na tlačítko
         """
        event.widget.config(bg="#999999")

    def on_click(self, event):
        """
        Akce při stisknutí tlačítka myši na tlačítku.

        :param event: událost stisknutí tlačítka myši
        """
        event.widget.config(bg="#999999", activebackground="#999999")
        event.widget.unbind("<Button-1>")
        event.widget.bind("<ButtonRelease-1>", self.on_click_release)

    def on_leave(self, event):
        """
        Akce při odjetí myši z tlačítka

        :param event: událost odjetí myši z tlačítka
        """
        event.widget.config(bg="SystemButtonFace", relief="raised")

    def login_attempt(self, username_entry, password_entry, root, login_window):
        """
        Ověření přihlašovacích údajů a zobrazení výsledku.

        :param username_entry: Entry widget pro uživatelské jméno
        :param password_entry: Entry widget pro heslo
        :param root: hlavní okno aplikace
        :param login_window: přihlašovací okno
        """
        # Získání uživatelského jména a hesla z Entry widgetů
        username = username_entry.get()
        password = password_entry.get()
        # Získání informací o zaměstnanci pomocí zadaného uživatelského jména a hesla
        employee_dict = self.get_employee_info(username, password)
        # Pokud existuje slovník s informacemi o zaměstnanci zobrazíme okno s úspěšným přihlášením
        if employee_dict:
            self.show_result_window(root, True, employee_dict, login_window)
        # Pokud ne zobrazíme okno s chybou přihlášení
        else:
            self.show_result_window(root, False)

    def show_result_window(self, root, success, employee_dict=None, login_window=None):
        """
        Zobrazí okno s výsledkem přihlášení.

        :param root: hlavní okno aplikace
        :param success: True, pokud bylo přihlášení úspěšné, jinak False
        :param employee_dict: slovník s informacemi o zaměstnanci
        :param login_window: přihlašovací okno
        """
        # Vytvoření nového okna pro zobrazení výsledku přihlášení
        result_window = tk.Toplevel(root)
        result_window.attributes('-topmost', True)
        # Nastavení rozměrů okna výsledku
        window_width = 300
        window_height = 150
        result_window.minsize(window_width, window_height)
        result_window.geometry(f"{window_width}x{window_height}")
        # Vycentrování okna výsledku
        self.window_open.center_window(result_window)
        result_window.configure(bg="#B0B0E0")
        # Nastavení titulku a zprávy v okně výsledku podle úspěšnosti přihlášení
        if success:
            result_window.title("Úspěch")
            message = "Přihlášení bylo úspěšné."
        else:
            result_window.title("Chyba")
            message = "Zadal jste špatné údaje."
        # Vytvoření a umístění textového štítku s výsledkem přihlášení
        result_label = tk.Label(result_window, text=message, bg="#B0B0E0")
        result_label.pack(pady=(20, 0))
        # Vytvoření tlačítka OK a přiřazení akce podle úspěšnosti přihlášení
        if success:
            ok_button = tk.Button(result_window, text="OK",
                                  command=lambda: self.open_management_window(root, result_window, employee_dict,
                                                                              login_window))
        else:
            ok_button = tk.Button(result_window, text="OK", command=result_window.destroy)
        # Umístění tlačítka OK
        ok_button.pack(pady=(10, 0))
        # Přiřazení událostí tlačítku OK (změna barvy pozadí při najetí myší zmáčknutí a opuštění tlačítka)
        ok_button.bind("<Enter>", self.on_enter)
        ok_button.bind("<Leave>", self.on_leave)
        ok_button.bind("<Button-1>", self.on_click)

    def open_management_window(self, root, result_window, employee_dict, login_window):
        """
        Otevře řídící okno a zavře přihlašovací a výsledkové okno.

        :param root: hlavní okno aplikace
        :param result_window: výsledkové okno
        :param employee_dict: slovník s informacemi o zaměstnanci
        :param login_window: přihlašovací okno
        """
        # Zničení výsledkového okna uvolnění prostředků
        result_window.destroy()
        # Zničení přihlašovacího okna uvolnění prostředků
        login_window.destroy()
        # Skrytí hlavního okna aplikace
        root.withdraw()
        # Vytvoření a otevření řídícího okna se zaměstnancem který se přihlásil
        management.Management.create_management_window(self.window_open, employee_dict, root)
