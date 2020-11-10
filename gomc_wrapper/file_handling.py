import os
import datetime


def read(filename='in.conf'):
    from __init__ import GOMC

    parameters = {}
    with open(filename, 'r') as f:
        for line in f:
            if line[0].isalpha():
                # ignoring all lines that do not start with a letter
                splitted = line.split()
                parameters[str(splitted[0])] = splitted[1:]

    # create GOMC object containing all parameters
    gomc = GOMC()
    for key, values in parameters.items():
        gomc.set(key, *tuple(values))
    return gomc


def write(self, filename='in.conf', verbose=True):
    """Write GOMC input script
    """
    now = datetime.datetime.now()
    filepath = os.path.join(self.wd, filename)

    with open(filepath, 'w') as f:

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
                f.write(key.ljust(16) + " \t")
                f.write(str(obj) + "\n")


if __name__ == "__main__":
    gomc = read("/home/evenmn/tip4p-vapor/src/gemc_gomc/in.conf")
    gomc.write("in.conf", verbose=False)
