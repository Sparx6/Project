import tkinter as tk
from tkinter import ttk
from product_show import ProductData
from dataoperation import DataOperations
from product_window import ProductWindows
from warehouse_window import WarehouseWindows
from store_window import StoreWindows
from supplier_window import SupplierManagement
from info_show import InformationDisplays
from management_show import ManagementShow
from customer_window import CustomerWindows
from order_window import OrderWindows
from exporting import ExportInformation
class Management:
    """
    Třída Management je zodpovědná za správu hlavního okna aplikace
    """

    def __init__(self, window_open, employee_dict, db_connection):
        """
        Inicializace třídy Management, která řídí hlavní okno aplikace pro správu.

        :param window_open: instance třídy WindowOpen pro správu otevřených oken
        :param employee_dict: slovník s informacemi o zaměstnanci
        :param db_connection: instance třídy pro připojení k databázi
        """
        self.window_open = window_open
        self.employee_dict = employee_dict
        self.db_connection = db_connection
        self.data_operations = DataOperations()
        self.content_frame = None
        self.management_show = None
        self.product_data_instance = db_connection
    def set_management_window_size(self, root):
        """
        Nastaví velikost a umístění hlavního okna aplikace.

        :param root: hlavní okno aplikace
        """
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 1000
        window_height = 800
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def set_db_connection(self, db_connection):
        """
        Nastaví instanci třídy pro připojení k databázi.

        :param db_connection: instance třídy pro připojení k databázi
        """
        self.db_connection = db_connection

    @staticmethod
    def create_management_window(window_open, employee_dict, start_window):
        """
        Vytvoří a zobrazí hlavní okno aplikace pro správu.

        :param window_open: instance třídy WindowOpen pro správu otevřených oken
        :param employee_dict: slovník s informacemi o zaměstnanci
        :param start_window: hlavní okno aplikace
        """
        root = tk.Tk()
        root.title("Správa")
        root.minsize(1000, 800)
        root.configure(bg="#B0B0E0")
        product_data_instance = ProductData()
        app = Management(window_open, employee_dict, product_data_instance)
        app.set_management_window_size(root)
        app.create_navigation(root)
        app.management_show = ManagementShow(app.content_frame, app.db_connection, employee_dict)

        root.protocol("WM_DELETE_WINDOW", lambda: [start_window.deiconify(), root.destroy()])
        root.mainloop()

    def create_navigation(self, root):
        """
        Vytvoří navigaci a obsah hlavního okna aplikace pro správu.

        :param root:hlavní okno aplikace
        """

        main_frame = tk.Frame(root, bg="#B0B0E0", padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        menu_frame = tk.Frame(main_frame, bg="#B0B0E0", width=200, bd=1, relief=tk.SUNKEN)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = tk.Frame(main_frame, bg="#B0B0E0", bd=1, relief=tk.SUNKEN)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.management_show = ManagementShow(self.content_frame, self.db_connection, self.employee_dict)
        menu_label = tk.Label(menu_frame, text="Menu", font=("Helvetica", 16), bg="#B0B0E0")
        menu_label.pack(pady=(20, 10))
        # Vytvoření tlačítek pro navigaci a přiřazení příslušné funkce
        my_profile_button = ttk.Button(menu_frame, text="Můj Profil", command=self.management_show.show_employee_info)
        my_profile_button.pack(pady=(10, 0))

        show_products_button = ttk.Button(menu_frame, text="Zobrazit produkty",
                                          command=self.management_show.show_products)
        show_products_button.pack(pady=(10, 0))

        close_button = ttk.Button(menu_frame, text="Zavřít obsah", command=self.clear_content)
        close_button.pack(side=tk.BOTTOM, pady=(0, 10))

        edit_products_button = ttk.Button(menu_frame, text="Úprava produktů",
                                          command=lambda: self.product_data_instance.show_products_buttons(
                                              self.content_frame))
        edit_products_button.pack(pady=(10, 0))

        stock_status_button = ttk.Button(menu_frame, text="Stav Skladů", command=self.management_show.show_stock_status)
        stock_status_button.pack(pady=(10, 0))

        store_status_button = ttk.Button(menu_frame, text="Stav Obchodů",
                                         command=self.management_show.show_store_status)
        store_status_button.pack(pady=(10, 0))

        product_windows_instance = ProductWindows(self.content_frame)

        product_management_button = ttk.Button(menu_frame, text="Správa produktů",
                                               command=product_windows_instance.show_product_management_buttons)
        product_management_button.pack(pady=(10, 0))

        customer_management_button = ttk.Button(menu_frame, text="Správa zákazníků",
                                                command=self.show_customer_management_buttons)
        customer_management_button.pack(pady=(10, 0))

        order_management_button = ttk.Button(menu_frame, text="Správa objednávek",
                                             command=self.show_order_management_buttons)
        order_management_button.pack(pady=(10, 0))

        warehouse_button = ttk.Button(menu_frame, text="Úprava skladů", command=self.show_warehouse_frame)
        warehouse_button.pack(pady=(10, 0))

        store_button = ttk.Button(menu_frame, text="Úprava obchodů", command=self.show_store_frame)
        store_button.pack(pady=(10, 0))

        suppliers_button = ttk.Button(menu_frame, text="Dodavatelé", command=self.show_supplier_frame)
        suppliers_button.pack(side=tk.TOP, pady=(10, 0))

        info_button = ttk.Button(menu_frame, text="Výpisy informací", command=self.show_info_frame)
        info_button.pack(side=tk.TOP, pady=(10, 0))

        exports_button = ttk.Button(menu_frame, text="Exporty",
                                    command=lambda: ExportInformation.show_export_frame(self.content_frame))
        exports_button.pack(pady=(10, 0), padx=(0, 10))

    def clear_content(self):
        """
        Tato metoda vymaže všechny widgety v rámci obsahu.
        :param: self
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def clear_content_frame(self):
        """
        Tato metoda vymaže všechny widgety v rámci obsahu.
        :param: self
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_warehouse_frame(self):
        """
        Tato metoda vymaže obsahový rámec a zobrazí rámec správy skladu.
        :param: self
        """
        self.clear_content()
        WarehouseWindows.show_warehouse_management(self.content_frame)

    def show_store_frame(self):
        """
        Tato metoda vymaže obsahový rámec a zobrazí rámec správy obchodu.
        :param: self
        """
        self.clear_content()
        StoreWindows.show_store_management(self.content_frame)

    def show_supplier_frame(self):
        """
        Tato metoda vymaže obsahový rámec a zobrazí rámec správy dodavatelů.
        :param: self
        """
        self.clear_content()
        SupplierManagement.show_supplier_management(self.content_frame)

    def show_info_frame(self):
        """
        Tato metoda vymaže obsahový rámec a zobrazí rámec informačního zobrazení.
        :param: self
        """
        InformationDisplays.show_info_frame(self.content_frame)

    def show_customer_management_buttons(self):
        """
        Tato metoda zobrazuje tlačítka pro správu zákazníků v obsahovém rámci a přijímá callback funkci 'clear_content'
         jako parametr, která vymaže obsahový rámec.
        :param: self, clear_content
        """
        CustomerWindows.show_customer_management_buttons(self.content_frame, self.clear_content)

    def show_order_management_buttons(self):
        """
        Tato metoda vytváří instanci třídy OrderWindows a zobrazuje tlačítka pro správu objednávek v obsahovém rámci.
        :param: self
        """
        order_windows = OrderWindows(self.content_frame)
        order_windows.show_order_management_buttons()