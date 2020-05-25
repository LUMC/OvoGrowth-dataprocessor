import time, sys
from helpers.Database import db


def insert_expression_to_db(dialect, driver, host, username, password, database, expression_file):
    DB = db(dialect, driver, host, username, password)
    DB.connect_to_db(database)
    with open(expression_file) as f:
        print(f[0])

    DB.connection.close()

if __name__ == '__main__':
    try:
        arg = sys.argv
        db_name_file = arg[1]
        db_host = arg[2]
        db_username = arg[3]
        db_password = arg[4]
        file_expression = arg[5]
        output = arg[6]

        db_name = open(db_name_file).read().replace("\n", "")
        insert_expression_to_db('mysql', 'pymysql', db_host, db_username, db_password, db_name, file_expression)
        with open(output, 'w') as f:
            f.write("all records are inserted to the db")
    except Exception as a:
        print(a)

