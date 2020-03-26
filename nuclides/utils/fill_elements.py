from nuclides.utils.gen_db import Decays, Nuclides, Elements, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import numpy as np
import argparse




parser = argparse.ArgumentParser(description='Reads NuBase2016 asciii file and writes elements into database ')
parser.add_argument('infile', type=argparse.FileType('r'),
                    help='Input data file (required)')
parser.add_argument('dbname', type=str,
                    help='Output data file (required)')
args = parser.parse_args()

print(args.dbname)

engine1 = create_engine('sqlite:///nuclides.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine1

DBSession = sessionmaker(bind=engine1)
session = DBSession()

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

raw_data = []

# skip first line
next(args.infile)

for idx, line in enumerate(args.infile):
    A = int(line[0:3])
    Z = int(line[4:7])
    isomer = False if line[7] == '0' else True
    N = A - Z
    name = element_names[Z - 1]
    stbl = N if line[61:65] == 'stbl' else -1

    df = (Z, N, name, stbl, isomer)
    raw_data.append(df)

raw_data = np.array(sorted(raw_data, key=lambda Z: Z[0]))

for name in element_names:
    idxs = np.where(raw_data[:, 2] == name)
    this_element = raw_data[idxs]
    print(this_element)
    stbl = []
    if len(idxs[0]) > 0:
        idx_start = raw_data[idxs][0][1]

        # getting the stable isotopes
        for entry in this_element:
            if int(entry[3]) > -1:
                stbl.append(int(entry[3]))

        # handle isomers (not relevant for elements db):
        if this_element[0][4] == True:
            np.delete(this_element, 0)
            print('bla')
        unique_entries = np.unique(this_element[:, 1])
        idx_range = len(unique_entries)

    else:
        continue
    Z = int(this_element[1,0])
    print(name, Z, idx_start, idx_range)
    # Insert an Element in the element table

    new_element = Elements(name=name, Z=Z, NStart=idx_start, NRange=idx_range)
    session.add(new_element)

session.commit()
