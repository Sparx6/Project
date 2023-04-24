from start import StartApp
from window_open import WindowOpen
def main():
    """
    Hlavní funkce aplikace, která inicializuje a spouští GUI.

    """
    # Vytvoření instance třídy WindowOpen pro správu otevřených oken
    window_open = WindowOpen()
    # Vytvoření instance třídy StartApp pro zahájení aplikace
    start_app = StartApp(window_open)
    # Inicializace hlavního okna aplikace
    root = start_app.app()
    # Spuštění hlavní smyčky aplikace
    root.mainloop()

if __name__ == "__main__":
    # Spuštění hlavní funkce aplikace
    main()