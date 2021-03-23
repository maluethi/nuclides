from nuclides.decays import Alpha, BetaMinus
from nuclides.element import Element
from nuclides.nuclide import Nuclide

#from nuclides import Si

## basic usage
#isotopes = Si[46, 47, 48, 49]
#Si46 = Si[46]
#t12 = Si46.decays.half_life
#mass = Si46.mass
#
#for nuc in isotopes:
#    print(nuc.mass)
#    print(nuc.stable)
import sqlalchemy as db

from nuclides.element import Element
from nuclides.nuclide import Nuclide
from nuclides.util import _check_N_exists, _get_nuc_info

nuc = Nuclide('Ti-48')
print(nuc)

nuc = Nuclide('Ti51')
print(nuc)


Ti = Element('Ti')
print(Ti[46])
print(Ti[59])

Au = Element('Au')
for iso in Au:
    print(iso)

Zn = Element('Zn')

decays = Ti[60].decays
for dec in decays:
    print(dec)

T12 = Ti[44].decays[0].half_life
BR = Ti[44].decays[0].branching_ratio

print(f'T-44 most probable decay: half-life: {T12}s, branching ratio: {BR}')

Si = Element('Si')
print(Si[27])
O = Element('O')
print(O[28])


