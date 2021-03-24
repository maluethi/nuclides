from . util import _get_Z, _get_name, _get_isotopes


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

        self.isotopes = sorted(_get_isotopes(self.Z), key=lambda nu: nu.N)
        self.isomers = sorted(_get_isotopes(self.Z, isomer=True), key=lambda nu: nu.N)      # TODO: This is failing!
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
