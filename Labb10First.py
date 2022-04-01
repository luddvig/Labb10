from LinkedQFile import LinkedQ
from molgrafik import *
from HashStuff import *
"""
*Bygg syntaxträd mha allmänt träd med pekare next och down

*Funktionen readgroup skapar först en tomruta objekt. rutan=Ruta(). Anropa readatom och readnum för att sätta in värden
på atom och num. 
Om det är en parentesgrupp ska readgroups anrop till readmol returnera en delmolekyl som sätts under rutan.down

*När readgroup är klar returnerar den rutan till anropet mol = readgroup() som görs allra först i readmol. 
Vad som ska göras med mol.next får du själv tänka ut. 

*Slutligen returnerar readmol den färdiga strukturen till readformel som returnerar den till huvudprogrammets anrop
mol = readformel() där mol pekar högst upp till vänster på syntaxträdet.
"""


class Ruta:
    """Klass för ruta i syntaxträd"""
    def __init__(self):
        self.atom = "( )"
        self.num = 1
        self.next = None
        self.down = None

    def __str__(self):
        return str(self.atom) + str(self.num)


class Syntaxfel(Exception):
    pass


def storeMolecule(molecule):
    """Hjälpfuntion för att lägga in molekylnamn i kö"""
    q = LinkedQ()
    for var in molecule:
        q.enqueue(var)
    return q


def readformel(q):
    """Startar första syntaxkontroll
       Returnerar mol som rutobjekt med eventuella next/down förbindelser"""
    mol = readmol(q, False)
    return mol


def readmol(q, startpar):
    """Kollar molekyl. Startpar=True om startparentes tidigare påträffats i grupp, annas False.
       Returnerar mol som rutobjekt med eventuella next/down förbindelser"""
    mol = readgroup(q)
    if not q.isEmpty() and q.peek() == ")" and startpar:    # Om slutpar påträffas sedan tidigare påträffad startpar
        return mol
    if not q.isEmpty():
        mol.next = readmol(q, startpar)                     # Läser nästa molekyl, ansätter till next för nuvarande
    return mol


def readgroup(q):
    """Kollar grupp i molekyl. Grupp måste starta med stor bokstav eller öppen parentes."""
    rutan = Ruta()                                          # Skapar rutobjekt
    if not q.isEmpty() and q.peek().isalpha():              # Stor och eventuellt liten bokstav, dvs atom
        rutan.atom = readatom(q)                            # Ansätter atomnamn som atom för rutobjekt
        if not q.isEmpty() and q.peek().isnumeric():        # Läser eventuell siffra efter atom
            rutan.num = readNum(q)                          # Ansätter nummer som num för rutobjekt

    elif not q.isEmpty() and q.peek() == "(":               # Startparentes, påträffad molekyl
        rutan.atom = q.dequeue()                            # Ansätter startpar som atom för rutobjekt
        rutan.down = readmol(q, True)                       # Kallar på readmol för att läsa påträffad molekyl
                                                            # Ansätter molekyl som down för rutobjekt
        if q.isEmpty():
            raise Syntaxfel("Saknad högerparentes vid radslutet ")  # Fall då slutparentes saknas
        if not q.isEmpty() and q.peek() == ")":
            rutan.atom = rutan.atom + q.dequeue()           # Adderar slutpar till rutobjekts atom
            if not q.isEmpty() and q.peek().isnumeric():
                rutan.num = readNum(q)                      # Ansätter nummer som num för rutobjekt
            else:
                raise Syntaxfel("Saknad siffra vid radslutet ")     # Fall då siffra efter slutparentes saknas

    else:
        raise Syntaxfel("Felaktig gruppstart vid radslutet ")       # Om ej atom eller startpar
    return rutan


def readatom(q):
    """Läser atom. Består av Stor och eventuell liten bokstav."""
    atoms = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
                 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
                 'Rb',
                 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
                 'Cs',
                 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf',
                 'Ta',
                 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
                 'Pa',
                 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs',
                 'Mt',
                 'Ds', 'Rg', 'Cn', 'Fl', 'Lv']
    cap = readCap(q)                                # Läser stor bokstav
    atom = cap
    if not q.isEmpty() and q.peek().islower():
        small = readSmall(q)                        # Läser liten bokstav
        atom = cap + small
    if atom not in atoms:
        raise Syntaxfel("Okänd atom vid radslutet ")    # Kollar om korrekt atom
    return atom


def readCap(q):
    """Läser bokstav, dequeue om stor, annars raise Syntaxfel."""
    if not q.isEmpty() and q.peek().isupper():
        return q.dequeue()
    if q.isEmpty() or not q.peek().isupper():
        raise Syntaxfel("Saknad stor bokstav vid radslutet ")


def readSmall(q):
    """Läser bokstav, dequeue om liten."""
    if not q.isEmpty() and q.peek().islower():
        return q.dequeue()


def readNum(q):
    """Läser nummer, måste vara större än 1, ex H2."""
    num = ""
    if not q.isEmpty() and q.peek() == "0":                     # Om nummer=0
        q.dequeue()
        raise Syntaxfel("För litet tal vid radslutet ")
    if not q.isEmpty() and q.peek() == "1":                     # Om nummer=1
        if q.isEmpty() or not q.isEmpty() and not q.peek().isnumeric():
            q.dequeue()
            raise Syntaxfel("För litet tal vid radslutet ")
    while not q.isEmpty() and q.peek().isnumeric():             # Dequeuear alla siffror i nummer
        num = num + q.dequeue()
    return int(num)                                             # Vill ha int för rutobjekt


def weight(mol):
    """Beräknar vikt för molekyl rekursivt.
       Rekursiv tanke: Molekylens vikt är lika med vikten för första gruppen + resterande molekyls vikt
                       Resterande molekyls vikt är lika med vikten för andra gruppen + resterande molekyls vikt
                       Osv...
       Basfall: Vi är vid sista gruppen i molekylen, resterande molekyl enl ovan är None."""
    if mol.next != None:                    # Om det finns en grupp till höger
        vikt = weight(mol.next)
        if mol.down == None:
            vikt = vikt + atomHashtable.search(mol.atom).getvikt() * mol.num
            return vikt                     # Nuvarande grupp + resterande molekyls vikt
        else:
            downWe = weight(mol.down)       # Om molekyl
            vikt = vikt + mol.num*downWe    # Nuvarande grupp + resterande molekyls vikt
            return vikt
    elif mol.down != None:                  # Om molekyl
        downWe = weight(mol.down)
        vikt = mol.num*downWe
        return vikt                         # Nuvarande grupp vikt
    else:
        vikt = atomHashtable.search(mol.atom).getvikt() * mol.num
        return vikt                         # Nuvarande grupp vikt



def checkMoleculeSyntax():
    """Kontrollerar om angiven molekyl följer syntax"""
    while True:
        uinput = input()
        if uinput == "#":
            break
        q = storeMolecule(uinput)
        try:
            mol = readformel(q)
            print(f"Vikt {uinput}: {weight(mol)}")
            mg = Molgrafik()
            mg.show(mol)
        except Syntaxfel as error:                    # Fångar fel i syntax
            print(str(error) + str(q))                # Skriver ut  fel


if __name__ == "__main__":
    checkMoleculeSyntax()

