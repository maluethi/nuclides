### Usage
```
>>> from nuclides.element import Element
>>> Ti = Element('Ti)
>>> print(Ti[44], Ti[59])

Ti-46 (Z=22, N=24) (stable) abundance: 8.25 ± 0.03 %
Ti-59 (Z=22, N=37) (unstable) b-: T_12 = 0.0285 ± 0.0019s, br = 100.0 ± 0.0% b-n: T_12 = 0.0285 ± 0.0019s, br = 0.3 ± 0.0% b-2n: T_12 = 0.0285 ± 0.0019s, br = 0.01 ± 0.0%
```


### TODO
- [ ] Implement a nuclide class factory (e.g from nuclide import Au)
- [ ] Clean up class structure
- [ ] Fix unstable abundances
- [ ] Implement proper decay classes (also delayed decays)
- [ ] Write better tests (with test.db and test cases)
- [ ] Documentation
