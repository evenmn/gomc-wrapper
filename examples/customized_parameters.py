from gomc_wrapper import GOMC
from gomc_wrapper.substance import TIP4P2005

# initialize substance
tip4p = TIP4P2005()

Z_H = 0.6
Z_O = - 2 * Z_H
r0 = 0.9572
OM = 0.1546
theta = 104.52
epsilon = 18.56
sigma = 3.16

# generate GOMC object
gomc = GOMC()
gomc.set("Restart", "false")
gomc.set("PRNG", "RANDOM")
gomc.set("GEMC", "NVT")
gomc.set("Temperature", 370.0)
gomc.set("PressureCalc", "true", 1000)
gomc.set_steps(run=4e6, eq=4e6, adj=1000)
gomc.set_prob(dis=0.6, rot=0.28, swap=0.1, vol=0.02)
gomc.set_cbmc(first=10, nth=4, ang=100, dih=20)
gomc.set_freq(coord=1e6, restart=1e6, console=1e4, block=1e4)
gomc.set_out(pressure=True, molnum=True, density=True, volume=True)

gomc.set_box(0, 448, tip4p, density=32.5)
gomc.set_box(1, 64, tip4p, density=1.0)

slurm_args = {'partition': 'normal',
              'ntask': 1,
              'gres': 'gpu:1',
              'job-name': 'GOMCtest',
              'cpus-per-task': 8}

gomc.run(gomc_exec='GOMC_GPU_GEMC', num_procs=4, slurm=True, slurm_args=slurm_args)
