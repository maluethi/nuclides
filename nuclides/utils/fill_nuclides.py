from nuclides.utils.gen_db import Decays, Nuclides, Elements, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Reads NuBase2016 asciii file and writes nuclides into database ')
parser.add_argument('infile', type=argparse.FileType('r'),
                    help='Input data file (required)')
parser.add_argument('dbname', type=str,
                    help='Output data file (required)')
args = parser.parse_args()

# Base unit for short times: second
# Also added here descriptive 'units'
short_time_units = {'d': 86400.0,
                    'h': 3600.0,
                    'm': 60.0,
                    's': 1.0,
                    'ms': 1e-3,
                    'us': 1e-6,
                    'ns': 1e-9,
                    'ps': 1e-12,
                    'fs': 1e-15,
                    'as': 1e-18,
                    'zs': 1e-21,
                    'ys': 1e-24,
                    'stbl': 'stable',
                    'p-unst': 'unstable',
                    'n-unst': 'unstable',
                    '?': 'unknown'}

# Base unit for long times: year
long_time_units = {'Yy': 1e24,
                   'Zy': 1e21,
                   'Ey': 1e18,
                   'Py': 1e15,
                   'Ty': 1e12,
                   'Gy': 1e9,
                   'My': 1e6,
                   'ky': 1e3,
                   'y': 1.0}

element_names = \
    'H', 'He', 'Li', 'Be', 'B', \
    'C', 'N', 'O', 'F', 'Ne', \
    'Na', 'Mg', 'Al', 'Si', 'P', \
    'S', 'Cl', 'Ar', 'K', 'Ca', \
    'Sc', 'Ti', 'V', 'Cr', 'Mn', \
    'Fe', 'Co', 'Ni', 'Cu', 'Zn', \
    'Ga', 'Ge', 'As', 'Se', 'Br', \
    'Kr', 'Rb', 'Sr', 'Y', 'Zr', \
    'Nb', 'Mo', 'Tc', 'Ru', 'Rh', \
    'Pd', 'Ag', 'Cd', 'In', 'Sn', \
    'Sb', 'Te', 'I', 'Xe', 'Cs', \
    'Ba', 'La', 'Ce', 'Pr', 'Nd', \
    'Pm', 'Sm', 'Eu', 'Gd', 'Tb', \
    'Dy', 'Ho', 'Er', 'Tm', 'Yb', \
    'Lu', 'Hf', 'Ta', 'W', 'Re', \
    'Os', 'Ir', 'Pt', 'Au', 'Hg', \
    'Tl', 'Pb', 'Bi', 'Po', 'At', \
    'Rn', 'Fr', 'Ra', 'Ac', 'Th', \
    'Pa', 'U', 'Np', 'Pu', 'Am', \
    'Cm', 'Bk', 'Cf', 'Es', 'Fm', \
    'Md', 'No', 'Lr', 'Rf', 'Db', \
    'Sg', 'Bh', 'Hs', 'Mt', 'Ds', \
    'Rg', 'Cn', 'Nh', 'Fl', 'Mc', \
    'Lv', 'Ts', 'Og', 'Uue', 'Ubn'


def parse_mass_defect(mass_defect):
    """Returns dict {value, uncertainty, extrapolated}
    parsed from format used by nubase2003"""
    result = {}
    mass_defect = mass_defect.strip()
    result['extrapolated'] = True if mass_defect.count('#') > 0 else False
    if result['extrapolated']:
        mass_defect = mass_defect.replace('#', ' ')
    try:
        mass_defect = mass_defect.split()
        for it in mass_defect:
            it = it.strip()
        if len(mass_defect) == 2:
            result['value'] = float(mass_defect[0])
            result['uncertainty'] = float(mass_defect[1])
        elif len(mass_defect) == 0:
            result['value'] = '?'
            result['uncertainty'] = '?'
        else:
            result['uncertainty'] = '?'
    except (ValueError, IndexError):
        raise ValueError(" {} is not valid mass defect string".format(mass_defect))
    return result


