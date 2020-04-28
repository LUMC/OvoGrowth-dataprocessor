import os, time, sys
from helpers.Database import db

class Seeder(db):

    def __init__(self, dialect, driver, host, username, password, database, gene_ref_file, gene_expression_file):
        super(Seeder, self).__init__(dialect, driver, host, username, password)
        self.database = database
        self.gene_ref_file = gene_ref_file
        self.gene_expression_file = gene_expression_file

    def insert_gene_ref(self):
        print('Preparing....')
        num_lines = sum(1 for line in open(self.gene_ref_file))
        self.connect_to_db(self.database)
        self.connection.execute('DELETE FROM gene;')
        row = 1
        with open(self.gene_ref_file) as f:
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