'''
This module hosts the DSSAT class. This class represents the simulation environment, 
so per each DSSAT instance there's a directory where all the necesary files to 
run the model are allocated. To run the model there are 3 basic steps:

1. Create a new Dscsm instance.
2. Initialize the environment by calling the setup() method.
3. Run the model by calling the run() method.
You can close the simulation environment by calling the close() method. This will
remove the directory and files created durinh the setup() call.

The model outputs are storage in the `output` attribute. Up to date the next output
are available: PlantGro, Weather, SoilWat, SoilOrg.
'''

import subprocess
import shutil
import os
import tempfile    
import random
import string
import pandas as pd
import sys
import warnings
import platform
import errno, stat

# Libraries for second version
from DSSATTools import __file__ as module_path
from DSSATTools import VERSION
from DSSATTools.soil import SoilProfile
from DSSATTools.weather import Weather
from DSSATTools.crop import Crop, CUL_VARNAME
from DSSATTools.management import Management
from DSSATTools.base.sections import TabularSubsection
from DSSATTools.base.sections import clean_comments

OS = platform.system().lower()
OUTPUTS = ['PlantGro', "Weather", "SoilWat", "SoilOrg"]
OUTPUT_MAP = {
    "PlantGro": "GROUT",  "SoilWat": "WAOUT", "SoilOrg": "CAOUT",
    "Weather": "GROUT"
}

PERENIAL_FORAGES = ['Alfalfa', 'Bermudagrass', 'Brachiaria', 'Bahiagrass']
ROOTS = ['Potato']

# function to handle windows permisions
def handleRemoveReadonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

if 'windows' in OS:
    WIN_SHUTIL_KWARGS = {'ignore_errors': False, 'onerror': handleRemoveReadonly}
    CHMOD_MODE = stat.S_IWRITE
else:
    WIN_SHUTIL_KWARGS = {}
    CHMOD_MODE = 111