def parse_half_life(half_life):
    """"Half-life given as a string "value unit" white-space separated
           as in nubase
           However sometimes evaluators use "value unit error"
           or "<value unit"
           or "stbl"
           or empty string
           returns dict {half life, unit, uncertainty, extrapolated}
        """
    result = {}
    half_life = half_life.strip()
    result['extrapolated'] = True if half_life.count('#') > 0 else False
    if result['extrapolated']:
        half_life = half_life.replace('#', ' ')

    # Sometimes R=, T=, R< or similar is appearing (whatever it means?)
    if half_life.find('T') > -1 or half_life.find('R') > -1:
        result['value'] = '?'
        result['unit'] = '?'
        result['relation'] = '?'
        result['uncertainty'] = '?'
        return result

    items = half_life.split()

    for it in items:
        it = it.strip()

    if len(items) == 0:
        result['value'] = '?'
        result['uncertainty'] = '?'
        result['unit'] = '?'
        result['relation'] = '?'
    elif items[0] in ['stbl', 'p-unst', 'n-unst']:
        result['value'] = short_time_units[items[0]]
        result['uncertainty'] = ''
        result['unit'] = ''
        result['relation'] = '='
    elif len(items) == 2 or len(items) == 3:
        if short_time_units.get(items[1]) is None and long_time_units.get(items[1]) is None:
            raise ValueError('Could not find half-life unit {}'.format(items[1]))


        if len(items) == 2:
            result['uncertainty'] = '?'
        else:
            splt = re.split('[0-9]*\.?[0-9]+', items[2])
            num = re.search('[0-9]*\.?[0-9]+', items[2])

            if len(splt) > 2:
               result['uncertainty'] = num[0] * short_time_units[splt[-1]]
            else:
                result['uncertainty'] = num[0]


        result['unit'] = items[1]

        if '~' in items[0]:
            result['value'] = items[0].split('~')[-1]
            result['relation'] = '~'
        elif '>' in items[0]:
            result['value'] = items[0].split('>')[-1]
            result['relation'] = '>'
        elif '<' in items[0]:
            result['value'] = items[0].split('<')[-1]
            result['relation'] = '<'
        else:
            result['value'] = items[0]
            result['relation'] = '='
    elif len(items) == 1:
        result['uncertainty'] = '?'

        try:
            split = re.split('[0-9]*\.?[0-9]+', items[0])
            val = re.search('[0-9]*\.?[0-9]+', items[0])

            result['relation'] = split[0]
            result['value'] = val[0]
            result['unit'] = split[1]
        except ValueError as IndexError:
            raise ValueError("String {} is not a valid half life string".format(half_life))

    else:
        raise ValueError("String {} is not a valid half life string".format(half_life))
    return result


def parse_gs_spin(gs_spin):
    """Parses nubase style spin information
        returns dictionary {value, extrapolated} """
    result = {}
    gs_spin = gs_spin.strip()
    result['extrapolated'] = True if gs_spin.count('#') > 0 else False
    if result['extrapolated']:
        gs_spin = gs_spin.replace('#', ' ')
    result['value'] = gs_spin
    return result


def parse_isomer_spin(spin):
    """Parses nubase style spin information
        returns dictionary {value, extrapolated} """
    result = {}
    result['extrapolated'] = True if spin.count('#') > 0 else False
    if result['extrapolated']:
        spin = spin.replace('#', ' ')
    result['value'] = spin[0:8].strip()
    result['T'] = spin[8:].strip('T= ')
    return result


def parse_decay_modes(decay_modes):
    """Parses decay modes string from nubase
        returns list of dictionaries
        [ {mode, value, relation, uncertainty}, {...} ]
        """
    # NuBase evaluators have left some fortran garbage like 'LE' and 'GE'
    # We replace them with proper unicode signs
    decay_modes = decay_modes.replace('le', '\u2264')
    decay_modes = decay_modes.replace('ge', '\u2265')
    decay_modes = decay_modes.replace('#', '')

    # Remove whatever is in [] bracket (some extra info)
    while True:
        begin = decay_modes.find('[')
        end = decay_modes.find(']')
        if begin < 0:
            break
        if end > -1:
            decay_modes = decay_modes[:begin] + decay_modes[end + 1:]
        else:
            decay_modes = decay_modes[:begin]

    decay_list = []
    if len(decay_modes.strip()) == 0:
        empty = {'mode': '?', 'value': '', 'relation': '',
                 'uncertainty': ''}
        decay_list.append(empty)
        return decay_list
    try:
        for item in decay_modes.split(';'):
            # For unknown values string "mode ?" is used
            # but sometimes it is "mode=?"
            # or "mode= ?"
            # we fix this so it always has '=' sign
            question = re.search(r" \?", item)
            if question is not None:
                if item.count('=') == 0:
                    item = re.sub(r" \?", "=?", item)

            # '...' is used in the nubtab12, whatever it means (?!)
            # it can't be unpacked in the next line, since there is
            # no relation symbol
            if item == "...":
                continue

            mode, relation, value = re.split('(=|~|>|<|\u2264|\u2265)',
                                             item)
            error = '0'
            value = value.split()
            if len(value) > 1:
                error = value[1]
            value = value[0]
            decay_mode = {'mode': mode, 'relation': relation, 'value': value,
                          'uncertainty': error}
            decay_list.append(decay_mode)
    except ValueError:
        raise ValueError('Error parsing decay modes string {} nuclide'.format(decay_modes))
    return decay_list

