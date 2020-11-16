from gomc_wrapper import read, write_topology, write_parameter, psfgen

# parameters
Z_H = 0.6
Z_O = - 2 * Z_H
r0 = 0.9572
OM = 0.1546
theta = 104.52
epsilon = 18.56
sigma = 3.16

# file names
configfile = "in.conf"
topofile = "topology.inp"
paramfile = "param.inp"
pdb1 = "liquid_gomc_tip4p.pdb"
pdb2 = "vapor_gomc_tip4p.pdb"
psf1 = "liquid_gomc_tip4p.psf"
psf2 = "vapor_gomc_tip4p.psf"

# define atoms
atoms = ['O', 'H', 'H', 'M']
labels = ['O', 'H1', 'H2', 'M']
mass = {'O': 15.9994, 'H': 1.0079, 'M': 0.0}
charge = {'O': 0.0, 'H': Z_H, 'M': Z_O}
bonds = ['OH', 'OM']
molname = 'TIP4P'
symbols = {'O': 'O', 'H': 'H', 'M': 'M'}

# define GOMC object
gomc = read(configfile)
gomc.set_working_directory("simulations")
gomc.copy_to_wd(paramfile, pdb1, pdb2)

# generate files
write_topology(topofile, atoms, labels, mass, charge, bonds, molname)
psfgen(coordinates=pdb1, topology=topofile, genfile=psf1)
psfgen(coordinates=pdb2, topology=topofile, genfile=psf2)
write_parameter(paramfile, r0, theta, OM, epsilon, sigma, symbols)

# modify GOMC object
gomc.set("Restart", False)
gomc.set("Parameters", paramfile)
gomc.set("Rcut", 8.5)
gomc.set("RcutCoulomb", 8.5)
gomc.set("Coordinates", 0, pdb1)
gomc.set("Coordinates", 1, pdb2)
gomc.set("Structure", 0, psf1)
gomc.set("Structure", 1, psf2)
# gomc.write("in.conf2")
gomc.run(gomc_exec="GOMC_CPU_GEMC", num_procs=1, gomc_input="in.conf2")
