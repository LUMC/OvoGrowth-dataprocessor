import time, sys
from helpers.Database import db


def insert_genes_to_db(dialect, driver, host, username, password, database, gene_file):
    DB = db(dialect, driver, host, username, password)
    DB.connect_to_db(database)
    with open(gene_file) as f:
        gene_values = ""
        n=0
        for line in f:
            [ensg, symbol, description] = line.replace('\n', '').split(';')
            description = description.replace('"', "")
            symbol = symbol.split(".")[0]
            gene_values += "{next}('{symbol}', '{desc}')".format(next=(", " if n > 0 else ""),
                                                             symbol=symbol, desc=description
                                                             )
            n=+1
        DB.connection.execute("INSERT IGNORE INTO gene (symbol, description) VALUES {values}"
                  .format(values=gene_values))
    with open(gene_file) as f:
        gene_origin_values = ""
        n=0
        for line in f:
            [ensg, symbol, description] = line.replace('\n', '').split(';')
            symbol = symbol.split(".")[0]
            gene_id = DB.connection.execute("select id from gene where symbol = '{symbol}'".format(symbol=symbol))\
                .fetchone()[0]
            gene_origin_values += "{next}('{gene}', '{ensg}')".format(next=(", " if n > 0 else ""), gene=gene_id, ensg=ensg)
            n=+1
        DB.connection.execute("INSERT IGNORE INTO gene_origin (gene, ensg) VALUES {values}"
                  .format(values=gene_origin_values))
    DB.connection.close()


if __name__ == '__main__':
    try:
        arg = sys.argv
        db_name = arg[1]
        db_host = arg[2]
        db_username = arg[3]
        db_password = arg[4]
        file_genes = arg[5]
        output = arg[6]

        insert_genes_to_db('mysql', 'pymysql', db_host, db_username, db_password, db_name, file_genes)
        with open(output, 'w') as f:
            f.write("all records are inserted to the db")
    except Exception as a:
        print(a)

