import os
import datetime
import numpy as np
import pandas as pd
from io import StringIO


def read(filename='in.conf'):
    """Read GOMC parameter file
    """
    from .__init__ import GOMC
    gomc = GOMC()
    with open(filename, 'r') as f:
        for line in f:
            if line[0].isalpha():
                # ignoring all lines that do not start with a letter
                splitted = line.split()
                gomc.set(splitted[0], *tuple(splitted[1:]))
    return gomc


def write(self, filename='in.conf', verbose=True):
    """Write GOMC parameter file
    """
    now = datetime.datetime.now()

    with open(filename, 'w') as f:
        f.write("#" * 30 + "\n")
        f.write("## Written by GOMC-wrapper \n")
        f.write(f"## DATE: {now:%Y-%m-%d %H:%M:%S}\n")
        f.write("#" * 30 + "\n")

        f.write("\n" + "#" * 76 + "\n")
        f.write("# " + "=" * 8 + "-" * 25 + " INPUT " + "-" * 25 + "=" * 8)
        f.write("\n" + "#" * 76 + "\n")

        for key, obj in self.parameters.items():
            if key == "ParaTypeCHARMM" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# FORCEFIELD")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "Coordinates" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# INPUT FILES")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "GEMC":
                f.write("\n" + "#" * 76 + "\n")
                f.write("# " + "=" * 8 + "-" * 25 + " SYSTEM " + "-" * 25 + "=" * 8)
                f.write("\n" + "#" * 76 + "\n")

                if verbose:
                    f.write("\n" + "#" * 36 + "\n")
                    f.write("# GEMC TYPE")
                    f.write("\n" + "#" * 36 + "\n")

            elif key == "Pressure" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# SIMULATION CONDITION")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "ElectroStatic" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# ELECTROSTATIC")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "PressureCalc" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# PRESSURE CALCULATION")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "RunSteps" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# STEPS")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "DisFreq" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# MOVE FREQUENCY")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "CellBasisVector1" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# BOX DIMENSIONS #, X, Y, Z")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "CBMC_First" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# CBMC TRIALS")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "FreeEnergyCalc" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# FREE ENERGY COMPUTATIONS")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "OutputName":
                f.write("\n" + "#" * 76 + "\n")
                f.write("# " + "=" * 8 + "-" * 25 + " OUTPUT " + "-" * 25 + "=" * 8)
                f.write("\n" + "#" * 76 + "\n")

                if verbose:
                    f.write("\n" + "#" * 36 + "\n")
                    f.write("# statistics filename add")
                    f.write("\n" + "#" * 36 + "\n")

            elif key == "CoordinatesFreq" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# enable, frequency")
                f.write("\n" + "#" * 36 + "\n")

            elif key == "OutEnergy" and verbose:
                f.write("\n" + "#" * 36 + "\n")
                f.write("# enable: blk avg., fluct.")
                f.write("\n" + "#" * 36 + "\n")

            if len(obj.values) > 0:
                if obj.multiline:
                    for i in range(len(obj.values)):
                        f.write(key.ljust(20) + " \t")
                        f.write(str(obj) + "\n")
                else:
                    f.write(key.ljust(20) + " \t")
                    f.write(str(obj) + "\n")


