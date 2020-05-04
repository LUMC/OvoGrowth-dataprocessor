import sys
import sqlalchemy
from helpers.Database import db


class MaterialViews(db):

    def __init__(self, file_db_name, host, username, password):
        name = open(file_db_name).read().replace("\n", "")
        super(MaterialViews, self).__init__('mysql', 'pymysql', host, username, password)
        self.database = name
        self.connect_to_db(self.database)

    def run_mv_transcript(self, file_output):
        self.connection.execute("DELETE FROM transcript_mv")
        result = self.connection.execute("SELECT id FROM tissue")
        tissues = [item for item in result]
        for tissue in tissues:
            tissue_id = tissue[0]
            query = "SELECT  gene, tissue, avg(count), avg(CPM) from transcript as t "
            query += "LEFT JOIN gene as g on g.id = t.gene "
            query += "WHERE t.tissue = {tissue} ".format(tissue=tissue_id)
            query += "AND g.symbol IS NOT NULL "
            query += "GROUP BY g.id "
            query += "ORDER BY avg(t.CPM) DESC "
            query += "LIMIT 100 "
            result = self.connection.execute(query)
            for item in result:
                query = "INSERT INTO transcript_mv (gene, tissue, count_avg, CPM_avg) "
                query += "VALUES ({x[0]}, {x[1]}, {x[2]}, {x[3]})".format(x=list(item))
                self.connection.execute(query)
        self.connection.close()
        with open(file_output, 'w') as f:
            f.write('created')


arg = sys.argv
mv = MaterialViews(arg[1], arg[2], arg[3], arg[4])
mv.run_mv_transcript(arg[5])