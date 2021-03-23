### Usage
```
>>> from nuclides.element import Element
>>> Ti = Element('Ti)
>>> print(Ti[46])

Ti-46 (Z=22, N=24) (stable) abundance: 8.25 ± 0.03 %

>>> decays = Ti[59].decays
>>> for dec in decays:
        print(dec)

b-: T_12 = 0.0285 ± 0.0019s, br = 100.0 ± 0.0%
b-n: T_12 = 0.0285 ± 0.0019s, br = 0.3 ± 0.0%
b-2n: T_12 = 0.0285 ± 0.0019s, br = 0.01 ± 0.0%

>>> T12 = Ti[44].decays[0].half_life
>>> BR = Ti[44].decays[0].branching_ratio
>>> print(f'T-44 most probable decay: half-life: {T12}s, branching ratio: {BR}')

T-44 most probable decay: half-life: 59.1s, branching ratio: 100.0

```


### TODO
- [ ] Implement a nuclide class factory (e.g from nuclide import Au)
- [ ] Clean up class structure
- [ ] Fix unstable abundances
- [ ] Implement proper decay classes (also delayed decays)
- [ ] Write better tests (with test.db and test cases)
- [ ] Documentation
- [ ] Test endge cases
- [ ] implement extrapolation flag in database
- [ ] what to do with isomers
- [ ] add atomic mass (and beta-decay energy) from mass16round.txt
- [ ] organize database / utils
