import time, sys
from helpers.Database import db


def insert_genes_to_db(dialect, driver, host, username, password, database, gene_file):
    DB = db(dialect, driver, host, username, password)
    DB.connect_to_db(database)
    with open(gene_file) as f:
        for line in f:
            [ensg, symbol] = line.replace('\n', '').split('\t')
            record = DB.connection.execute("SELECT id FROM gene where symbol = '{symbol}'".format(symbol=symbol))\
                .fetchone()
            if record:
                DB.connection.execute("INSERT INTO gene_origin (gene, ensg) VALUES ('{id}', '{ensg}')"
                                      .format(id=str(record[0]), ensg=ensg))
            else:
                DB.connection.execute("INSERT INTO gene (symbol) VALUES ('{symbol}')"
                                                .format(symbol=symbol))
                gene_id = DB.connection.execute("SELECT LAST_INSERT_ID()").fetchone()
                DB.connection.execute("INSERT INTO gene_origin (gene, ensg) VALUES ('{id}', '{ensg}')"
                                      .format(id=str(gene_id[0]), ensg=ensg))
    DB.connection.close()

if __name__ == '__main__':
    try:
        arg = sys.argv
        db_name_file = arg[1]
        db_host = arg[2]
        db_username = arg[3]
        db_password = arg[4]
        file_genes = arg[5]
        output = arg[6]

        db_name = open(db_name_file).read().replace("\n", "")
        insert_genes_to_db('mysql', 'pymysql', db_host, db_username, db_password, db_name, file_genes)
        with open(output, 'w') as f:
            f.write("all records are inserted to the db")
    except Exception as a:
        print(a)

