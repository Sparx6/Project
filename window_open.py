class WindowOpen:
    """
    Třída pro ovládání oken pro přihlašování a registraci uživatelů.
    """
    def __init__(self):
        """
               Inicializace proměnných pro login a register.
        """
        self.login = None
        self.register = None

    def open_login_window(self, root, register_window=None):
        """
        Otevře okno pro přihlášení a zavře okno pro registraci, pokud je otevřeno.

        :param:
        root (tkinter.Tk): Hlavní okno aplikace.
        register_window (tkinter.Toplevel, volitelné): Okno pro registraci.
        """
        if register_window:
            register_window.destroy()
        self.login.create_login_window(root)

    def open_register_window(self, root, login_window=None):
        """
        Otevře okno pro registraci a zavře okno pro přihlášení, pokud je otevřeno.

        :param:
        root (tkinter.Tk): Hlavní okno aplikace.
        login_window (tkinter.Toplevel, volitelné): Okno pro přihlášení.
        """
        if login_window:
            login_window.destroy()
        self.register.create_register_window(root)

    def center_window(self, window):
        """
        Centruje okno na střed obrazovky.

        :param:
        window (tkinter.Toplevel): Okno, které chceme vycentrovat.
        """
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_reqwidth()
        window_height = window.winfo_reqheight()
        x_coordinate = int((screen_width/2) - (window_width/2))
        y_coordinate = int((screen_height/2) - (window_height/2))
        window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
