import time, sys
from helpers.Database import db


def insert_dataset_to_database(dialect, driver, host, username, password, database, dataset_name):
    DB = db(dialect, driver, host, username, password)
    DB.connect_to_db(database)
    result = DB.connection.execute("INSERT IGNORE INTO dataset (name) VALUES ('{value}')"
                          .format(value=dataset_name))
    DB.connection.close()
    return result.lastrowid

if __name__ == '__main__':
    try:
        arg = sys.argv
        db_name = arg[1]
        db_host = arg[2]
        db_username = arg[3]
        db_password = arg[4]
        dataset_name = arg[5]
        output = arg[6]

        id = insert_dataset_to_database('mysql', 'pymysql', db_host, db_username, db_password, db_name, dataset_name)
        with open(output, 'w') as f:
            f.write(str(id))
    except Exception as a:
        print(a)

