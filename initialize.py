from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database_setup import Base, Users

engine = create_engine('sqlite:///crudlab.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# You can add some starter data for your database here.
Mahmoud=Users(
    name = 'Mahmoud Khalifa',
    email = 'mahmoud.khalifa00@gmail.com',
    password = '123'
    )
session.add(Mahmoud)
session.commit()
noura=Users(
    name = 'noura barakat',
    email = 'nourabarakat05@gmail.com',
    password = '111'
    )

session.add(noura)
session.commit()

