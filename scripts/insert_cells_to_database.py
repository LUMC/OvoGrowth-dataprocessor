import time, sys
from helpers.Database import db


def insert_cells_to_db(dialect, driver, host, username, password, database, cells_file):
    DB = db(dialect, driver, host, username, password)
    DB.connect_to_db(database)
    n=0
    with open(cells_file) as f:
        for line in f:
            n += 1
            if n < 2:
                continue
            [cell_marker, cluster_id, tsne_1, tsne_2, sample_id] = line.replace('\n', '').split('\t')
            DB.connection.execute("INSERT INTO cell (cell_marker, cluster_id, tsne_1, tsne_2, sample_id)"
                                  "VALUES ('{cell_marker}', '{cluster_id}', '{tsne_1}', '{tsne_2}', '{sample_id}')"
                .format(
                cell_marker=cell_marker,
                cluster_id=cluster_id,
                tsne_1=tsne_1,
                tsne_2=tsne_2,
                sample_id=sample_id
            ))
    DB.connection.close()


if __name__ == '__main__':
    try:
        arg = sys.argv
        db_name_file = arg[1]
        db_host = arg[2]
        db_username = arg[3]
        db_password = arg[4]
        file_cells = arg[5]
        output = arg[6]
        db_name = open(db_name_file).read().replace("\n", "")
        insert_cells_to_db('mysql', 'pymysql', db_host, db_username, db_password, db_name, file_cells)
        with open(output, 'w') as f:
            f.write("all records are inserted to the db")
    except Exception as a:
        print(a)
