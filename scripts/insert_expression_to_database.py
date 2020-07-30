import time, sys
from helpers.Database import db


def get_cell_ids(cell_markers, reference_id, DB):
    cell_ids = []
    for cell_marker in cell_markers:
        print(reference_id, cell_marker)
        cell_id = DB.connection.execute('select id from cell where cell_marker = "{cell}" and dataset="{reference_id}"'
                                        .format(cell=cell_marker, reference_id=reference_id)).fetchone()[0]
        cell_ids.append(cell_id)
    return cell_ids


def insert_expression_to_db(dialect, driver, host, username, password, database, expression_file, reference_id):
    DB = db(dialect, driver, host, username, password)
    DB.connect_to_db(database)
    DB.connection.execute('ALTER TABLE `expression` DISABLE KEYS')
    with open(expression_file) as f:
        line_n = 0
        for line in f:
            line_n+=1
            if line_n == 1:
                items = line.replace('\n', '').replace('"', '').split("\t")
                items.pop(0)
                cell_markers = get_cell_ids(items, reference_id, DB)
                continue
            line_items = line.replace('\n', '').split("\t")
            gene_symbol = line_items[0].split(".")[0].replace('"', '')
            line_items.pop(0)
            gene_id = DB.connection.execute("select id from gene where symbol = '{gene}'"
                                            .format(gene=gene_symbol)).fetchone()
            print(gene_symbol)
            values = ""
            for i in range(len(cell_markers)):
                values +="{next}('{gene}', '{cell}', '{CPM}')"\
                    .format(gene=gene_id[0], cell=cell_markers[i], CPM=line_items[i], next=(", " if i > 0 else ""))
            DB.connection.execute("INSERT INTO expression (gene, cell, CPM) VALUES {values}".format(values=values))
            print("Inserted expression for {gene} among all cells".format(gene=gene_symbol))
    DB.connection.execute('ALTER TABLE `expression` ENABLE KEYS')
    DB.connection.close()


if __name__ == '__main__':
    arg = sys.argv
    db_name = arg[1]
    db_host = arg[2]
    db_username = arg[3]
    db_password = arg[4]
    file_expression = arg[5]
    reference_file = arg[6]
    output = arg[7]

    reference_id = open(reference_file).read().replace("\n", "")
    insert_expression_to_db('mysql', 'pymysql', db_host, db_username, db_password, db_name, file_expression, reference_id)
    with open(output, 'w') as f:
        f.write("all records are inserted to the db")

