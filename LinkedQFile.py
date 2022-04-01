import unittest

class Node:
    """Hjälpklass för att skapa en nod, har instansvariabler value och next"""
    def __init__(self, value, next=None):
        self.value = value    # Något value. Inte privata, vill manipulera dessa i klasserna för kö.
        self.next = next      # För att länka ihop flera Node-objekt

class LinkedQ:
    """Klass för kö. Är alltid tom när den skapas, ingen fördefinierad instansvariabel"""
    def __init__(self):
        self.__first = None       # Skapar privata instansvariabel first. Håller reda på first i kön. Tom från början.
        self.__last = None        # Samma för last.

    def __str__(self):
        tmp = self.__first
        items = list()
        while tmp != None:
            items.append(str(tmp.value))
            tmp = tmp.next
        return "".join(items)

    def peek(self):
        """Metod för att veta vilken nod som är längst fram i kön. Tar ingen parameter. Returnera value för first"""
        if self.isEmpty():
            return None
        else:
            return self.__first.value

    def size(self):
        """Metod för att räkna antal noder i kön. Tar ingen parameter. Returnerar antal noder."""
        if self.isEmpty():
            return 0
        else:
            tmp = self.__first
            i = 1
            while tmp.next != None:
                tmp = tmp.next
                i += 1
            return i

    def enqueue(self, value):
        """Metod för att lägga till nod. Läggs till efter last. Last flyttas till next, dvs den tillagda noden"""
        # Tar in parameter value för noden som ska läggas till. Returnerar inget.
        tmp = Node(value)                       # Anropar Node och skapar ett objekt med value.
        if self.isEmpty():
            self.__first = self.__last = tmp    # Om det är första noden i kön ansätts den som first och last.
        else:
            self.__last.next = tmp    # Next för köns last flyttas till den nya noden.
            self.__last = tmp         # Flyttar last till den tillagda noden.

    def isEmpty(self):
        """Metod för att undersöka om kön är tom. Returnerar boolean."""
        return self.__first == None

    def dequeue(self):
        """Metod för att ta bort noden längst fram i kön. value från first lagras. First flyttas sedan till next."""
        # Tar ingen parameter. Returnerar value för borttagen nod.
        if self.isEmpty():
            return None                         # Om kön är tom returneras None.
        else:
            tmp = self.__first.value            # Lagrar value från first.
            self.__first = self.__first.next    # Flyttar first till next.
            return tmp                          # Returnerar value


class TestQueue(unittest.TestCase):
    """Test för klassen LinkedQ"""
    def test_isEmpty(self):
        #isEmpty ska returnera True för tom kö, False annars
        q = LinkedQ()
        self.assertTrue(q.isEmpty(), "isEmpty på tom kö")
        q.enqueue(17)
        self.assertFalse(q.isEmpty(), "isEmpty på icke-tom kö")

    def test_order(self):
        #Kontrollerar att kö-ordningen blir rätt
        q = LinkedQ()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)


if __name__ == "__main__":
    unittest.main()