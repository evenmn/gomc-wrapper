# GOMC wrapper
[GOMC](http://gomc.eng.wayne.edu/), an abbreviation of GPU Optimized Monte Carlo, is an open-source library for simulating molecular systems using the Metropolis Monte Carlo algorithm. The software has been written in object oriented C++, and uses OpenMP and NVIDIA CUDA to allow for execution on multi-core CPU and GPU architectures.

This GOMC Python interface was developed to automatize file handling, simulation launching and data analysis. This allows for simulation pipelines handled by the computer. Other than that, the wrapper does not extend the functionality of GOMC.

## Basic tutorial
### Read file into GOMC object
If you already have a GOMC input script, `in.conf`, this can be read into a GOMC object by
``` python
from gomc_wrapper import read
gomc = read("in.conf")
```
Then, parameters can be changed by the `set` method:
``` python
gomc.set("Temperature", 298.15)
```
When one is done editing the configuration file, one usually either wants to write a new GOMC input file or run GOMC with the desired configurations. In the former case, one calls the `write` method:
``` python
gomc.write("in.conf.new", verbose=True)
```
In the latter case, one calls the `run` method:
``` python
gomc.run(num_procs=4, gomc_exec="GOMC_CPU_NVT")
```

### Create a new GOMC object
A GOMC object might also be created from scratch. Then, all the required parameters need to be set. The standard way of doing this, is to use the `set` method:
``` python
from gomc_wrapper import GOMC
gomc = GOMC()
gomc.set("GEMC", "NVT")
gomc.set("Coordinates", 0, "BUTAN_BOX_0.pdb")
```
However, for some operations it might be more convenient to use one of the specialized set-methods `add_box`, `set_steps` or `set_prob`. `add_box` lets you add a box to the system:
``` python
gomc.add_box(coordinates="BUTAN_BOX_0.pdb",
             structure="BUTAN_BOX_0.psf",
             hmatrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]])
```
`set_steps` lets you set all numbers of steps in one call:
``` python
gomc.set_steps(run=1000000, eq=100000, adj=1000)
```
`set_prob` lets you specify the transition probabilities:
``` python
gomc.set_prob(dis=0.6, rot=0.3, swap=0.08, vol=0.02)
```

## To do
- Write a simple PSF generator 
