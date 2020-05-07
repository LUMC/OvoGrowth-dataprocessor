from helpers.Database import db
import sys

arg = sys.argv
DB = db('mysql', 'pymysql', arg[1], arg[2], arg[3])
name = 'KeyGenes_PL'
DB.add_db(name)
with open(arg[4], "w") as out:
    out.write(name)