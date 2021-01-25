from gomc_wrapper import GOMC, psfgen, write_pdb, write_parameter, write_topology, write_molecule
from gomc_wrapper.substance import TIP4P2005
from scipy import constants

# define system properties
temp = 298
num_mol = 512
rho = 0.997

cycles = 1000
steps = cycles * num_mol
seed = 32848

# define file names
molfile = "molecule.pdb"
topofile = "topology.inp"
paramfile = "Par_TIP4P.inp"
pdb = "coords.pdb"
psf = "coords.psf"
out = "output"
gomc_input = "in.conf"

# generate pdb and psf files
tip4p = TIP4P2005()
write_parameter(paramfile,
                r0=tip4p.bonds['O1,H1'],
                theta=tip4p.angles['H1,O1,H2'],
                OM=tip4p.bonds['O1,M1'],
                epsilon=tip4p.lj_params['OO']['epsilon'],
                sigma=tip4p.lj_params['OO']['sigma'])

# generate topology file to be used by psfgen
write_topology(atoms=tip4p.atom_types, labels=tip4p.atom_labels,
               mass=tip4p.masses, charge=tip4p.charges,
               bonds=tip4p.bond_types, molname=tip4p.__repr__(),
               filename=topofile)

# write molecule file to be used by packmol
write_molecule(bonds=tip4p.bonds, angles=tip4p.angles, filename=molfile)

# compute necessary quantities
tot_mass = 18.01528 * num_mol / constants.N_A     # in grams
volume = (tot_mass / rho) * 1e24    # in Å³
length = volume**(1/3)  # in Å
hmatrix = [[length, 0, 0], [0, length, 0], [0, 0, length]]

# pack initial configuration using Packmol
write_pdb(num_mol, length, molfile, outfile=pdb)

# generate PSF file
psfgen(coordinates=pdb, topology=topofile, genfile=psf)

# generate GOMC input script
gomc = GOMC()
gomc.set("PRNG", "INTSEED")
gomc.set("Random_Seed", seed)
gomc.set("Restart", False)
gomc.set("Temperature", temp)
gomc.set("PressureCalc", True, 1000)
gomc.set("OutputName", out)
gomc.set("Parameters", paramfile)
gomc.set("ParaTypeCHARMM", "on")
gomc.set("FreeEnergyCalc", True, 1000)
gomc.set("MoleculeType", "TIP4", 1)
gomc.set("InitialState", 0)
gomc.set("ScalePower", 2)
gomc.set("ScaleAlpha", 0.5)
gomc.set("MinSigma", 3.0)
gomc.set("ScaleCoulomb", False)
# states        0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
gomc.set("LambdaVDW", 0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00)
gomc.set("LambdaCoulomb",  0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.20, 0.40, 0.60, 0.70, 0.80, 0.90, 1.00)
gomc.set_steps(run=steps, eq=steps, adj=1000)
gomc.set_prob(dis=0.6, rot=0.4)
gomc.set_cbmc(first=10, nth=4, ang=100, dih=20)
gomc.set_freq(coord=1e5, restart=1e5, console=1e4, block=1e4)
gomc.set_out(pressure=True, molnum=True, density=True)

# set parameters related to the force-field
for key, value in tip4p.gomc_params.items():
    gomc.set(key, value)

gomc.set("RcutCoulomb", 0, tip4p.gomc_params['Rcut'])
gomc.add_box(coordinates=pdb, structure=psf, hmatrix=hmatrix)

job_id = gomc.run(gomc_exec="GOMC_CPU_NVT", num_procs=8, gomc_input=gomc_input)
