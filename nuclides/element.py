
from .nuclide import Nuclide
from dataclasses import dataclass
from typing import List

import sqlalchemy as db
from sqlalchemy import and_

engine = db.create_engine('sqlite:///../nuclides/utils/nuclides.db')
connection = engine.connect()
metadata = db.MetaData()
elements = db.Table('elements', metadata, autoload=True, autoload_with=engine)
nuclides_table = db.Table('nuclides', metadata, autoload=True, autoload_with=engine)


class Element:
    def __init__(self, name):
        self.name = name
        self.Z = self._get_Z()
        self.isotopes = sorted(self._get_isotopes(), key=lambda nu: nu.N)
        self.isomers = sorted(self._get_isotopes(), key=lambda nu: nu.N)
        self._first_avail = self.isotopes[0].A
        self.n_nuclides = len(self.isotopes)

        self._idx = 0

    def __getitem__(self, A):

        idx = [idx for idx, nuc in enumerate(self.isotopes) if nuc.A == A]
        if not idx:
            raise ValueError('No data for this nuclide available')

        return self.isotopes[idx[0]]

    def __iter__(self):
        return self

    def __next__(self):
        if self._idx < self.n_nuclides:
            res = self.isotopes[self._idx]
            self._idx += 1
            return res
        else:
            raise StopIteration

    def _get_Z(self):
        query = db.select([elements]).where(elements.columns.name == self.name)
        res_prox = connection.execute(query)
        Z = res_prox.fetchall()[0][0]
        return Z

    def _get_isotopes(self, isomer=False):
        query = db.select([nuclides_table]).where(and_(
            nuclides_table.columns.Z == self.Z,
            nuclides_table.columns.isomer == isomer)
        )

        res_prox = connection.execute(query)
        nuc_data = res_prox.fetchall()

        nuclides = []
        for nuc in nuc_data:
            nuclides.append(Nuclide(name=self.name, Z=self.Z, N=nuc[2],
                                    mass_defect=nuc[5], mass_defect_error=nuc[6],
                                    stable=nuc[7],
                                    abundance=nuc[8], abundance_error=nuc[9],
                                    decays=[],
                                    _nuc_id=nuc[0]))

        return nuclides
