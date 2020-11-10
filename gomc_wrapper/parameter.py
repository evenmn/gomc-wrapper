class Parameter:
    def __init__(self, *types, multiline=False):
        self.types = types
        self.values = []
        self.multiline = multiline

    def __repr__(self):
        return ', '.join(self.types)

    def __str__(self):
        string = ""
        if self.multiline:
            # for values in self.values:
            for value, thistype in zip(self.values[0], self.types):
                if thistype == int:
                    string += str(int(value)) + " \t"
                elif thistype == float:
                    string += str(float(value)) + " \t"
                elif thistype == str:
                    string += str(value) + " \t"
                elif thistype == bool:
                    if value is True:
                        string += "true \t"
                    else:
                        string += "false \t"
                elif thistype == list:
                    string += " \t".join(value)
        else:
            for value, thistype in zip(self.values, self.types):
                if thistype == int:
                    string += str(int(value)) + " \t"
                elif thistype == float:
                    string += str(float(value)) + " \t"
                elif thistype == str:
                    string += str(value) + " \t"
                elif thistype == bool:
                    if value is True:
                        string += "true \t"
                    else:
                        string += "false \t"
                elif thistype == list:
                    string += " \t".join(value)
        return string

    def set(self, *values):
        if self.multiline:
            # save all inputs if multiple lines is allowed
            self.values.append([])
            for value, thistype in zip(values, self.types):
                self.values[-1].append(thistype(value))
        else:
            # overwrite inputs if multiple lines is not allowed
            for value, thistype in zip(values, self.types):
                self.values.append(thistype(value))


parameters = {}
parameters["Restart"] = Parameter(bool)
parameters["RestartCheckpoint"] = Parameter(bool)
parameters["PRNG"] = Parameter(str)
parameters["Random_Seed"] = Parameter(int)
parameters["ParaTypeCHARMM"] = Parameter(bool)
parameters["ParaTypeEXOTIC"] = Parameter(bool)
parameters["ParaTypeMie"] = Parameter(bool)
parameters["ParaTypeMARTINI"] = Parameter(bool)
parameters["Parameters"] = Parameter(str)
parameters["Coordinates"] = Parameter(int, str, multiline=True)
parameters["Structure"] = Parameter(int, str, multiline=True)
parameters["Structures"] = Parameter(int, str, multiline=True)
parameters["MultiSimFolderName"] = Parameter(str)
parameters["GEMC"] = Parameter(str)
parameters["Pressure"] = Parameter(float)
parameters["Temperature"] = Parameter(float)
parameters["Rcut"] = Parameter(float)
parameters["RcutLow"] = Parameter(float)
parameters["RcutCoulomb"] = Parameter(int, float, multiline=True)
parameters["LRC"] = Parameter(bool)
parameters["Exclude"] = Parameter(str)
parameters["Potential"] = Parameter(str)
parameters["Rswitch"] = Parameter(float)
parameters["VDWGeometricSigma"] = Parameter(bool)
parameters["ElectroStatic"] = Parameter(bool)
parameters["Ewald"] = Parameter(bool)
parameters["CachedFourier"] = Parameter(bool)
parameters["Tolerance"] = Parameter(float)
parameters["Dielectric"] = Parameter(float)
parameters["PressureCalc"] = Parameter(bool, int)
parameters["1-4scaling"] = Parameter(float)
parameters["RunSteps"] = Parameter(int)
parameters["EqSteps"] = Parameter(int)
parameters["AdjSteps"] = Parameter(int)
parameters["ChemPot"] = Parameter(str, float)
parameters["Fugacity"] = Parameter(str, float)
parameters["DisFreq"] = Parameter(float)
parameters["RotFreq"] = Parameter(float)
parameters["IntraSwapFreq"] = Parameter(float)
parameters["RegrowthFreq"] = Parameter(float)
parameters["CrankShaftFreq"] = Parameter(float)
parameters["MultiParticleFreq"] = Parameter(float)
parameters["IntraMEMC-1Freq"] = Parameter(float)
parameters["IntraMEMC-2Freq"] = Parameter(float)
parameters["IntraMEMC-3Freq"] = Parameter(float)
parameters["MEMC-1Freq"] = Parameter(float)
parameters["MEMC-2Freq"] = Parameter(float)
parameters["MEMC-3Freq"] = Parameter(float)
parameters["SwapFreq"] = Parameter(float)
parameters["VolFreq"] = Parameter(float)
parameters["ExchangeVolumeDim"] = Parameter(float, float, float)
parameters["ExchangeSmallKind"] = Parameter(float)
parameters["ExchangeLargeKind"] = Parameter(float)
parameters["ExchangeRatio"] = Parameter(int)
parameters["LargeKindBackBone"] = Parameter(str, str)
parameters["SmallKindBackBone"] = Parameter(str, str)
parameters["useConstantArea"] = Parameter(bool)
parameters["FixVolBox0"] = Parameter(bool)
parameters["CellBasisVector1"] = Parameter(int, float, float, float,
                                           multiline=True)
parameters["CellBasisVector2"] = Parameter(int, float, float, float,
                                           multiline=True)
parameters["CellBasisVector3"] = Parameter(int, float, float, float,
                                           multiline=True)
parameters["CBMC_First"] = Parameter(int)
parameters["CBMC_Nth"] = Parameter(int)
parameters["CBMC_Ang"] = Parameter(int)
parameters["CBMC_Dih"] = Parameter(int)
parameters["FreeEnergyCalc"] = Parameter(bool, int)
parameters["MoleculeType"] = Parameter(str, int)
parameters["InitialState"] = Parameter(int)
parameters["LambdaVDW"] = Parameter(float)
parameters["LambdaCoulomb"] = Parameter(float)
parameters["ScaleCoulomb"] = Parameter(bool)
parameters["ScalePower"] = Parameter(int)
parameters["ScaleAlpha"] = Parameter(float)
parameters["MinSigma"] = Parameter(float)
parameters["OutputName"] = Parameter(str)
parameters["CoordinatesFreq"] = Parameter(bool, int)
parameters["RestartFreq"] = Parameter(bool, int)
parameters["CheckpointFreq"] = Parameter(bool, int)
parameters["ConsoleFreq"] = Parameter(bool, int)
parameters["BlockAverageFreq"] = Parameter(bool, int)
parameters["HistogramFreq"] = Parameter(bool, int)
parameters["DistName"] = Parameter(str)
parameters["HistName"] = Parameter(str)
parameters["RunNumber"] = Parameter(int)
parameters["RunLetter"] = Parameter(str)
parameters["SampleFreq"] = Parameter(int)
parameters["OutEnergy"] = Parameter(bool, bool)
parameters["OutPressure"] = Parameter(bool, bool)
parameters["OutMolNum"] = Parameter(bool, bool)
parameters["OutDensity"] = Parameter(bool, bool)
parameters["OutVolume"] = Parameter(bool, bool)
parameters["OutSurfaceTension"] = Parameter(bool, bool)