class DSSAT():
    '''
    Class that represents the simulation environment. When initializing and seting 
    up the environment, a new folder is created (usually in the tmp folder), and 
    all of the necesary files to run the model are copied into it.

    After the model runs, the output is saved in the output property. 
    '''
    def __init__(self):
        BASE_PATH = os.path.dirname(module_path)
        self._STATIC_PATH = os.path.join(BASE_PATH, 'static')
        if 'windows'in OS:
            self._BIN_PATH = os.path.join(self._STATIC_PATH, 'bin', 'dscsm048.exe')
            self._CONFILE = 'DSSATPRO.V48'
        else: 
            self._BIN_PATH = os.path.join(self._STATIC_PATH, 'bin', 'dscsm048')
            self._CONFILE = 'DSSATPRO.L48'
        self._STD_PATH = os.path.join(self._STATIC_PATH, 'StandardData')
        self._CRD_PATH = os.path.join(self._STATIC_PATH, 'Genotype')
        self._SLD_PATH = os.path.join(self._STATIC_PATH, 'Soil')
        self._SETUP = False
        self._input = {
            'crop': None, 'wheater': None, 'soil': None, 'management': None 
        }

        self._output = {}

    def setup(self, cwd=None):
        '''
        Setup a simulation environment. Creates a tmp folder to run the simulations
        and move all the required files to run the model. Some rguments are 
        optional, if those aren't provided, then standard files location will be
        used.

        Arguments
        ----------
        cwd: str
            Working directory. All the model files would be moved to that 
            directory. If None, then a tmp directory will be created.
        '''
        # TODO: verbose the setup process.
        TMP_BASE = tempfile.gettempdir()
        if cwd:
            self._RUN_PATH = cwd
            if not os.path.exists(self._RUN_PATH):
                os.mkdir(self._RUN_PATH)
        else:
            self._RUN_PATH = os.path.join(
                TMP_BASE, 
                'dssat'+''.join(random.choices(string.ascii_lowercase, k=8))
            )
            os.mkdir(self._RUN_PATH)
        sys.stdout.write(f'{self._RUN_PATH} created.\n')
        
        # Move files
        if not os.path.exists(
            os.path.join(self._RUN_PATH, os.path.basename(self._BIN_PATH))
            ):
            shutil.copyfile(
                self._BIN_PATH, 
                os.path.join(self._RUN_PATH, os.path.basename(self._BIN_PATH))
            )
            os.chmod(
                os.path.join(self._RUN_PATH, os.path.basename(self._BIN_PATH)),
                mode=CHMOD_MODE
            )
        for file in os.listdir(self._STATIC_PATH):
            if file.endswith('.CDE'):
                shutil.copyfile(
                    os.path.join(self._STATIC_PATH, file), 
                    os.path.join(self._RUN_PATH, file)
                )
        # Copy static path
        if os.path.exists(os.path.join(self._RUN_PATH, 'static')):
            shutil.rmtree(os.path.join(self._RUN_PATH, 'static'))
        shutil.copytree(self._STATIC_PATH, os.path.join(self._RUN_PATH, 'static'))
        sys.stdout.write(f'Static files copied to {self._RUN_PATH}.\n')
        self._STATIC_PATH = os.path.join(self._RUN_PATH, 'static')
        if 'windows'in OS:
            self._BIN_PATH = os.path.join(self._STATIC_PATH, 'bin', 'dscsm048.exe')
        else: 
            self._BIN_PATH = os.path.join(self._STATIC_PATH, 'bin', 'dscsm048')
        self._STD_PATH = os.path.join(self._STATIC_PATH, 'StandardData')
        self._CRD_PATH = os.path.join(self._STATIC_PATH, 'Genotype')
        self._SLD_PATH = os.path.join(self._STATIC_PATH, 'Soil')

        self._SETUP = True


    def run(self, 
            soil:SoilProfile,
            weather:Weather,
            crop:Crop,
            management:Management,
        ):
        '''
        Start the simulation and runs until the end or failure. It will return
        None, but the simulation outputs will be assigned to self.output.

        Arguments
        ----------
        soil: DSSATTools.SoilProfile
            SoilProfile instance
        weather: DSSATTools.Weather
            Weather instance
        crop: DSSATTools.Crop
            Crop instance
        managment: DSSATTools.Management
            Management instance
        '''
        
        assert self._SETUP, 'You must initialize the simulation environment by'\
            + ' running the setup() method'

        # Remove previous outputs and inputs
        OUTPUT_FILES = [i for i in os.listdir(self._RUN_PATH) if i[-3:] == 'OUT']
        INP_FILES = [i for i in os.listdir(self._RUN_PATH) if i[-3:] in ['INP', 'INH']]
        self._output = {}

        for file in (OUTPUT_FILES + INP_FILES):
            os.remove(os.path.join(self._RUN_PATH, file))
        
        # Fill Managament fields
        management._Management__cultivars['CR'] = crop._CODE
        management._Management__cultivars['INGENO'] = crop.cultivar["@VAR#"]
        management._Management__cultivars['CNAME'] = \
            crop.cultivar[CUL_VARNAME[crop._CODE]]

        management.field['WSTA....'] = weather._name
        management.field['SLDP'] = soil.total_depth
        management.field['ID_SOIL'] = soil.id
        if management.field["...........XCRD"] is None:
            management.field["...........XCRD"] = weather.LON
        if management.field["...........YCRD"] is None:
            management.field["...........YCRD"] = weather.LAT
        if management.field[".....ELEV"] is None:
            management.field[".....ELEV"] = weather.ELEV

        management.initial_conditions['PCR'] = crop._CODE
        if not management.initial_conditions['ICDAT']:
            management.initial_conditions['ICDAT'] = \
                management.sim_start.strftime('%y%j')
        
        initial_swc = []
        for depth, layer in soil.layers.items():
            initial_swc.append((
                depth, 
                layer['SLLL'] + management.initial_swc \
                    * (layer['SDUL'] - layer['SLLL'])
            ))
        table = TabularSubsection(initial_swc)
        table.columns = ['ICBL', 'SH2O']
        table = table.sort_values(by='ICBL').reset_index(drop=True)
        table['SNH4'] = [0.]*len(table)
        table['SNO3'] = [1.] + [0.]*(len(table)-1)
        if crop.crop_name in ROOTS:
            assert not any(pd.isna([management.planting_details['PLWT'], management.planting_details['SPRL']])), \
                f"PLWT, SPRL transplanting parameters are mandatory for {crop.crop_name} crop, you must "\
                "define those parameters in management.planting_details"
        management.initial_conditions['table'] = table

        management.simulation_controls['SMODEL'] = crop._SMODEL        

        management_filename = weather.INSI \
            + management.sim_start.strftime('%y01') \
            + f'.{crop._CODE}X'
        management_filename = os.path.join(self._RUN_PATH, management_filename) 
        management.write(filename=management_filename)

        if crop.crop_name in PERENIAL_FORAGES:
            if len(management.mow['table']) < 1:
                warnings.warn('No mow was defined. Define it at the Management.mow attribute')
            management.write_mow(f'{management_filename[:-4]}.MOW')

        crop.write(self._RUN_PATH)
        soil.write(os.path.join(self._RUN_PATH, 'SOIL.SOL'))
        wth_path = os.path.join(self._RUN_PATH, 'Weather')
        weather.write(wth_path, management=management)

        

        with open(os.path.join(self._RUN_PATH, self._CONFILE), 'w') as f:
            f.write(f'WED    {wth_path}\n')
            f.write(f'M{crop._CODE}    {self._RUN_PATH} dscsm048 {crop._SMODEL}{VERSION}\n')
            f.write(f'CRD    {self._CRD_PATH}\n')
            f.write(f'PSD    {os.path.join(self._STATIC_PATH, "Pest")}\n')
            f.write(f'SLD    {self._SLD_PATH}\n')
            f.write(f'STD    {self._STD_PATH}\n')

        exc_args = [self._BIN_PATH, 'C', os.path.basename(management_filename), '1']
        excinfo = subprocess.run(exc_args, 
            cwd=self._RUN_PATH, capture_output=True, text=True
        )
        for line in clean_comments(excinfo.stdout.split('\n')):
            sys.stdout.write(line + '\n')

        assert excinfo.returncode == 0, 'DSSAT execution Failed, check '\
            + f'{os.path.join(self._RUN_PATH, "ERROR.OUT")} file for a'\
            + ' detailed report'

        OUTPUT_FILES = [i for i in os.listdir(self._RUN_PATH) if i[-3:] == 'OUT']
        self.OUTPUT_LIST = [
            var for var in OUTPUTS
            if management.simulation_controls.get(OUTPUT_MAP.get(var)) in ("Y", None)
        ]
        
        for file in self.OUTPUT_LIST:
            assert f'{file}.OUT' in OUTPUT_FILES, \
                f'{file}.OUT does not exist in {self._RUN_PATH}'
            table_start = -1
            with open(os.path.join(self._RUN_PATH, f'{file}.OUT'), 'r', encoding='cp437') as f:
                while True:
                    table_start += 1
                    if '@' in f.readline():
                        break
            try:  
                df = pd.read_csv(
                    os.path.join(self._RUN_PATH, f'{file}.OUT'),
                    skiprows=table_start, sep=' ', skipinitialspace=True
                )
            except UnicodeDecodeError:
                with open(os.path.join(self._RUN_PATH, f'{file}.OUT'), 'r', encoding='cp437') as f:
                    lines = f.readlines()
                with open(os.path.join(self._RUN_PATH, f'{file}.OUT'), 'w', encoding='utf-8') as f:
                    f.writelines(lines[table_start:])
                df = pd.read_csv(
                    os.path.join(self._RUN_PATH, f'{file}.OUT'),
                    skiprows=0, sep=' ', skipinitialspace=True
                )
            if all(('@YEAR' in df.columns, 'DOY' in df.columns)):
                df['DOY'] = df.DOY.astype(int).map(lambda x: f'{x:03d}')
                df['@YEAR'] = df['@YEAR'].astype(str)
                df.index = pd.to_datetime(
                    (df['@YEAR'] + df['DOY']),
                    format='%Y%j'
                )
            self._output[file] = df
        return

    def close(self):
        '''
        Removes the simulation environment (tmp folder and files).
        '''
        shutil.rmtree(self._RUN_PATH, **WIN_SHUTIL_KWARGS)
        sys.stdout.write(f'{self._RUN_PATH} and its content has been removed.\n')

    @property
    def output(self):
        if len(self._output) < 1:
            warnings.warn("No output has been saved")
            return None
        return self._output

    

