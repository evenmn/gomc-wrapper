class Substance:
    def __init__(self):
        pass


class TIP3P(Substance):
    def __init__(self):
        self.atom_labels = ['O', 'H1', 'H2']
        self.atom_types = ['O', 'H', 'H']
        self.bond_types = ['OH']
        self.masses = {'O': 15.9994, 'H': 1.0079}
        self.charges = {'O': -1.128, 'H': 0.5564}
        self.bonds = {'O,H1': 0.9572, 'O,H2': 0.9572}
        self.angles = {'H1,O,H2': 104.72}

    def __repr__(self):
        return "TIP3P"


class TIP4P2005(Substance):
    def __init__(self):
        self.atom_labels = ['O1', 'H1', 'H2', 'M1']
        self.atom_types = ['O', 'H', 'H', 'M']
        self.bond_types = ['OH', 'OM']
        self.masses = {'O': 15.9994, 'H': 1.0079, 'M': 0.0}
        self.charges = {'O': 0.0, 'H': 0.5564, 'M': -1.1128}
        self.bonds = {'O1,H1': 0.9572, 'O1,H2': 0.9572, 'O1,M1': 0.1546}
        self.angles = {'H1,O1,H2': 104.52, 'H1,O1,M1': 52.26, 'H2,O1,M1': 52.26}
        self.lj_params = {'OO': {'epsilon': 0.1852, 'sigma': 3.1589},
                          'OH': {'epsilon': 0.0000, 'sigma': 0.0000},
                          'HH': {'epsilon': 0.0000, 'sigma': 0.0000}}
        self.gomc_params = {'Rcut': 8.5, 'LRC': True, 'Exclude': '1-4',
                            'Potential': 'VDW', 'ElectroStatic': True,
                            'Ewald': True, 'CachedFourier': True,
                            'Tolerance': 1e-5, 'RcutLow': 1.0}

    def __repr__(self):
        return "TIP4P/2005"

    def set_parameters(self, Z_H, r0, OM, theta, epsilon, sigma):
        """Set TIP4P parameters
        """
        self.charges['H'] = Z_H
        self.charges['M'] = - 2 * Z_H
        self.bonds['O,H1'] = r0
        self.bonds['O,H2'] = r0
        self.bonds['O,M'] = OM
        self.angles['H1,O,H2'] = theta
        self.angles['H1,O,M'] = theta/2
        self.angles['H2,O,M'] = theta/2
        self.lj_params['OO']['epsilon'] = epsilon
        self.lj_params['OO']['sigma'] = sigma
