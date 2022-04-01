

class Node:
    """Noder till klassen Hashtable"""
    def __init__(self, key="", data=None):
        self.key = key          # Nyckel som används vid hashning
        self.data = data        # Objekt som ska hashas in

    def __str__(self):
        return self.data


class Hashtable:
    """Klass för hashtabell"""
    def __init__(self, size):
        """Size: hashtabellens storlek"""
        self.size = size
        self.tabell = [[] for i in range(self.size)]    # Skapar lista med listor på varje index 0-size

    def store(self, key, data):
        """key: nyckel. data: objekt som ska lagras"""
        new_node = Node(key, data)                      # Skapar Nod-objekt som ska läggas in
        self.tabell[self.hashfunction(key) % self.size].append(new_node)  # Hashar index av nyckel, appendar nod i lista

    def search(self, key):
        """key: nyckel. Hämtar det objekt som finns lagrat med nyckeln "key" och returnerar det.
         Om "key" inte finns ges Exception, KeyError """
        data = self.tabell[self.hashfunction(key) % self.size]  # Hämtar lista på index för angiven key
        found = False       # Initierar att objektet ej hittats
        for nod in data:
            if nod.key == key:  # Itererar genom listan, söker efter nod med överrensstämmande nyckel
                found = True        # Ändrar till att objektet hittats
                true_node = nod     # Sparar den hittade noden
        if found:
            return true_node.data   # Returnerar den hittade noden
        else:
            raise KeyError(key)     # Om noden inte hittats (dvs om found fortfarande är False), ges KeyError

    def hashfunction(self, key):
        """key: nyckel. Hashar värde för key"""
        resultat = 0
        for i in key:
            resultat = resultat * 32 + (ord(i)**2)
        return resultat

