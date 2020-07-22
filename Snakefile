from os import path
import random
import string
from scripts.helpers.Database import db

# Config section
files_dataset = config['files_dataset']
append_datasets = config['append_datasets']

output_dir = config['output_dir']
db_host = config['DB_HOST']
db_username = config['DB_USERNAME']
db_password = config['DB_PASSWORD']

def validate_input(files_dataset, required_files, output, logfile):
    failed=False
    log=""
    if not failed:
        for file_set in files_dataset:
            for rfile in required_files:
                if (not path.exists(file_set+"/"+rfile)):
                    failed=True
                    log+=file_set+"/"+rfile+ " is required but missing\n"
    open(str(logfile), 'w').write("Error:\n"+str(log))
    if not failed:
        open(output, 'w').write("correct")
        return True
    return False

rule all:
    input:
         expand("{output_dir}/validate_input.txt", output_dir=output_dir),
         expand("{output_dir}/validate_input.txt", output_dir=output_dir),

rule validate_input:
    log:
        "{output_dir}/logs/validate_input.txt"
    output:
        "{output_dir}/validate_input.txt"
    params:
        files_dataset=files_dataset,
        required_files=["count_matrix.tsv", "gene.tsv", "cell_cluster.tsv"]
    run:
        validate_input(params.files_dataset, params.required_files, output, log)

# Rule section


rule init_db_schema:
    input:
        name="{output_dir}/validate_input.txt",
        schema="files/schema.sql"
    params:
    output:
        "{output_dir}/database/schema.txt"
    log:
        "{output_dir}/logs/init_db_schema.txt"
    shell:
        """bash scripts/init_db_schema.sh {db_username} {db_password} {input.name} {input.schema} {output} &> {log}"""

# rule insert_genes:
#     input:
#          db="{output_dir}/database/name.txt",
#          schema="{output_dir}/database/schema.txt",
#          genes=input_file_genes,
#     output:
#          db="{output_dir}/database/inserted_genes.txt"
#     log:
#         "{output_dir}/logs/inserted_genes.txt"
#     shell:
#         """python3 scripts/insert_genes_to_database.py"""
#         """ {input.db} {db_host} {db_username} {db_password} {input.genes}"""
#         """ {output.db} """
#         """ &> {log}"""
#
# rule insert_cells:
#     input:
#          db="{output_dir}/database/name.txt",
#          schema="{output_dir}/database/schema.txt",
#          cells=input_file_cluster,
#     output:
#          db="{output_dir}/database/inserted_cells.txt"
#     log:
#         "{output_dir}/logs/inserted_cells.txt"
#     shell:
#         """python3 scripts/insert_cells_to_database.py"""
#         """ {input.db} {db_host} {db_username} {db_password} {input.cells}"""
#         """ {output.db} """
#         """ &> {log}"""
#
# rule insert_expression:
#     input:
#          db="{output_dir}/database/name.txt",
#          schema="{output_dir}/database/schema.txt",
#          gene_db="{output_dir}/database/inserted_genes.txt",
#          cell_db="{output_dir}/database/inserted_cells.txt",
#          cells=input_file_counts,
#     output:
#          db="{output_dir}/database/inserted_expression.txt"
#     log:
#         "{output_dir}/logs/inserted_expression.txt"
#     shell:
#         """python3 scripts/insert_expression_to_database.py"""
#         """ {input.db} {db_host} {db_username} {db_password} {input.cells}"""
#         """ {output.db} """
#         """ &> {log}"""

