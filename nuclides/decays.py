from dataclasses import dataclass
import re

neutron = 1
proton = 1


#@dataclass(init=False)
@dataclass
class Decay:
    name: str
    dZ: int = None
    dN: int = None

    half_life: float = None
    half_life_error: float = None
    half_life_rel: str = None

    branching_ratio: float = None
    branching_ratio_error: float = None
    branching_ratio_rel: str = None

    delayed: bool = False

    def __post_init__(self):
        if self.half_life is None:
            raise ValueError("Half-Life not set")

        if self.branching_ratio is None:
            self.branching_ratio = 'unknown'
            self.branching_ratio_error = ''

        #if self.branching_ratio <= 0 or self.branching_ratio > 1:
        #    raise ValueError("Branching ratio must be in the range (0,1]")

        if self.half_life <= 0:
            raise ValueError("Half-Life must be larger than 0 seconds")

    def __str__(self):
        return f'{self.name}: T_12 {self.half_life_rel} {self.half_life} \u00B1 {self.half_life_error}s, ' \
               f'br {self.branching_ratio_rel} {self.branching_ratio} \u00B1 {self.branching_ratio_error}%'


@dataclass
class Alpha(Decay):
    name = 'a'
    dN = -2 * proton
    dZ = -2 * neutron


@dataclass
class BetaPlus(Decay):
    name = 'b+'
    dZ = -1 * proton
    dN = 1 * neutron


@dataclass
class BetaMinus(Decay):
    name = 'b-'
    dZ = 1 * proton
    dN = -1 * neutron


@dataclass
class Fission(Decay):
    pass


@dataclass
class NProtonDecay(Decay):
    n_protons: int = 1
    dN = 0

    def __post_init__(self):
        self.dZ = - self.n_protons * proton
        self.name = f'{self.n_protons if self.n_protons > 1 else ""}p'
        super().__post_init__()


@dataclass
class NNeutronDecay(Decay):
    n_neutrons: int = 1
    dZ = 0

    def __post_init__(self):
        self.dN = - self.n_neutrons * neutron
        self.name = f'{self.n_neutrons if self.n_neutrons > 1 else ""}n'
        super().__post_init__()

@dataclass
class Igamma(Decay):
    name = 'Igamma'
    dZ = 0
    dN = 0

def _dec_parser(key: str):
    prim_dec = ['a', 'b-', 'b\+', 'p', 'n', 'it', 'is', 'ec', 'e\+', 'sf', 'd', ]

    key = key.strip(' ')
    regex = '|'.join(prim_dec)
    split = re.findall(f'({regex})', key)

