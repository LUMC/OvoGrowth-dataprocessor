import random
import string
from scripts.helpers.Database import db

# Config section
input_file_genes = config['input_genes']
input_file_cluster = config['input_cluster']
input_file_counts = config['input_counts']
output_dir = config['output_dir']
db_host = config['DB_HOST']
db_username = config['DB_USERNAME']
db_password = config['DB_PASSWORD']



# Rule section
rule all:
    input:
         expand("{output_dir}/database/inserted_expression.txt", output_dir=output_dir),

rule create_database:
    output:
        "{output_dir}/database/name.txt"
    message:
        "Creating the working database"
    log:
        "{output_dir}/logs/create_db.txt"
    shell:
        """python3 scripts/create_db.py {db_host} {db_username} {db_password} {output} &> {log}"""

rule init_db_schema:
    input:
        name="{output_dir}/database/name.txt",
        schema="files/schema.sql"
    output:
        "{output_dir}/database/schema.txt"
    log:
        "{output_dir}/logs/init_db_schema.txt"
    shell:
        """bash scripts/init_db_schema.sh {db_username} {db_password} {input.name} {input.schema} {output} &> {log}"""

rule insert_genes:
    input:
         db="{output_dir}/database/name.txt",
         schema="{output_dir}/database/schema.txt",
         genes=input_file_genes,
    output:
         db="{output_dir}/database/inserted_genes.txt"
    log:
        "{output_dir}/logs/inserted_genes.txt"
    shell:
        """python3 scripts/insert_genes_to_database.py"""
        """ {input.db} {db_host} {db_username} {db_password} {input.genes}"""
        """ {output.db} """
        """ &> {log}"""

rule insert_cells:
    input:
         db="{output_dir}/database/name.txt",
         schema="{output_dir}/database/schema.txt",
         cells=input_file_cluster,
    output:
         db="{output_dir}/database/inserted_cells.txt"
    log:
        "{output_dir}/logs/inserted_cells.txt"
    shell:
        """python3 scripts/insert_cells_to_database.py"""
        """ {input.db} {db_host} {db_username} {db_password} {input.cells}"""
        """ {output.db} """
        """ &> {log}"""

rule insert_expression:
    input:
         db="{output_dir}/database/name.txt",
         schema="{output_dir}/database/schema.txt",
         gene_db="{output_dir}/database/inserted_genes.txt",
         cell_db="{output_dir}/database/inserted_cells.txt",
         cells=input_file_counts,
    output:
         db="{output_dir}/database/inserted_expression.txt"
    log:
        "{output_dir}/logs/inserted_expression.txt"
    shell:
        """python3 scripts/insert_expression_to_database.py"""
        """ {input.db} {db_host} {db_username} {db_password} {input.cells}"""
        """ {output.db} """
        """ &> {log}"""

