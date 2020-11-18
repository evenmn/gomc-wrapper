import numpy as np
import pandas as pd
from io import StringIO


class Analyze:
    """Class for handling GOMC dat-files.
    Parameters
    ----------------------
    :param filename: path to lammps log file
    :type filename: string or file
    """
    def __init__(self, filename):
        # Identifiers for places in the log file
        if hasattr(filename, "read"):
            logfile = filename
        else:
            logfile = open(filename, 'r')
        self.read_file_to_dataframe(logfile)

    def read_file_to_dataframe(self, logfile):
        # read three first lines, which should be information lines
        string = logfile.readline()[1:]  # string should start with the kws
        self.keywords = string.split()
        contents = logfile.read()
        self.contents = pd.read_table(StringIO(string + contents), sep=r'\s+')

    def find(self, entry_name):
        return np.asarray(self.contents[entry_name])

    def get_keywords(self):
        """Return list of available data columns in the log file."""
        print(", ".join(self.keywords))

    @staticmethod
    def average(arr, window):
        """Average an array arr over a certain window size
        """
        if window == 1:
            return arr
        elif window > len(arr):
            raise IndexError("Window is larger than array size")
        else:
            remainder = len(arr) % window
            if remainder == 0:
                avg = np.mean(arr.reshape(-1, window), axis=1)
            else:
                avg = np.mean(arr[:-remainder].reshape(-1, window), axis=1)
        return avg


if __name__ == "__main__":
    window = 10
    filenames = ["Blk_TIP4P_370_00_K_RESTART5_BOX_0.dat",
                 "Blk_TIP4P_370_00_K_RESTART5_BOX_1.dat"]

    phases = ["liquid", "gas"]

    fileobjs = []
    dependents = []
    for filename in filenames:
        file = Analyze(filename)
        fileobjs.append(file)
        dependents.append(file.average(file.find("STEPS")[50:], window))

    import matplotlib.pyplot as plt
    keywords = ["TOT_EN", "EN_INTER", "EN_TC", "EN_INTRA(B)", "EN_INTRA(NB)",
                "EN_ELECT", "EN_REAL", "EN_RECIP", "TOTAL_VIR", "PRESSURE",
                "TOT_MOL", "TOT_DENS", "SURF_TENSION"]
    keywords = ["PRESSURE", "TOT_MOL", "TOT_DENS", "SURF_TENSION"]
    keywords = ["PRESSURE"]
    for keyword in keywords:
        for fileobj, dependent, phase in zip(fileobjs, dependents, phases):
            arr = fileobj.find(keyword)
            arr_avg = fileobj.average(arr[50:], window)
            plt.plot(dependent, arr_avg, label=phase)
        plt.xlabel("Steps")
        plt.ylabel(keyword)
        plt.legend(loc='best')
        plt.grid()
        plt.show()
