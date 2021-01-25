from gomc_wrapper import GOMC

gomc_parameters = {'Rcut': 8.5, 'LRC': True, 'Exclude': '1-4',
                   'Potential': 'VDW', 'ElectroStatic': True,
                   'Ewald': True, 'CachedFourier': True,
                   'Tolerance': 1e-5, 'RcutLow': 1.0}

nummol = 512
steps = 2500 * nummol
pdb1 = "output1_BOX_0_restart.pdb"
pdb2 = "output2_BOX_0_restart.pdb"
psf1 = "coords1.psf"
psf2 = "coords2.psf"

hmatrix1 = [[23.77703, 0, 0], [0, 23.77703, 0], [0, 0, 23.77703]]
hmatrix2 = [[156.44680, 0, 0], [0, 156.44680, 0], [0, 0, 156.44680]]

# generate GOMC input script
gomc = GOMC()
gomc.set("Restart", False)
gomc.set("PRNG", "RANDOM")
gomc.set("Random_Seed", 54355)
gomc.set("Temperature", 373.15)
gomc.set("PressureCalc", True, 1000)
gomc.set("GEMC", "NVT")
gomc.set("OutputName", "output")
gomc.set("OutHeat", True, True)
gomc.set("Parameters", "Par_TIP4P.inp")
gomc.set("ParaTypeCHARMM", "on")
gomc.set_steps(run=steps, eq=steps, adj=1000)
gomc.set_prob(dis=0.6, rot=0.28, swap=0.1, vol=0.02)
gomc.set_cbmc(first=10, nth=4, ang=100, dih=20)
gomc.set_freq(coord=1e5, restart=1e5, console=1e1, block=1e4)
gomc.set_out(pressure=True, molnum=True, density=True, volume=True, energy=True, heat=True)

gomc.add_box(coordinates=pdb1, structure=psf1, hmatrix=hmatrix1)
gomc.add_box(coordinates=pdb2, structure=psf2, hmatrix=hmatrix2)

# set parameters related to the force-field
for key, value in gomc_parameters.items():
    gomc.set(key, value)

gomc.set("RcutCoulomb", 0, gomc_parameters['Rcut'])
gomc.set("RcutCoulomb", 1, gomc_parameters['Rcut'])

#gomc.write('in.conf')
gomc.run(gomc_exec="GOMC_CPU_GEMC", num_procs=8, gomc_input="in.conf")
