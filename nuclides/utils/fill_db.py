from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nuclides.utils.gen_db import Decays, Nuclides, Elements, Base

engine = create_engine('sqlite:///nuclides.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Insert an Element in the element table
new_element = Elements(name="Ma", Z=10, NStart=11, NRange=2)
session.add(new_element)
session.commit()


Ti = session.query(Elements).filter(Elements.Z == 10)[0]

print(Ti)
# Insert an Address in the address table
new_nuclide = Nuclides(Z=10, N=11, mass=1.2, stable=True, element=Ti)
session.add(new_nuclide)
session.commit()
