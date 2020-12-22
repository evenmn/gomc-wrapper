import os
import re
import time
import shutil
import subprocess
from .parameter import _initialize_parameters
from .file_handling import read, write_topology, write_parameter, write_molecule, write_pdb, write_jobscript, psfgen


class GOMC:
    def __init__(self):

        self.parameters = _initialize_parameters()

        self.numboxes = 0
        self.boxes = []
        self.cwd = os.getcwd()

    # import
    from .config import add_box, set_box, set_steps, set_prob, set_cbmc, set_freq, set_out
    from .file_handling import write

    def set(self, keyword, *values):
        self.parameters[keyword].set(*values)

    def set_working_directory(self, wd, overwrite=False):
        """Define working directory
        """
        self.wd = wd    # proposed working directory
        if overwrite:
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
        os.chdir(self.wd)

    def copy_to_wd(self, *filename):
        """Copy one or several files to working directory.

        :param filename: filename or list of filenames to copy
        :type filename: str or list of str
        """

        for file in filename:
            path = os.path.join(self.cwd, file)
            head, tail = os.path.split(path)
            shutil.copyfile(path, tail)

    def run(self, gomc_exec='GOMC_CPU_NVT', num_procs=1, gomc_input='in.conf',
            slurm=False, slurm_args={}, jobscript='job.sh', wait=True):
        """Run
        """
        self.write(gomc_input)
        executable = f"{gomc_exec} +p{num_procs} {gomc_input}"
        if slurm:
            write_jobscript(jobscript, executable, slurm_args)
            output = str(subprocess.check_output(['sbatch', jobscript]))
            job_id = int(re.findall("([0-9]+)", output)[0])
            print("Job_ID found to be: ", job_id)
        else:
            # os.system(executable)
            subprocess.Popen(executable.split())
            time.sleep(1)
            job_id = int(subprocess.check_output(['pidof', gomc_exec]))

            if wait:
                done = False
                while not done:
                    try:
                        subprocess.check_output(['pidof', gomc_exec])
                        # subprocess.check_output(['ps', '-p', str(pid), '|', 'grep', str(pid)])
                        time.sleep(3)
                    except subprocess.CalledProcessError:
                        done = True
                    except:
                        subprocess.Popen(['kill', str(job_id)])
        return job_id
