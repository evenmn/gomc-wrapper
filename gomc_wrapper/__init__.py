import os
import shutil
import subprocess
from .parameter import parameters
from .file_handling import read, write_topology, write_parameter, psfgen


class GOMC:
    def __init__(self):

        self.parameters = parameters

        self.numboxes = 0
        self.boxes = []
        self.wd = ""

    # import
    from .config import add_box, set_steps, set_prob
    from .file_handling import write

    def set(self, keyword, *values):
        print(" ")
        print(keyword)
        self.parameters[keyword].set(*values)
        print(self.parameters[keyword].values)

    def set_working_directory(self, wd, overwrite=False):
        self.wd = wd
        if overwrite:
            self.wd = wd
            try:
                os.makedirs(wd)
            except FileExistsError:
                pass
        else:
            ext = 0
            repeat = True
            while repeat:
                try:
                    os.makedirs(self.wd)
                    repeat = False
                except FileExistsError:
                    ext += 1
                    self.wd = wd + f"_{ext}"
        self.wd += "/"

    def copy_to_wd(self, *filename):
        """Copy one or several files to working directory.

        :param filename: filename or list of filenames to copy
        :type filename: str or list of str
        """

        for file in filename:
            head, tail = os.path.split(file)
            shutil.copyfile(file, self.wd + tail)

    def run(self, gomc_exec='GOMC_CPU_NVT', num_procs=1, gomc_input='in.conf'):
        """Run
        """
        self.write(gomc_input)
        subprocess.Popen([gomc_exec, f"+p{num_procs}", gomc_input])


if __name__ == "__main__":
    gomc = GOMC()
    gomc.set("PRNG", "RANDOM")
    gomc.add_box("some.pdb", "some.psf", [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    gomc.add_box("some2.pdb", "some2.psf", [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    gomc.write("test")
