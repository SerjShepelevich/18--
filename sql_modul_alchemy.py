class Sql_modul_alchemy():

    # name TEXT, mid_salary INT, max_salary INT, min_salary INT, common_skills TEXT'
    def __init__(self, db_name, **kwargs):
        self.db_name = db_name

    def create_db(self):
        from sqlalchemy import create_engine, MetaData, Table
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import mapper, sessionmaker, clear_mappers

        engine = create_engine(f'sqlite:///{self.db_name}', echo = False)
        Base = declarative_base()

        class Record(Base):
            from sqlalchemy import Column, Integer, String, Float
            __tablename__ = 'table'
            id = Column(Integer, primary_key = True)
            name = Column(String)
            mid_salary = Column(Float)
            max_salary = Column(Integer)
            min_salary = Column(Integer)
            common_skills = Column(String)

            def __init__(self, name, mid_salary, max_salary, min_salary, common_skills):
                self.name = name
                self.mid_salary = mid_salary
                self.max_salary = max_salary
                self.min_salary = min_salary
                self.common_skills = common_skills

            def __str__(self):
                return f'{self.id}, {self.name}, {self.mid_salary}, {self.max_salary}, {self.min_salary}, {self.common_skills}'

        #Record(Base)

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind = engine)
        session = Session()
        session.commit()
        clear_mappers()

    def insert_record(self, data):
        from sqlalchemy import create_engine, MetaData, Table
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import mapper, sessionmaker, clear_mappers
        engine = create_engine(f'sqlite:///{self.db_name}', echo = False)
        metadata = MetaData(engine)
        meta_param = Table('table',metadata,autoload = True)
        clear_mappers()
        mapper(Record, meta_param)
        Session = sessionmaker(bind = engine)
        session = Session()
        session.add(Record(data[0], data[1], data[2], data[3], data[4]))
        session.commit()
        clear_mappers()

    def loadSession(self):
        from sqlalchemy import create_engine, MetaData, Table
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import mapper, sessionmaker, clear_mappers
        engine = create_engine(f'sqlite:///{self.db_name}', echo = False)
        clear_mappers()
        metadata = MetaData(engine)
        meta_param = Table('table', metadata, autoload = True)
        mapper(Record, meta_param)
        Session = sessionmaker(bind = engine)
        session = Session()
        return session

class Record(object):
    from sqlalchemy import Column, Integer, String, Float
    __tablename__ = 'table'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    mid_salary = Column(Float)
    max_salary = Column(Integer)
    min_salary = Column(Integer)
    common_skills = Column(String)

    def __init__(self, name, mid_salary, max_salary, min_salary, common_skills):
        self.name = name
        self.mid_salary = mid_salary
        self.max_salary = max_salary
        self.min_salary = min_salary
        self.common_skills = common_skills

    def __str__(self):
        return f'{self.id}, {self.name}, {self.mid_salary}, {self.max_salary}, {self.min_salary}, {self.common_skills}'

    def convert(self):
        return [self.id, self.name, self.mid_salary, self.max_salary, self.min_salary, self.common_skills]

# data = ('python', 3454656 / 345, 150000, 65000, '<sdfswerweve', )
#
# Sql_modul_alchemy('alchemy.sqlite').create_db()
# Sql_modul_alchemy('alchemy.sqlite').insert_record(data)
# session = Sql_modul_alchemy('alchemy.sqlite').loadSession()
# records = session.query(Record).all()
#
# # for record in records:
# #     print(record)
# rec = records[len(records)-1]
# print(rec.convert()[1])