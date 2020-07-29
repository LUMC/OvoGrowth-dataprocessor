import time, sys
from helpers.Database import db


def insert_cells_to_db(dialect, driver, host, username, password, database, cells_file, reference_id):
    DB = db(dialect, driver, host, username, password)
    DB.connect_to_db(database)
    n = 0
    with open(cells_file) as f:
        values = ""
        for line in f:
            n += 1
            if n == 1:
                continue
            [cell_marker, cluster_id, tsne_1, tsne_2] = line.replace('\n', '').split('\t')
            print(cell_marker, cluster_id, tsne_1, tsne_2)
            values += "{next}('{dataset}', '{cell_marker}', " \
                      "'{cluster_id}', '{tsne_1}', '{tsne_2}')".format(
                next=(", " if n != 2 else ""),
                dataset=reference_id,
                cell_marker=cell_marker,
                cluster_id=cluster_id,
                tsne_1=float(tsne_1),
                tsne_2=float(tsne_2)
            )

        DB.connection.execute("INSERT INTO cell (dataset, cell_marker, cluster_id, tsne_1, tsne_2)"
                              " VALUES {values}".format(values=values))
    DB.connection.close()


if __name__ == '__main__':
    try:
        arg = sys.argv
        db_name = arg[1]
        db_host = arg[2]
        db_username = arg[3]
        db_password = arg[4]
        file_cells = arg[5]
        reference_file = arg[6]
        output = arg[7]

        reference_id = open(reference_file).read().replace("\n", "")
        insert_cells_to_db('mysql', 'pymysql', db_host, db_username, db_password, db_name, file_cells, reference_id)
        with open(output, 'w') as f:
            f.write("all records are inserted to the db")
    except Exception as a:
        print(a)
