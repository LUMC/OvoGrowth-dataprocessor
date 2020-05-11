import sys
import sqlalchemy
from helpers.Database import db


class MaterialViews(db):

    def __init__(self, file_db_name, host, username, password):
        name = open(file_db_name).read().replace("\n", "")
        super(MaterialViews, self).__init__('mysql', 'pymysql', host, username, password)
        self.database = name
        self.connect_to_db(self.database)

    def get_mv_group_settings(self, tag, adult_id):
        adult_id = str(adult_id)
        if tag == 'adult':
            return "AND t.stage = "+adult_id, 1
        if tag == 'fetal':
            return "AND t.stage != "+adult_id, 0
        if tag == 'all':
            return '', 'NULL'

    def run_mv_transcript(self, file_output):
        self.connection.execute("DELETE FROM transcript_mv")
        result = self.connection.execute("SELECT id FROM tissue")
        tissues = [item for item in result]
        result = self.connection.execute("SELECT id FROM stage where name = 'adult'")
        adult_id = [item[0] for item in result][0]
        groups = ["adult", "fetal", "all"]
        for group in groups:
            print(group, "---")
            q_addition, req = self.get_mv_group_settings(group, adult_id)
            for tissue in tissues:
                print(tissue[0], "---")
                tissue_id = tissue[0]
                query = "SELECT  gene, tissue, avg(count), avg(CPM) from transcript as t "
                query += "LEFT JOIN gene as g on g.id = t.gene "
                query += "WHERE t.tissue = {tissue} ".format(tissue=tissue_id)
                query += "AND g.symbol IS NOT NULL "
                query += q_addition
                query += " GROUP BY g.id "
                query += "ORDER BY avg(t.CPM) DESC "
                query += "LIMIT 100 "
                print(query)
                result = self.connection.execute(query)
                print(len([item for item in result]))
                for item in result:
                    query = "INSERT INTO transcript_mv (gene, tissue, count_avg, CPM_avg, adult_only) "
                    query += "VALUES ({x[0]}, {x[1]}, {x[2]}, {x[3]}, {group})".format(x=list(item), group=req)
                    self.connection.execute(query)
        self.connection.close()
        with open(file_output, 'w') as f:
            f.write('created')


arg = sys.argv
mv = MaterialViews(arg[1], arg[2], arg[3], arg[4])
mv.run_mv_transcript(arg[5])