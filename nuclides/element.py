
from .nuclide import Nuclide
from . util import _get_Z, _get_name
from dataclasses import dataclass
from typing import List

import sqlalchemy as db
from sqlalchemy import and_
from pkg_resources import resource_filename

engine = db.create_engine( f'sqlite:///{resource_filename(__name__, "data/nuclides.db")}')
connection = engine.connect()
metadata = db.MetaData()
elements = db.Table('elements', metadata, autoload=True, autoload_with=engine)
nuclides_table = db.Table('nuclides', metadata, autoload=True, autoload_with=engine)


class Element:
    def __init__(self, constructor):

        if type(constructor) == str:
            self.Z = _get_Z(constructor)
            self.name = constructor
        elif type(constructor) == int or type(constructor) == float:
            self.name = _get_name(int(constructor))
            self.Z = int(constructor)
        else:
            raise TypeError("Unknown type of nuclide specifier")

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

    def _get_isotopes(self, isomer=False):
        query = db.select([elements]).where(elements.columns.Z == self.Z)

        res_prox = connection.execute(query)
        elem_data = res_prox.fetchall()[0]

        elem_nstart = elem_data[2]
        elem_nrange = elem_data[3]

        nuclides = []
        for N in range(elem_nstart, elem_nstart + elem_nrange):
            nuclides.append(Nuclide(N=N, Z=self.Z))

        return nuclides
