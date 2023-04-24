import tkinter as tk
from login import Login
from register import Register


def on_enter(event):
    """
    Tato funkce se zavolá, když kurzor myši najede na tlačítko (widget).
    :param event:
    :return:
    """
    event.widget.config(bg="#999999")

def on_leave(event):
    """
    Tato funkce se zavolá, když kurzor myši opustí tlačítko (widget).
    :param event:
    :return:
    """
    event.widget.config(bg="SystemButtonFace")

class StartApp:
    """
    Třída StartApp je hlavní třída aplikace, která obsahuje metodu pro spuštění hlavního okna aplikace.
    """
    def __init__(self, window_open):
        """
        Inicializace třídy StartApp.

        Parametry:
        window_open (object): Instance třídy WindowOpen, která obsahuje metody pro otevření jednotlivých oken.
        """
        self.window_open = window_open
        self.login = Login(self.window_open)
        self.register = Register(self.window_open)
        self.window_open.login = self.login
        self.window_open.register = self.register

    def app(self):
        """
        Metoda pro spuštění hlavního okna aplikace. Vytváří tlačítka pro přihlášení a registraci a umožňuje
        otevření okna pro přihlášení nebo registraci při stisknutí příslušného tlačítka.

        Návratová hodnota:
        root (tkinter.Tk): Instance hlavního okna aplikace.
        """
        root = tk.Tk()
        root.title("Hlavní okno")
        self.window_open.center_window(root)

        root.geometry("240x120")
        root.config(bg="#B0B0E0")

        login_button = tk.Button(root, text="Přihlásit se",
                                 command=lambda: self.window_open.open_login_window(root),
                                 activebackground="#999999")
        login_button.pack(pady=10)
        login_button.config(height=1, width=12)
        login_button.bind("<Enter>", on_enter)
        login_button.bind("<Leave>", on_leave)

        register_button = tk.Button(root, text="Registrovat se",
                                    command=lambda: self.window_open.open_register_window(root),
                                    activebackground="#999999")
        register_button.pack(pady=10)
        register_button.config(height=1, width=12)
        register_button.bind("<Enter>", on_enter)
        register_button.bind("<Leave>", on_leave)

        return root