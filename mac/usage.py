from nuclides import Nuclide

Au196 = Nuclide('Au-196')
print(Au196)

What = Nuclide(Z=92, N=143)
print(What.name)

from nuclides import Element
Ti = Element('Ti')
print(Ti[46])

decays = Ti[59].decays
for dec in decays:
    print(dec)

T12 = Ti[44].decays[0].half_life
BR = Ti[44].decays[0].branching_ratio
print(f'T-44 most probable decay: half-life: {T12}s, branching ratio: {BR}')
