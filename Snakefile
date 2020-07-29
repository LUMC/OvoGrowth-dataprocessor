from os import path
import random
import string
from scripts.helpers.Database import db

# Config section
dataset_names = config['dataset_names']
append_datasets = config['append_datasets']

output_dir = config['output_dir']
db_host = config['DB_HOST']
db_name = config['DB_NAME']
db_username = config['DB_USERNAME']
db_password = config['DB_PASSWORD']


def validate_input(files_dataset, required_files, output, logfile):
    failed = False
    log = ""
    for file_set in files_dataset:
        for rfile in required_files:
            if (not path.exists("input/"+ file_set + "/" + rfile)):
                failed = True
                log += file_set + "/" + rfile + " is required but missing\n"
    if not failed:
        open(str(output), 'w').write("correct")
    else:
        open(str(logfile), 'w').write("Error:\n" + str(log))

rule all:
    input:
         expand("{output_dir}/database/{dataset}/inserted_expression.txt",
                output_dir=output_dir, dataset=dataset_names)
# Rule section
rule validate_input:
    log:
       "{output_dir}/logs/validate_input.txt"
    output:
          "{output_dir}/validate_input.txt"
    params:
          files_dataset=dataset_names,
          required_files=["count_matrix.tsv", "genes.tsv", "cell_cluster.tsv"]
    threads: 8
    run:
        validate_input(params.files_dataset, params.required_files, output, log)


rule init_db_schema:
    input:
         name="{output_dir}/validate_input.txt",
         schema="files/schema.sql"
    params:
          append_datasets=append_datasets
    output:
          "{output_dir}/database/schema.txt"
    log:
        "{output_dir}/logs/init_db_schema.txt"
    threads: 8
    run:
        if int(params.append_datasets) == 0:
            shell("""bash scripts/init_db_schema.sh {db_username} {db_password}"""
                  """ {db_name} {input.schema} {output}"""
                  """ &> {log}""")
        else:
            shell("echo 'not applicable'  > {output} &> {log}")

rule prepare_dataset:
    input:
        schema="{output_dir}/database/schema.txt"
    output:
        "{output_dir}/database/{dataset}/id.txt"
    log:
        "{output_dir}/logs/{dataset}/prepare_dataset.txt"
    threads: 8
    shell:
        """python3 scripts/insert_dataset_to_database.py"""
        """ {db_name} {db_host} {db_username} {db_password} {wildcards.dataset}"""
        """ {output} """
        """ &> {log}"""

rule insert_genes:
    input:
         schema="{output_dir}/database/schema.txt",
         genes="input/{dataset}/genes.tsv",
    output:
         db="{output_dir}/database/{dataset}/inserted_genes.txt"
    log:
        "{output_dir}/logs/{dataset}/inserted_genes.txt"
    threads: 1
    shell:
        """python3 scripts/insert_genes_to_database.py"""
        """ {db_name} {db_host} {db_username} {db_password} {input.genes}"""
        """ {output.db} """
        """ &> {log}"""

rule insert_cells:
    input:
         reference_file="{output_dir}/database/{dataset}/id.txt",
         schema="{output_dir}/database/schema.txt",
         cells="input/{dataset}/cell_cluster.tsv",
    output:
         db="{output_dir}/database/{dataset}/inserted_cells.txt"
    log:
        "{output_dir}/logs/{dataset}/inserted_cells.txt"
    threads: 8
    shell:
        """python3 scripts/insert_cells_to_database.py"""
        """ {db_name} {db_host} {db_username} {db_password} {input.cells} {input.reference_file}"""
        """ {output.db} """
        """ &> {log}"""

rule insert_expression:
    input:
         reference_file="{output_dir}/database/{dataset}/id.txt",
         schema="{output_dir}/database/schema.txt",
         cell_db="{output_dir}/database/{dataset}/inserted_cells.txt",
         gene_db="{output_dir}/database/{dataset}/inserted_genes.txt",
         expression="input/{dataset}/count_matrix.tsv",
    output:
         db="{output_dir}/database/{dataset}/inserted_expression.txt"
    log:
        "{output_dir}/logs/{dataset}/inserted_expression.txt"
    threads: 8
    shell:
        """python3 scripts/insert_expression_to_database.py"""
        """ {db_name} {db_host} {db_username} {db_password} {input.expression} {input.reference_file}"""
        """ {output.db} """
        """ &> {log}"""
