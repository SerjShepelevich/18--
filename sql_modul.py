#pip install pysqlite3

# создаем базу
class Sql_modul():

    def __init__(self, db_name, config_db):
        self.db_name = db_name
        self.config_db = config_db


    def create_db(self):
        import sqlite3 as lite
        import sys
        connect = None
        try:
            connect = lite.connect(self.db_name)
            cur = connect.cursor()
            cur.execute('SELECT SQLITE_VERSION()')
            data = cur.fetchone()[0]
            print(f"SQLite version: {data}")
        except lite.Error as e:
            print(f"Error {e.args[0]}:")
            sys.exit(1)
        connect.commit()
        connect.close()
        Sql_modul.create_db_table(self)

    # создаем таблицу
    def create_db_table(self):
        import sqlite3 as lite
        connect = None
        connect = lite.connect(self.db_name)
        cur = connect.cursor()
        cur.execute("CREATE TABLE records(" + self.config_db + ")")
        connect.commit()
        connect.close()

    # добавляем запись в базу
    def insert_record(self, data):
        import sqlite3 as lite
        import sys
        import os.path
        if os.path.exists(self.db_name) is not True:
            Sql_modul.create_db(self)
        connect = None
        try:
            connect = lite.connect(self.db_name)
            cursor = connect.cursor()
            cursor.execute("select * from records")
            results = cursor.fetchall()
            number_new_rec = len(results)
            config_rec = Sql_modul.create_config_rec(self)
            cursor.execute("INSERT INTO records VALUES" + config_rec ,[number_new_rec+1] + data)
            connect.commit()
            connect.close()
        except lite.Error as e:
            print(f"Error {e.args[0]}:")
            sys.exit(1)

    # конфигурируем строчку записи, так как не знаем сколько колонок в базе будет
    # фактически делаем универсальный способ записи в базу
    def create_config_rec(self):
        config_db = self.config_db.split(',')
        config_rec = '('
        for i in range(len(config_db)):
            config_rec = config_rec + '?'
            if i < len(config_db)-1:
                config_rec = config_rec + ','
            if i == len(config_db)-1:
                config_rec = config_rec + ')'
        return config_rec

    # Прочитаем записи из базы
    def read_data(self, uname):
        import sqlite3 as lite
        import sys
        import os.path

        if os.path.exists(self.db_name) is not True:
            Sql_modul.create_db(self)

        connect = None

        try:
            connect = lite.connect(self.db_name)
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM records')
            names_colums = list(map(lambda x: x[0], cursor.description))
            cursor.execute("SELECT * FROM records WHERE name=?", (uname,))
            rows = cursor.fetchall()
            connect.close()
        except lite.Error as e:
            print(f"Error {e.args[0]}:")
            connect.close()
            rows = None
            sys.exit(1)
        return rows




#create_db("test.db", 'id INT, name TEXT, mid_salary INT, max_salary INT, min_salary INT, common_skills TEXT')
# config_db = 'id INT, name TEXT, mid_salary INT, max_salary INT, min_salary INT, common_skills TEXT'
# data = ["python", 70000 , 120000, 40000, "sqllite3"]
# Sql_clas = Sql_modul("test.db", config_db)
# Sql_clas.insert_record(data)
# Sql_clas.read_data("python")