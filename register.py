import tkinter as tk
from conn import DatabaseConnection
import re
from tkinter import messagebox

class Register:
    """
    Třída pro registraci uživatele v aplikaci. Obsahuje metody pro validaci vstupních dat,
    registraci uživatele a vytvoření okna pro registraci.
    """

    def __init__(self, window_open):
        """
        Inicializuje instanci třídy Register s odkazem na instanci třídy pro správu oken.
        """
        self.window_open = window_open

    def is_valid_input(self, name, surname, username, password):
        """
        Ověřuje, zda zadané jméno, příjmení, uživatelské jméno a heslo splňují požadavky.
        Vrací dvojici (True, '') pokud jsou vstupy platné, jinak dvojici (False, 'chybová zpráva').
        """

        name_pattern = r'^[a-zA-Zá-žÁ-Ž]{3,}$'
        username_pattern = r'^[a-zA-Z0-9]{3,}$'
        password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if not re.match(name_pattern, name) or not re.match(name_pattern, surname):
            return False, 'Křestní jméno a příjmení musí mít alespoň 3 znaky a obsahovat pouze písmena české abecedy.'
        if not re.match(username_pattern, username):
            return False, 'Uživatelské jméno musí mít alespoň 3 znaky a obsahovat pouze znaky anglické abecedy a čísla.'
        if not re.match(password_pattern, password):
            return False, 'Heslo musí mít alespoň 8 znaků, obsahovat minimálně jedno velké písmeno, jedno malé písmeno, jednu číslici a jeden speciální znak.'

        return True, ''

    def register_user(self, register_window, name, surname, username, password):
        """
        Registruje uživatele do databáze, pokud jsou zadané údaje platné. Zobrazuje chybové nebo úspěšné
        hlášení v závislosti na výsledku operace.
        """
        is_valid, error_msg = self.is_valid_input(name, surname, username, password)
        if not is_valid:
            tk.messagebox.showerror("Chyba", error_msg, parent=register_window)
            return

        connection = DatabaseConnection().connect_to_database()
        cursor = connection.cursor()

        query = """
        INSERT INTO zamestnanec (jmeno, prijmeni, uzivatelske_jmeno, heslo)
        VALUES (%s, %s, %s, %s)
        """

        try:
            cursor.execute(query, (name, surname, username, password))
            connection.commit()
            tk.messagebox.showinfo("Úspěch", "Úspěšně jste se zaregistrovali.", parent=register_window)
        except:
            tk.messagebox.showerror("Chyba", "Registrace se nezdařila.", parent=register_window)
        finally:
            cursor.close()
            connection.close()

    def create_register_window(self, root):
        """
        Vytváří okno pro registraci uživatele s formulářem pro zadání potřebných údajů.
        """
        register_window = tk.Toplevel(root)
        register_window.title("Registrace")
        register_window.attributes('-topmost', True)
        self.window_open.center_window(register_window)
        register_window.geometry("300x300")
        register_window.configure(bg="#B0B0E0")

        name_label = tk.Label(register_window, text="Křestní jméno:", bg="#B0B0E0")
        name_label.pack(pady=(10, 0))
        name_entry = tk.Entry(register_window)
        name_entry.pack(pady=(0, 10))

        surname_label = tk.Label(register_window, text="Přijmení:", bg="#B0B0E0")
        surname_label.pack(pady=(10,0))
        surname_entry = tk.Entry(register_window)
        surname_entry.pack(pady=(0, 10))
        username_label = tk.Label(register_window, text="Uživatelské jméno:", bg="#B0B0E0")
        username_label.pack(pady=(10, 0))
        username_entry = tk.Entry(register_window)
        username_entry.pack(pady=(0, 10))

        password_label = tk.Label(register_window, text="Heslo:", bg="#B0B0E0")
        password_label.pack(pady=(0, 0))
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack(pady=(0, 10))

        register_button = tk.Button(register_window, text="Registrovat se",
                                    command=lambda: self.register_user(register_window, name_entry.get(),
                                                                       surname_entry.get(),
                                                                       username_entry.get(), password_entry.get()))
        register_button.pack(pady=(0, 0))

        register_button.bind("<Enter>", self.on_enter)
        register_button.bind("<Leave>", self.on_leave)
        register_button.bind("<Button-1>", self.on_click)

        login_label = tk.Label(register_window, text="Přihlásit se", bg="#B0B0E0", fg="blue", cursor="hand2")
        login_label.pack(pady=10)
        login_label.bind("<Button-1>", lambda event: self.window_open.open_login_window(root, register_window))

    def on_enter(self, event):
        """
        Změní barvu pozadí tlačítka na šedou, když na něj najede kurzor myši.
        """
        event.widget.config(bg="#999999")

    def on_leave(self, event):
        """
        Změní barvu pozadí tlačítka zpět na výchozí barvu tlačítek systému, když kurzor myši opustí tlačítko.
        """
        event.widget.config(bg="SystemButtonFace")

    def on_click(self, event):
        """
        Změní barvu pozadí tlačítka na šedou, když je tlačítko stisknuto.
        """
        event.widget.config(bg="#999999", activebackground="#999999")