def nb_add_isomer(isomer_data):
        """Adds isomer using nubase style data"""

        isomer_data = isomer_data.strip()

        extrapolated = True if isomer_data.count('#') > 0 else False
        if extrapolated:
            isomer_data = isomer_data.replace('#', ' ')

        isomer_data = isomer_data.split()
        try:
            energy = isomer_data[0].strip()
            error = isomer_data[1].strip()
            # Default is gamma spectrometry
            code = 'Gamma spectometry'
            if len(isomer_data) >= 3 and not (isomer_data[-1].isnumeric()):
                code = isomer_data[-1].strip()
                starred = True if code.count('*') > 0 else False
                if starred:
                    code_comment = 'uncertainty of energy is larger then energy itself'
                    code = code.replace('*', ' ')
                if code == 'MD':
                    code = 'Mass doublet'
                elif code == 'RQ':
                    code = 'Reaction energy difference'
                elif code == 'AD':
                    code = 'Alpha energy difference'
                elif code == 'BD':
                    code = 'Beta energy difference'
                elif code == 'p':
                    code = 'Proton decay'
                elif code == 'XL':
                    code = 'L X-rays'
                elif code == 'Nm':
                    code = 'Estimated value from Nilsson model'
                elif code == 'EU':
                    code = 'Existence under discussion'
                elif code == 'RN':
                    code = 'Proved not to exists'
                elif code == '&':
                    code = 'Ground state and isomer ordering reversed compared to ENSDF'
                else:
                    code = "Code '{}' is not documented'".format(code)

                if starred:
                    code += " " + code_comment

        except (IndexError, ValueError):
            raise ValueError('Error parsing isomer data string {} nuclide'.format(isomer_data))

        result = {'energy': energy,
                  'uncertainty': error,
                  'extrapolated': extrapolated,
                  'comment': code + " " + comment}

        return result

def check_unknown(val):
    return val if val not in ['?', ''] else None


m_neutron = 939565.4133  # in keV
m_proton = 938272.0813  #in keV

m_u = 931494.102  # in keV

engine = create_engine('sqlite:///nuclides.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# skip first line
next(args.infile)

for idx, line in enumerate(args.infile):
    A = int(line[0:3])
    Z = int(line[4:7])
    N = A-Z

    name = element_names[Z - 1]
    print(idx, name, A, Z)

    isomer = False if line[7] == '0' else True
    mass_defect = line[18:38].strip()
    isomer_data = line[38:60].strip()
    half_life = line[60:78].strip()
    spin = line[79:93].strip()
    comment = line[93:109].strip()
    decay_modes = line[110:-1].strip().lower()

    mass_defect = parse_mass_defect(mass_defect)
    half_life = parse_half_life(half_life)
    decay_modes = parse_decay_modes(decay_modes)

    if not isomer:
        spin = parse_gs_spin(spin)
    if isomer:
        spin = parse_isomer_spin(spin)

    if half_life['value'] == 'stable':
        stable = True

        # convert to numeric values in %
        abund = decay_modes[0]['value']
        abund_uncert = decay_modes[0]['uncertainty']
        pot = len(abund.split('.')[1])
        abund = float(abund)
        abund_uncert = round(float(abund_uncert) * 10. ** -pot, pot)


        new_nuclide = Nuclides(Z=Z,
                               N=N,
                               mass_excess=mass_defect['value'],
                               mass_exces_uncertainty=mass_defect['uncertainty'],
                               stable=stable,
                               abundance=abund,
                               abundance_error=abund_uncert,
                               isomer=isomer)
        session.add(new_nuclide)
        session.commit()

    else:
        stable = False

        mass_def = mass_defect['value']
        mass_def_uncert = mass_defect['uncertainty']

        mass_def = mass_def if mass_def != '?' else None
        mass_def_uncert = mass_def_uncert if mass_def_uncert != '?' else None

        new_nuclide = Nuclides(Z=Z,
                               N=N,
                               mass_excess=mass_def,
                               mass_exces_uncertainty=mass_def_uncert,
                               stable=stable,
                               isomer=isomer)

        session.add(new_nuclide)
        session.commit()

        hlf_unit = half_life['unit']
        hlf_val = half_life['value']
        hlf_rel = check_unknown(half_life['relation'])
        hlf_unc = check_unknown(half_life['uncertainty'])



        if hlf_val == 'unstable' or hlf_val == '?':
            continue
        if 'y' in hlf_unit and 'ys' not in hlf_unit:
            hlf = float(hlf_val) * long_time_units[hlf_unit]
            hlf_unc = float(hlf_unc) * long_time_units[hlf_unit] if hlf_unc else None
        else:
            hlf = float(hlf_val) * short_time_units[hlf_unit]
            hlf_unc = float(hlf_unc) * short_time_units[hlf_unit] if hlf_unc else None

        for dec in decay_modes:
            mode = check_unknown(dec['mode'])
            br_ratio = check_unknown(dec['value'])
            br_rel = check_unknown(dec['relation'])
            br_unc = check_unknown(dec['uncertainty'])

            if br_ratio is not None:
                if '#' in br_ratio:
                    pass
            new_decay = Decays(decay_mode=mode,
                               branching=br_ratio,
                               branching_error=br_unc,
                               branching_relation=br_rel,
                               half_life=hlf,
                               half_life_error=hlf_unc,
                               half_life_relation=hlf_rel,
                               nuclide_id=new_nuclide.id)

            session.add(new_decay)
            session.commit()

session.commit()



