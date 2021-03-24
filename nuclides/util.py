import sqlalchemy as db
from . import nuclide
from . import decays
from pkg_resources import resource_filename

_engine = db.create_engine( f'sqlite:///{resource_filename(__name__, "data/nuclides.db")}')
_connection = _engine.connect()
_metadata = db.MetaData()
_elements = db.Table('elements', _metadata, autoload=True, autoload_with=_engine)
_nuclides_table = db.Table('nuclides', _metadata, autoload=True, autoload_with=_engine)
_decay_table = db.Table('decays', _metadata, autoload=True, autoload_with=_engine)


def _get_name(Z):
    query = db.select([_elements]).where(_elements.columns.Z == Z)
    res_prox = _connection.execute(query)
    try:
        name = res_prox.fetchall()[0][1]
    except IndexError:
        raise ValueError(f'Element with {Z} does not exist')
    return name


def _get_Z(name):
    query = db.select([_elements]).where(_elements.columns.name == name)
    res_prox = _connection.execute(query)
    try:
        Z = res_prox.fetchall()[0][0]
    except IndexError:
        raise ValueError(f'Element with {name} does not exist')
    return int(Z)


def _get_nuc_info(Z, N, isomer=False):
    query = db.select([_nuclides_table]).where(db.and_(_nuclides_table.columns.Z == Z,
                                                       _nuclides_table.columns.N == N,
                                                       _nuclides_table.columns.isomer == isomer))

    res_prox = _connection.execute(query)
    res = res_prox.fetchall()[0]
    return {'mass': res[3], 'mass_error': res[4],
            'mass_defect': res[5], 'mass_defect_error': res[6],
            'stable': res[7], 'abundance': res[8], 'abundance_error': res[9], 'isomer': res[10], '_nuc_id': res[0]}

def _get_isotopes(Z, isomer=False):
    query = db.select([_elements]).where(db.and_(_elements.columns.Z == Z,
                                                 _nuclides_table.columns.isomer == isomer))

    res_prox = _connection.execute(query)
    elem_data = res_prox.fetchall()[0]

    elem_nstart = elem_data[2]
    elem_nrange = elem_data[3]

    nuclides = []
    for N in range(elem_nstart, elem_nstart + elem_nrange):
        nuclides.append(nuclide.Nuclide(N=N, Z=Z))

    return nuclides


def get_decays(nuclide):
    query = db.select([_decay_table]).where(_decay_table.columns.nuclide_id == nuclide._nuc_id)
    res_prox = _connection.execute(query)
    dec_data = res_prox.fetchall()

    deca = []
    for dec in dec_data:
        deca.append(decays.Decay(name=dec[2],
                                branching_ratio=dec[3], branching_ratio_error=dec[4], branching_ratio_rel=dec[5],
                                half_life=dec[6], half_life_error=dec[7], half_life_rel=dec[8]))

    return deca


def _check_N_exists(N, **kwargs):
    if 'name' in kwargs:
        Z = _get_Z(kwargs['name'])
    elif 'Z' in kwargs:
        Z = kwargs['Z']
    else:
        raise ValueError('Not enough information for query')
    query = db.select([_nuclides_table]).where(db.and_(_nuclides_table.columns.Z == Z,
                                                       _nuclides_table.columns.N == N))

    res_prox = _connection.execute(query)
    res = res_prox.fetchall()
    if res:
        return True
    else:
        return False
