import mysql.connector
import configparser

class DatabaseConnection:
    """
    Třída DatabaseConnection slouží k připojení k databázi pomocí hodnot uložených v konfiguračním souboru config.ini.
    """

    def __init__(self):
        """
        V konstruktoru třídy inicializujeme configparser a načítáme hodnoty z config.ini souboru.
        """
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    def connect_to_database(self):
        """
        Metoda connect_to_database vytváří spojení s databází pomocí načtených hodnot z config.ini souboru
        a vrací vytvořené spojení.
        """
        connection = mysql.connector.connect(
            host=self.config.get("database", "host"),
            user=self.config.get("database", "user"),
            password=self.config.get("database", "password"),
            database=self.config.get("database", "database"),
        )

        return connection