def write_topology(filename="topology.inp", atoms=['O', 'H', 'H', 'M'],
                   labels=['O', 'H1', 'H2', 'M'],
                   mass={'O': 15.9994, 'H': 1.0079, 'M': 0.0},
                   charge={'O': 0.0, 'H': 0.5564, 'M': -1.1128},
                   bonds=['OH', 'OM'], molname='TIP4P'):
    """Write topology file
    """
    now = datetime.datetime.now()
    atoms_unique = np.unique(atoms)

    # find total charge
    chargemol = 0
    for atom in atoms:
        chargemol += charge[atom]
    if abs(chargemol) > 1e-6:
        raise Warning("Molecule is not neutral")

    with open(filename, 'w') as f:
        f.write(f"* Custom top file for {molname}\n")
        f.write("* Generated by GOMC-wrapper\n")
        f.write(f"* DATE: {now:%Y-%m-%d %H:%M:%S}\n\n")

        for i, atom in enumerate(atoms_unique):
            f.write(f"MASS{i+1:>5}  {atom:<2}{mass[atom]:>11.4f}  {atom:<2}\n")

        f.write("\nDEFA FIRS NONE LAST NONE\n")
        f.write("AUTOGENERATE ANGLES DIHEDRALS\n")

        f.write(f"\nRESI {molname[:4]}{chargemol:>19.4f}\n")
        f.write("GROUP\n")

        counter = {}
        for key in mass.keys():
            counter[key] = 0

        atom_IDs = []
        for i, atom in enumerate(atoms):
            counter[atom] += 1
            if labels is None:
                proposed_label = atom + str(counter[atom])
                atom_IDs.append(proposed_label)
            else:
                atom_IDs.append(labels[i])
            f.write(f"ATOM {atom_IDs[-1]:<9}{atom:<2}{charge[atom]:>12.4f}\n")

        f.write("BOND    ")
        for i in range(len(atoms)):
            for j in range(len(atoms)):
                for bond in bonds:
                    if atoms[i] == bond[0] and atoms[j] == bond[1]:
                        f.write(f"{atom_IDs[i]:<5}{atom_IDs[j]:<7}")
        f.write("\nPATCHING FIRS NONE LAST NONE\n\nEND\n")


