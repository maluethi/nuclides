from . decays import Decay
from . util import _get_name, _get_Z, _check_N_exists, _get_nuc_info, get_decays
from dataclasses import dataclass
from typing import List
import re
import sqlalchemy as db
from pkg_resources import resource_filename

engine = db.create_engine( f'sqlite:///{resource_filename(__name__, "data/nuclides.db")}')
connection = engine.connect()
metadata = db.MetaData()
decay_table = db.Table('decays', metadata, autoload=True, autoload_with=engine)


class Nuclide:
    """
        A Class to represent a nuclide.

        Attributes:
            name: name of the associate element
            Z: number of protons
            N: number of neutrons
            A: Z + N

            mass: mass of the nuclide
            mass_error: uncertainty on the mass
            mass_excess: energy excess over the mass number (A) in keV
            mass_excess_error: uncertainty on the mass excess

            stable: wether the nuclide is stable or not
            abundance: natural occurence of the nuclide (only applicable if stable or long-lived)
            abundance_error: uncertainty on the abundance

            decays: List of associate decays

            _nuc_id: key in database

   """


    def __init__(self, *args, **kwargs):
        ''' Nuclide('Ti-48'), Nuclide('Ti48')  or
            Nuclide(Z=20, N=20) or Nuclide(name=Ti, N=48)
            or Nuclide(A=123, N=45) or Nuclide(A=123, Z=32)'''
        if len(args) == 1:      # Ti-48 or Ti48 ot 48Ti
            _name = re.findall(r'[a-z]{1,2}', args[0], flags=re.IGNORECASE)[0]
            _A = re.findall(r'\d{1,3}', args[0], flags=re.IGNORECASE)[0]

            self.Z = _get_Z(_name)
            _N = int(_A) - self.Z
            if _check_N_exists(_N, name=_name):
                self.N = _N
            else:
                raise ValueError(f'Requested nuclide does not exist, assuming A={_A}, name={_name}')

        elif len(kwargs) == 2:          # N=12, name='Ti' or N=12
            _N = kwargs['N']        # Neutron number must always be supplied
            if 'name' in kwargs:
                _name = kwargs['name']
                self.Z = _get_Z(_name)
            elif 'Z' in kwargs:
                _Z = int(kwargs['Z'])
                _name = _get_name(_Z)
                self.Z = _Z

            if _check_N_exists(_N, name=_name):
                self.N = _N
            else:
                raise ValueError(f'{self.name} with neutron number N={_N} does not exist')

        else:
            raise ValueError("Not enough data provided for a Nuclide")
        self.A = self.N + self.Z
        self.name = _name + f'-{self.A}'

        attrs = _get_nuc_info(self.Z, self.N)

        self.mass = attrs['mass']
        self.mass_error = attrs['mass_error']
        self.mass_defect = attrs['mass_defect']
        self.mass_defect_error = attrs['mass_defect_error']
        self.stable = attrs['stable']
        self.abundance = attrs['abundance']
        self.abundance_error = attrs['abundance_error']
        self.isomer = attrs['isomer']
        self._nuc_id = attrs['_nuc_id']
        self.decays = get_decays(self)

    def __repr__(self):
        if self.stable:
            string = f'{self.name} (Z={self.Z}, N={self.N}) (stable)' \
                  f' abundance: {self.abundance} \u00B1 {self.abundance_error} %' \
                  #f' mass_def:  {self.mass_defect} \u00B1 {self.mass_defect_error} keV'

        else:
            string = f'{self.name} (Z={self.Z}, N={self.N}) (unstable)'

            for dec in self.decays:
                string += " " + str(dec)

        return string
