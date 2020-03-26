import nuclides.decays as d

import sqlalchemy as db

engine = db.create_engine('sqlite:///../nuclides/utils/nuclides.db')
connection = engine.connect()
metadata = db.MetaData()
decay_table = db.Table('decays', metadata, autoload=True, autoload_with=engine)

db.select
a = d.Alpha(1, 0.2)


print(a)


