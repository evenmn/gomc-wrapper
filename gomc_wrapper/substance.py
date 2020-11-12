class Substance:
    def __init__(self):
        pass


class TIP3P(Substance):
    def __init__(self):
        self.atom_labels = ['O', 'H1', 'H2']
        self.atom_types = ['O', 'H', 'H']
        self.masses = {'O': 15.9994, 'H': 1.0079}
        self.charges = {'O': -1.128, 'H': 0.5564}
        self.bonds = {'O,H1': 0.9572, 'O,H2': 0.9572}
        self.angles = {'H1,O,H2': 104.72}


class TIP4P2005(Substance):
    def __init__(self):
        self.atom_labels = ['O', 'H1', 'H2', 'M']
        self.atom_types = ['O', 'H', 'H', 'M']
        self.masses = {'O': 15.9994, 'H': 1.0079, 'M': 0.0}
        self.charges = {'O': 0.0, 'H': 0.5564, 'M': -1.128}
        self.bonds = {'O,H1': 0.9572, 'O,H2': 0.9572, 'O,M': 0.1546}
        self.angles = {'H1,O,H2': 104.52, 'H1,O,M': 52.26, 'H2,O,M': 52.26}
