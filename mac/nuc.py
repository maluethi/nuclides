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




Ti = Element("V")

for nuc in Ti:
    print(nuc)