def write_parameter(filename="Par_TIP4P-2020_Charmm.inp", r0=0.9572,
                    theta=104.52, OM=0.1546, epsilon=0.1856, sigma=3.16,
                    symbols={'O': 'O', 'H': 'H', 'M': 'M'}):
    """Write parameter file, type CHARMM
    """
    large = 9999999999
    with open(filename, 'w') as f:
        # write header information
        f.write("* Parameters for TIP4P\n")
        f.write("* Generated by GOMC-wrapper\n\n")

        # write bond information
        temp_bond = "{:<5}{:<5}{:>10}{:10.4f}\n"
        f.write("BONDS\n")
        f.write("!\n")
        f.write("!V(bond) = Kb(b - b0)**2\n")
        f.write("!\n")
        f.write("!   1   2   Kb   b0\n")
        f.write(temp_bond.format(symbols['O'], symbols['H'], large, r0))
        f.write(temp_bond.format(symbols['O'], symbols['M'], large, OM))
        f.write("\n\n")

        # write angle information
        temp_angle = "{:<5}{:<5}{:<5}{:>10}{:10.4f}\n"
        f.write("ANGLES\n")
        f.write("!\n")
        f.write("!V(angle) = Ktheta(Theta - Theta0)**2\n")
        f.write("!\n")
        f.write("!   1   2   3   Ktheta   Theta0\n")
        f.write(temp_angle.format(symbols['H'], symbols['O'], symbols['H'], large, theta))
        f.write(temp_angle.format(symbols['H'], symbols['O'], symbols['M'], large, theta/2))
        f.write("\n\n")

        # write dihedral information
        f.write("DIHEDRALS\n")
        f.write("!\n")
        f.write("!V(dihedral) = Kchi(1 + cos(n(chi) - delta))\n")
        f.write("!\n")
        f.write("!atom types\n")
        f.write("\n\n")

        # write non-bonded information
        temp_nb = "{:<5}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}\n"
        f.write("NONBONDED\n")
        f.write("!\n")
        f.write("!V(Lennard-Jones) = Eps,i,j[(Rmin,i,j/ri,j)**12-2(Rmin,i,j/ri,j)**6]\n")
        f.write("!\n")
        f.write("!   atom   ignored   epsilon   Rmin/2   ignored eps,1-4   Rmin/2,1-4\n")
        f.write(temp_nb.format(symbols['H'], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        f.write(temp_nb.format(symbols['M'], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        f.write(temp_nb.format(symbols['O'], 0.0, -epsilon, sigma/2, 0.0, 0.0, 0.0))


def write_molecule(bonds, angles={}, filename="molecule.pdb", molname='TIP4P'):
    """Write a PDB for a single molecule. Support molecules with two to
    four atoms.

    - Diatomic molecules require one bond, no angle
    - Triatomic molecules require two bonds, one angle
    - Tetratomic molecules require three bonds, three angles
    """
    # collect all atoms
    atoms = {}
    for bondatoms in bonds.keys():
        atom1, atom2 = bondatoms.split(",")
        atoms[atom1] = None
        atoms[atom2] = None
    atoms = list(atoms.keys())
    atoms_ordered = []

    # place first atom in origin
    coordinates = np.zeros((len(atoms), 3))

    # place second atom along x-axis
    first_bond = list(bonds.keys())[0]
    coordinates[1, 0] = bonds[first_bond]
    first_two_atoms = first_bond.split(",")
    for first in first_two_atoms:
        atoms_ordered.append(first)

    if len(atoms) > 2:
        # place third atom in the xy-plane
        for angleatoms, angle in angles.items():
            angle_atoms = angleatoms.split(",")
            third_atom = angle_atoms.copy()
            if atoms[0] in angle_atoms and atoms[1] in angle_atoms:
                third_atom.remove(atoms[0])
                third_atom.remove(atoms[1])
                break

        middle_atom = angle_atoms[1]
        middle_index = atoms.index(middle_atom)

        for bondatoms, bond in bonds.items():
            bond_atoms = bondatoms.split(",")
            if third_atom[0] in bond_atoms and middle_atom in bond_atoms:
                break

        x_middle = coordinates[middle_index, 0]
        x_third = x_middle + np.sign(x_middle + 1e-6) * bond * np.cos(np.deg2rad(angle))
        y_third = bond * np.sin(np.deg2rad(angle))

        coordinates[2] = [x_third, y_third, 0]
        atoms_ordered.append(third_atom[0])

    if len(atoms) > 3:
        # place fourth atom somewhere in the space that satisfies conditions
        # restricted to the xy-plane
        distributed_atom_indices = []
        for atom in angle_atoms:
            distributed_atom_indices.append(atoms.index(atom))

        fourth_index = 6 - sum(distributed_atom_indices)
        fourth_atom = atoms[fourth_index]
        atoms_ordered.append(fourth_atom)

        # find potential locations of the fourth particle
        potential_points = []
        for angleatoms, angle in angles.items():
            angle_atoms = angleatoms.split(",")
            if fourth_atom in angle_atoms:
                assert fourth_atom != angle_atoms[1], "Circular bonding"
                middle_atom = angle_atoms[1]
                middle_index = atoms.index(middle_atom)

                # find angle ordering
                if fourth_atom == angle_atoms[0]:
                    this_atom = angle_atoms[0]
                    other_atom = angle_atoms[2]
                    this_index = atoms.index(this_atom)
                    other_index = atoms.index(other_atom)
                else:
                    other_atom = angle_atoms[0]
                    this_atom = angle_atoms[2]
                    other_index = atoms.index(other_atom)
                    this_index = atoms.index(this_atom)

                A = coordinates[middle_index]
                B = coordinates[other_index]

                # find bond length
                for bondatoms, bondlength in bonds.items():
                    bondatoms = bondatoms.split(",")
                    if this_atom in bondatoms and middle_atom in bondatoms:
                        break

                # use simple trigonometric relations to find potential points
                theta2 = np.arctan2(B[1] - A[1], B[0] - A[0])
                phi1 = theta2 + np.deg2rad(angle)
                phi2 = theta2 - np.deg2rad(angle)
                p1 = [bondlength * np.cos(phi1), bondlength * np.sin(phi1)]
                p2 = [bondlength * np.cos(phi2), bondlength * np.sin(phi2)]
                potential_points.append([p1, p2])

        # pick the correct coordinates of the fourth particle
        for point1 in potential_points[0]:
            for point2 in potential_points[1]:
                if np.allclose(point1, point2):
                    break
        coordinates[3] = [point2[0], point2[1], 0]

    if len(atoms) > 4:
        raise AttributeError(
            "Not able to construct molecules containing > 4 atoms")

    # write to file
    temp = "ATOM   {:>4}  {:<4}{:<4}{:>4}{:>10.3f}{:>10.3f}{:>10.3f}{:>6.2f}{:>6.2f}\n"
    with open(filename, 'w') as f:
        f.write("CRYST1    0.000    0.000    0.000  90.00  90.00  90.00 P 1          1\n")
        for i, coord in enumerate(coordinates):
            f.write(temp.format(i+1, atoms_ordered[i], molname[:4], 1, coord[0], coord[1], coord[2], 0, 0))
        f.write("END\n")


def write_pdb(nummol, length, single_mol, tolerance=2.0, filetype='pdb',
              outfile=None):
    """Write PDB file using Packmol
    """
    if outfile is None:
        outfile = "out." + filetype
    with open("input.inp", 'w') as f:
        f.write(f"tolerance {tolerance}\n")
        f.write(f"filetype {filetype}\n")
        f.write(f"output {outfile}\n\n")
        f.write(f"structure {single_mol}\n")
        f.write(f"  number {nummol}\n")
        f.write(f"  inside cube 0. 0. 0. {length}\n")
        f.write("end structure")

    # Run packmol input script
    try:
        os.system("packmol < input.inp")
        # subprocess.run(["packmol", "<", "input.inp"])
    except:
        raise OSError("packmol is not found. For installation instructions, \
                       see http://m3g.iqm.unicamp.br/packmol/download.shtml.")


def write_jobscript(filename, executable, slurm_args={}):
    """Write jobscript for Slurm
    """
    string = "#!/bin/bash\n"
    temp = "#SBATCH --{}={}\n"
    for key, value in slurm_args.items():
        string += temp.format(key, value)
    string += "\n\n" + executable + "\n"
    with open(filename, 'w') as f:
        f.write(string)


def psfgen(coordinates="coord.pdb", topology="topology.inp", genfile=None):
    """Generate PSF file
    """

    # read coordinate file
    with open(coordinates, 'r') as f:
        f.readline()
        title = f.readline()
        line = f.readline()
        while line.startswith("REMARK"):
            line = f.readline()
        columns = "TYPE ATOM_ID ATOM_LABEL MOL_LABEL MOL_ID X Y Z \
                   MASS CHARGE ATOM_TYPE\n"
        full_string = columns + line + f.read()[:-6]
        df = pd.read_table(StringIO(full_string), sep=r'\s+')
    numatoms = df['ATOM_ID'].iloc[-1]
    nummols = df['MOL_ID'].iloc[-1]

    # read topology file
    autogenerate = []
    atom_types = []
    atom_masses = []
    atoms = []
    atom_labels = []
    atom_charges = []
    bonds = []
    with open(topology, 'r') as f:
        for line in f:
            splitted = line.split()
            if line.startswith("MASS "):
                atom_types.append(splitted[2])
                atom_masses.append(splitted[3])
            elif line.startswith("DEFA "):
                first = splitted[2]
                last = splitted[4]
            elif line.startswith("AUTOGENERATE "):
                for i in range(1, len(splitted)):
                    autogenerate.append(splitted[i])
            elif line.startswith("RESI "):
                mollabel = splitted[1]
            elif line.startswith("ATOM "):
                atom_labels.append(splitted[1])
                atoms.append(splitted[2])
                atom_charges.append(splitted[3])
            elif line.startswith("BOND "):
                for i in range((len(splitted)-1)//2):
                    bonds.append([splitted[2*i+1], splitted[2*i+2]])

    # create filename of not given
    if genfile is None:
        name, extention = coordinates.split('.')
        genfile = name + ".psf"

    # structurate information to be used in PSF file
    charges, masses = {}, {}
    for atom, charge in zip(atoms, atom_charges):
        charges[atom] = charge
    for atom, mass in zip(atom_types, atom_masses):
        masses[atom] = mass

    df['ISB'] = numatoms * ["ISB"]
    df['ZEROS'] = numatoms * [0]
    all_atom_ids = df['ATOM_LABEL']
    all_charges = df['ATOM_LABEL']
    all_masses = df['ATOM_LABEL']
    for atom, label in zip(atoms, atom_labels):
        all_atom_ids = np.where(all_atom_ids == label, atom, all_atom_ids)
        all_charges = np.where(all_atom_ids == atom, charges[atom], all_charges)
        all_masses = np.where(all_atom_ids == atom, masses[atom], all_masses)

    df['ATOM_TYPE_TOPO'] = all_atom_ids
    df['CHARGE'] = np.asarray(all_charges, dtype=float)
    df['MASS'] = np.asarray(all_masses, dtype=float)
    df['MOL_LABEL_TOPO'] = numatoms * [mollabel]

    # generate bond and angle lists
    angles = [['H1', 'O1', 'M1'], ['H1', 'O1', 'H2'], ['H2', 'O1', 'M1']]
    numbonds = nummols * len(bonds)
    numangles = nummols * len(angles)
    bond_list = []
    angle_list = []
    for mol in range(nummols):
        mol_atoms = {}
        for atom in np.where(df['MOL_ID'] == mol + 1)[0]:
            mol_atoms[df['ATOM_LABEL'].iloc[atom]] = atom + 1
        for bond in bonds:
            bond_list.append(mol_atoms[bond[0]])
            bond_list.append(mol_atoms[bond[1]])
        for angle in angles:
            angle_list.append(mol_atoms[angle[0]])
            angle_list.append(mol_atoms[angle[1]])
            angle_list.append(mol_atoms[angle[2]])

    # write PSF file
    now = datetime.datetime.now()
    temp = "{:>8} {}\n"
    with open(genfile, 'w') as f:
        # write header information
        f.write("PSF\n\n")
        f.write(temp.format(4, "!NTITLE"))
        f.write(temp.format("REMARKS", "PSF file generated by GOMC-wrapper"))
        f.write(temp.format("REMARKS", f"DATE: {now:%Y-%m-%d %H:%M:%S}"))
        f.write(temp.format("REMARKS", f"topology {topology}"))
        string = "segment ISB {"
        string += " first " + first + ";"
        string += " last " + last + ";"
        string += " auto"
        for auto in autogenerate:
            string += " " + auto.lower()
        string += " }\n"
        f.write(temp.format("REMARKS", string))

        # write atom information
        f.write(temp.format(numatoms, "!NATOM"))
        df_as = df[['ATOM_ID', 'ISB', 'MOL_ID', 'MOL_LABEL_TOPO', 'ATOM_LABEL',
                    'ATOM_TYPE_TOPO', 'CHARGE', 'MASS', 'ZEROS']].copy()
        np.savetxt(f, df_as.values, fmt='%8d %-4s %-4d %-4s %-4s %-4s %10.6f %13.4f %11d')

        # write bond information
        numcol = 6
        f.write("\n")
        f.write(temp.format(numbonds, "!NBOND: bonds"))
        bonds = np.asarray(bond_list, dtype=int).reshape(-1, numcol)
        np.savetxt(f, bonds, fmt=numcol * '%8d')

        # write angle information
        numcol = 9
        f.write("\n")
        f.write(temp.format(numangles, "!NTHETA: angles"))
        angles = np.asarray(angle_list, dtype=int).reshape(-1, numcol)
        np.savetxt(f, angles, fmt=numcol * '%8d')

        # write dihedral information
        f.write("\n")
        f.write(temp.format(0, "!NPHI: dihedrals"))

        # write improper information
        f.write("\n\n")
        f.write(temp.format(0, "!NIMPHI: impropers"))

        # write donor information
        f.write("\n\n")
        f.write(temp.format(0, "!NDON: donors"))

        # write acceptors information
        f.write("\n\n")
        f.write(temp.format(0, "!NACC: acceptors"))

        # write non-bonded information
        f.write("\n\n")
        f.write(temp.format(0, "!NNB: non-bonded"))
        f.write("\n")
        zeros = np.zeros(numatoms)
        numcol = 4
        zeros = zeros.reshape(-1, numcol)
        np.savetxt(f, zeros, fmt=numcol * '%8d')

        # write acceptors information
        f.write("\n")
        f.write(temp.format(1, f"{0:>8} !NGRP"))
        f.write(temp.format(0, f"{0:>8}{0:>8}"))
