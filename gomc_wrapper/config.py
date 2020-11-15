def add_box(self, coordinates, structure, hmatrix):
    """Add box
    """
    box_ID = self.numboxes
    self.numboxes += 1

    self.set("Coordinates", box_ID, str(coordinates))
    self.set("Structure", box_ID, str(structure))

    self.set("CellBasisVector1", box_ID,
             hmatrix[0][0], hmatrix[0][1], hmatrix[0][2])
    self.set("CellBasisVector2", box_ID,
             hmatrix[1][0], hmatrix[1][1], hmatrix[1][2])
    self.set("CellBasisVector3", box_ID,
             hmatrix[2][0], hmatrix[2][1], hmatrix[2][2])


def set_box(self, id, nummol, substance, numberdensity=None, massdensity=None,
            volume=None, pbc=0):
    """Set box with box id 'id'. Density is number density
    """
    from .file_handling import write_molecule, write_pdb, write_topology, write_parameter, psfgen

    assert [numberdensity, massdensity, volume].count(None) == 2, \
        "Either volume or density has to be given"

    if numberdensity is not None:
        volume = nummol / numberdensity
    if massdensity is not None:
        molmass = sum(list(substance.masses.values()))
        totmass = nummol * molmass
        volume = totmass / massdensity

    box_length = volume**(1/3) - pbc

    molfile = "molecule.pdb"
    coordfile = f"box_{id}.pdb"
    topofile = "topology.inp"
    psffile = f"box_{id}.psf"
    paramfile = "param.inp"

    # write molecule file
    write_molecule(bonds=substance.bonds, angles=substance.angles,
                   filename=molfile)

    # write pdb file using Packmol
    write_pdb(nummol, box_length, single_mol=molfile, outfile=coordfile)

    # write topology file
    write_topology(atoms=substance.atom_types, labels=substance.atom_labels,
                   mass=substance.masses, charge=substance.charges,
                   bonds=substance.bond_types, molname=substance.__repr__(),
                   filename=topofile)

    # generate PSF file
    psfgen(coordinates=coordfile, topology=topofile, genfile=psffile)

    # generate parameter file
    write_parameter(paramfile)

    # set parameters related to the force-field
    for key, value in substance.gomc_parameters.items():
        self.set(key, value)

    # set parameters related to the box
    self.set("Parameters", paramfile)
    self.set("ParaTypeCHARMM", "on")
    self.set("RcutCoulomb", id, substance.gomc_parameters['Rcut'])
    self.set("Coordinates", id, coordfile)
    self.set("Structure", id, psffile)
    self.set("CellBasisVector1", id, box_length + pbc, 0, 0)
    self.set("CellBasisVector2", id, 0, box_length + pbc, 0)
    self.set("CellBasisVector3", id, 0, 0, box_length + pbc)


def set_steps(self, run, eq=0, adj=0):
    """Set number of steps
    """
    self.set("RunSteps", run)
    self.set("EqSteps", eq)
    self.set("AdjSteps", adj)


def set_prob(self, dis=0.0, rot=0.0, intraswap=0.0, regrowth=0.0,
             crankshaft=0.0, multiparticle=0.0, intramemc1=0.0,
             intramemc2=0.0, intramemc3=0.0, memc1=0.0, memc2=0.0,
             memc3=0.0, swap=0.0, vol=0.0):
    """Set transition probabilities
    """
    dct = {"DisFreq": dis, "RotFreq": rot, "IntraSwapFreq": intraswap,
           "RegrowthFreq": regrowth, "CrankShaftFreq": crankshaft,
           "MultiParticleFreq": multiparticle, "IntraMEMC-1Freq": intramemc1,
           "IntraMEMC-2Freq": intramemc2, "IntraMEMC-3Freq": intramemc3,
           "MEMC-1Freq": memc1, "MEMC-2Freq": memc2, "MEMC-3Freq": memc3,
           "SwapFreq": swap, "VolFreq": vol}
    assert sum(dct.values()) == 1.0, "Sum of probabilities has to be equal to 1!"

    for key, value in dct.items():
        if value > 0:
            self.set(key, value)


def set_cbmc(self, first, nth, ang, dih):
    """Set parameters for Configuration-Biased Monte Carlo (CBMC)
    """
    dct = {"CBMC_First": first, "CBMC_Nth": nth, "CBMC_Ang": ang, "CBMC_Dih": dih}

    for key, value in dct.items():
        self.set(key, value)


def set_freq(self, coord=None, restart=None, console=None, block=None,
             checkpoint=None, histogram=None):
    """Set write frequencies
    """
    dct = {"CoordinatesFreq": coord, "RestartFreq": restart,
           "ConsoleFreq": console, "BlockAverageFreq": block,
           "CheckpointFreq": checkpoint, "HistogramFreq": histogram}

    for key, value in dct.items():
        if value is not None:
            self.set(key, "true", value)


def set_out(self, energy=False, pressure=False, molnum=False, density=False,
            volume=False, surfacetension=False):
    """Set block averaged outputs
    """
    dct = {"OutEnergy": energy, "OutPressure": pressure, "OutMolNum": molnum,
           "OutDensity": density, "OutVolume": volume,
           "OutSurfaceTension": surfacetension}

    for key, value in dct.items():
        if value:
            self.set(key, "true", "true")
