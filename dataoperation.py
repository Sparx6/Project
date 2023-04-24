from conn import DatabaseConnection

class DataOperations:
    """
    Třída DataOperations obsahuje metody pro získávání informací z databáze.
    """
    def __init__(self):
        """
        Inicializace třídy DataOperations.
        Vytvoří připojení k databázi pomocí třídy DatabaseConnection.
        """
        self.db_connection = DatabaseConnection().connect_to_database()


    def get_stock_status(self):
        """
        Metoda get_stock_status získává stav skladu pro každý produkt.
        Returns:
        list: Seznam slovníků obsahujících informace o skladech a produktech.

        """
        cursor = self.db_connection.cursor(dictionary=True)
        query = '''
            SELECT s.nazev, s.adresa, sp.produkt_id, p.nazev as nazev_produktu, sp.mnozstvi
            FROM sklad s
            JOIN sklad_produkt sp ON s.id = sp.sklad_id
            JOIN produkt p ON sp.produkt_id = p.id
            ORDER BY s.nazev, p.nazev;
        '''
        cursor.execute(query)
        return cursor.fetchall()

    def get_store_status(self):
        """
        Metoda get_store_status získává stav obchodů pro každý produkt.

        Returns:
        list: Seznam slovníků obsahujících informace o obchodech a produktech.
        """
        cursor = self.db_connection.cursor(dictionary=True)
        query = '''
            SELECT o.nazev, o.adresa, op.produkt_id, p.nazev as nazev_produktu, op.mnozstvi
            FROM obchod o
            JOIN obchod_produkt op ON o.id = op.obchod_id
            JOIN produkt p ON op.produkt_id = p.id
            ORDER BY o.nazev, p.nazev;
        '''
        cursor.execute(query)
        return cursor.fetchall()