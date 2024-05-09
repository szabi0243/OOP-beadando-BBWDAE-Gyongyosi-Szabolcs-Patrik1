import random
from datetime import datetime, date

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []
        self.szabad_szobak = []
    
    def szoba_hozzaadasa(self, szoba):
        self.szobak.append(szoba)
        self.szabad_szobak.append(szoba)
    
    def foglalas_szoba_datum_ar_alapjan(self, datum):
        foglalhato_szobak = [szoba for szoba in self.szabad_szobak if isinstance(szoba, (EgyagyasSzoba, KetagyasSzoba))]
        foglalasok = []
        for szoba in foglalhato_szobak:
            foglalasok.append(Foglalas(szoba, datum))
        self.foglalasok.extend(foglalasok)
        for foglalas in foglalasok:
            self.szabad_szobak.remove(foglalas.szoba)
        return foglalasok
    
    def foglalas_lemondasa(self, foglalas_idx):
        if 1 <= foglalas_idx <= len(self.foglalasok):
            foglalas = self.foglalasok[foglalas_idx - 1]
            self.foglalasok.remove(foglalas)
            self.szabad_szobak.append(foglalas.szoba)
            return f"A foglalás a {foglalas.datum} dátumra le lett mondva."
        else:
            return "Hibás foglalás sorszám. Kérem válasszon újra."

    def osszes_foglalas_listazasa(self):
        if self.foglalasok:
            print("Összes foglalás:")
            for i, foglalas in enumerate(self.foglalasok, start=1):
                print(f"{i}. {foglalas.foglalas_jellemzese()}")
        else:
            print("Nincsenek foglalások a szállodában.")
    
    def szobak_allapota(self):
        print("Szobák állapota:")
        for szoba in self.szobak:
            allapot = "Foglalt" if szoba not in self.szabad_szobak else "Szabad"
            print(f"{szoba.jellemzok()}, Állapot: {allapot}")

class Szoba:
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    def jellemzok(self):
        return f"Szobaszám: {self.szobaszam}, Ár: {self.ar} Ft"

class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam, minibar=False):
        super().__init__(ar, szobaszam)
        self.minibar = minibar

    def jellemzok(self):
        return f"Egyágyas szoba, {super().jellemzok()}"

class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam, erkely=False):
        super().__init__(ar, szobaszam)
        self.erkely = erkely

    def jellemzok(self):
        return f"Kétágyas szoba, {super().jellemzok()}"

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

    def foglalas_jellemzese(self):
        return f"Szoba száma: {self.szoba.szobaszam}, Foglalás dátuma: {self.datum}"

def main():
    szalloda = Szalloda("Példa Szálloda")

# Hozzáadunk 5 egyágyas és 5 kétágyas szobát a szállodához
    for _ in range(5):
        egyagyas_szoba = EgyagyasSzoba(random.randint(10000, 50000), random.randint(100, 999), minibar=True)
        ketagyas_szoba = KetagyasSzoba(random.randint(10000, 50000), random.randint(1000, 1999), erkely=True)
        szalloda.szoba_hozzaadasa(egyagyas_szoba)
        szalloda.szoba_hozzaadasa(ketagyas_szoba)

    # Felhasználói interakció
    today = date.today()
    while True:
        print("\nVálasszon műveletet:")
        print("1. Foglalás")
        print("2. Lemondás")
        print("3. Összes foglalás listázása")
        print("4. Szobák állapotának lekérdezése")
        print("5. Kilépés")

        valasztas = input("Kérem válasszon (1-5): ")

        if valasztas == "1":
            datum = input("Kérem adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
            try:
                foglalas_datum = datetime.strptime(datum, "%Y-%m-%d").date()
            except ValueError:
                print("Hibás dátumformátum. Kérem adja meg a dátumot helyesen (YYYY-MM-DD formátumban).")
                continue
            if foglalas_datum < today:
                print("Csak a mai vagy későbbi dátumokra lehet foglalni.")
                continue
            foglalasok = szalloda.foglalas_szoba_datum_ar_alapjan(foglalas_datum)
            if foglalasok:
                print(f"A {datum} dátumra foglalható szobák:")
                for i, foglalas in enumerate(foglalasok, start=1):
                    print(f"{i}. {foglalas.szoba.jellemzok()}")
                szobaszam = input("Kérem válasszon szobaszámot: ")
                for foglalas in foglalasok:
                    if foglalas.szoba.szobaszam == int(szobaszam):
                        print(f"Ön sikeresen lefoglalta a {foglalas.szoba.jellemzok()} szobát a {datum} dátumra.")
                        break
                else:
                    print("Hibás szobaszám. Kérem válasszon újra.")
            else:
                print("Nincsenek szabad szobák a megadott dátumra.")
        elif valasztas == "2":
            if not szalloda.foglalasok:
                print("Nincsenek foglalások a szállodában.")
                continue
            foglalas_idx = int(input("Kérem adja meg a lemondani kívánt foglalás sorszámát: "))
            print(szalloda.foglalas_lemondasa(foglalas_idx))
        elif valasztas == "3":
            szalloda.osszes_foglalas_listazasa()
        elif valasztas == "4":
            szalloda.szobak_allapota()
        elif valasztas == "5":
            print("Kilépés...")
            break
        else:
            print("Nem érvényes választás. Kérem válasszon újra.")

if __name__ == "__main__":
    main()