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
