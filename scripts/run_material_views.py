import time, sys
from helpers.Database import db

class Seeder(db):

    def __init__(self, dialect, driver, host, username, password, database):
        super(Seeder, self).__init__(dialect, driver, host, username, password)
        self.database = database

    def insert_gene_ref(self, file_genes):
        num_lines = sum(1 for line in open(file_genes))
        self.connect_to_db(self.database)
        self.connection.execute('DELETE FROM gene;')
        row = 1
        with open(file_genes) as f:
            for line in f:
                line = line.replace('\n', '').replace('\r', '')
                items = line.split(';')
                try:
                    if len(items) < 3:
                        self.connection.execute("INSERT INTO gene (ensg) VALUES ('{ensg}')".format(
                            ensg=items[0]
                        ))
                    else:
                        self.connection.execute("INSERT INTO gene (ensg, symbol, description) VALUES (%s, %s, %s)",
                                                [items[0], items[2], items[1]]
                        )
                    print("Inserted gene: {gene} | {line}/{lines}".format(
                        gene=items[0],
                        line=row,
                        lines=num_lines
                    ))
                    row += 1
                except:
                    print('!!! Error adding: {}'.format(items[0]))
                    time.sleep(5)
        print('--- All genes inserted! ---')
        self.connection.close()

    def insert_group_ref(self, file_groups, output):
        num_lines = sum(1 for line in open(file_groups))
        self.connect_to_db(self.database)
        self.connection.execute('DELETE FROM stage;')
        row = 1
        with open(file_groups) as f:
            for line in f:
                line = line.replace('\n', '').replace('\r', '')
                self.connection.execute("INSERT INTO stage (name) VALUES ('{name}')".format(
                    name=line
                ))
                print("Inserted group: {name} | {line}/{lines}".format(
                    name=line,
                    line=row,
                    lines=num_lines
                ))
                row += 1
        result = self.connection.execute("SELECT * FROM stage").fetchall()
        with open(output, 'w') as f:
            for item in result:
                f.write(",".join(str(column) for column in item)+"\n")
        print('--- All groups inserted! ---')
        self.connection.close()

    def insert_tissue_ref(self, file_tissues, output):
        num_lines = sum(1 for line in open(file_tissues))
        self.connect_to_db(self.database)
        self.connection.execute('DELETE FROM tissue;')
        row = 1
        with open(file_tissues) as f:
            for line in f:
                line = line.replace('\n', '').replace('\r', '')
                self.connection.execute("INSERT INTO tissue (name) VALUES ('{name}')".format(
                    name=line
                ))
                print("Inserted tissue: {name} | {line}/{lines}".format(
                    name=line,
                    line=row,
                    lines=num_lines
                ))
                row += 1
        result = self.connection.execute("SELECT * FROM tissue").fetchall()
        with open(output, 'w') as f:
            for item in result:
                f.write(",".join(str(column) for column in item)+"\n")
        print('--- All tissues inserted! ---')
        self.connection.close()

    def prepare_data(self, stage_file, tissue_file):
        stages = {}
        tissues = {}
        with open(stage_file) as f:
            for line in f:
                line = line.replace('\n', '').replace('\r', '')
                line = line.split(',')
                stages[line[4]] = line[0]
        f.close()
        with open(tissue_file) as f:
            for line in f:
                line = line.replace('\n', '').replace('\r', '')
                line = line.split(',')
                tissues[line[4]] = line[0]
        f.close()
        return stages, tissues

    def insert_expression(self, file_expressions, stage_file, tissue_file):
        row = 1
        print('Preparing....')
        num_lines = sum(1 for line in open(file_expressions))
        stages, tissues = self.prepare_data(stage_file,tissue_file )
        self.connect_to_db(self.database)
        self.connection.execute('DELETE FROM transcript;')
        with open(file_expressions) as f:
            for line in f:
                line = line.replace('\n', '').replace('\r', '')
                items = line.split(';')
                result = self.connection.execute("SELECT id FROM gene WHERE ensg = '{gname}'".format(gname=items[0]))
                try:
                    self.connection.execute("INSERT INTO transcript (gene, stage, tissue, count, sex, CPM ) VALUES "
                                            "('{gene}', '{stage}', '{tissue}', '{count}', '{sex}', '{CPM}')".format(
                                                gene=[item[0] for item in result][0],
                                                stage=stages[items[2]], tissue=tissues[items[1]],
                                                count=items[4], CPM=items[3], sex=items[5]
                    ))
                    print("Inserted gene count: {gene} | {line}/{lines}".format(
                        gene=items[0],
                        line=row,
                        lines=num_lines
                    ))
                    row += 1
                except Exception as e:
                    print('!!! Error adding count: {}'.format(items[0]))
                    print(e)
        print('--- All counts inserted! ---')
        self.connection.close()


if __name__ == '__main__':

    try:
        arg = sys.argv
        db_name_file = arg[1]
        db_host = arg[2]
        db_username = arg[3]
        db_password = arg[4]
        file_genes = arg[5]
        file_tissues = arg[6]
        file_groups = arg[7]
        file_expressions = arg[8]
        output_inserted = arg[9]
        output_stage = arg[10]
        output_tissue = arg[11]

        print(open(file_tissues).read())
        db_name = open(db_name_file).read().replace("\n", "")
        seeder = Seeder('mysql', 'pymysql', db_host, db_username, db_password, db_name)
        seeder.insert_gene_ref(file_genes)
        seeder.insert_group_ref(file_groups, output_stage)
        seeder.insert_tissue_ref(file_tissues, output_tissue)
        seeder.insert_expression(file_expressions, output_stage, output_tissue)

        with open(output_inserted, 'w') as f:
            f.write("all records are inserted to the db")
    except Exception as a:
        print(a)

