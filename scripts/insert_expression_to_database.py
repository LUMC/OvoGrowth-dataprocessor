import time, sys
from helpers.Database import db


def get_cell_ids(cell_markers, DB):
    cell_ids = []
    for cell_marker in cell_markers:
        cell_id = DB.connection.execute('select id from cell where cell_marker = "{cell}"'
                                        .format(cell=cell_marker)).fetchone()[0]
        cell_ids.append(cell_id)
    return cell_ids


def insert_expression_to_db(dialect, driver, host, username, password, database, expression_file):
    DB = db(dialect, driver, host, username, password)
    DB.connect_to_db(database)
    with open(expression_file) as f:
        line_n = 0
        for line in f:
            line_n+=1
            if line_n == 1:
                items = line.replace('\n', '').split("\t")
                items.pop(0)
                cell_markers = get_cell_ids(items, DB)
                continue
            line_items = line.replace('\n', '').split("\t")
            gene_symbol = line_items[0]
            line_items.pop(0)
            gene_id = DB.connection.execute("select id from gene where symbol = '{gene}'"
                                            .format(gene=gene_symbol)).fetchone()
            print("Inserted expression for {gene} among all cells".format(gene=gene_symbol))
            values = ""
            for i in range(len(cell_markers)):
                values +="{next}('{gene}', '{cell}', '{CPM}')"\
                    .format(gene=gene_id[0], cell=cell_markers[i], CPM=line_items[i], next=(", " if i > 0 else ""))
            DB.connection.execute("INSERT INTO expression (gene, cell, CPM) VALUES {values}".format(values=values))

    DB.connection.close()

if __name__ == '__main__':
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

