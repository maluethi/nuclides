from . decays import Decay
from dataclasses import dataclass
from typing import List

import sqlalchemy as db

engine = db.create_engine('sqlite:///../nuclides/utils/nuclides.db')
connection = engine.connect()
metadata = db.MetaData()
decay_table = db.Table('decays', metadata, autoload=True, autoload_with=engine)

@dataclass
class Isotope:
    name: str
    Z: int
    N: int
    mass_defect: float
    mass_defect_error: float
    decays: List[Decay]

    stable: bool = False
    abundance: float = None
    abundance_error: float = None
    _nuc_id: int = None
    A: int = None

    def __post_init__(self):
        if len(self.decays) > 0:
            if self.abundance is not None:
                raise ValueError("If nuclide is not stable (i.e there are decays specified), abundance can't be set")

            if self.stable is True:
                raise ValueError("Nuclide can not be stable and have decays")

        total_br = sum([dec.branching_ratio for dec in self.decays])
        if total_br > 1.0:
            raise ValueError("Total branching ratio is greater than 1")

        if self.Z < 0:
            raise ValueError('We can not have negative number of protons')

        if self.N < 0:
            raise ValueError('We can not have negative number of neutrons')

        self.A = self.N + self.Z
        # sort the list according to the branching ratio
        self.decays = self._fill_decays()

        self.name = f'{self.name}-{self.A}'

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

    def _fill_decays(self):
        query = db.select([decay_table]).where(decay_table.columns.nuclide_id == self._nuc_id)
        res_prox = connection.execute(query)
        dec_data = res_prox.fetchall()

        decays = []
        for dec in dec_data:
            decays.append(Decay(name=dec[2],
                                branching_ratio=dec[3], branching_ratio_error=dec[4], branching_ratio_rel=dec[5],
                                half_life=dec[6], half_life_error=dec[7], half_life_rel=dec[8]))

        return decays
