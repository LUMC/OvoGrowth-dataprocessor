import random
import string
from helpers.Database import db

# Config section
input_files = config['input']
input_file_names = [file_name.split('.')[0] for file_name in input_files]
output_dir = "../"+config['output_dir']
db_host = config['DB_HOST']
db_username = config['DB_USERNAME']
db_password = config['DB_PASSWORD']


def random_string(string_length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))
def gene_inputs(wildcards):
    files = expand("{output_dir}/expr/{file_name}_expression.tsv",output_dir=output_dir, file_name=input_file_names)
    return files

# Rule section
rule all:
    input:
         expand("{output_dir}/expr/{file_name}_expression.tsv", output_dir=output_dir, file_name=input_file_names),
         expand("{output_dir}/gene/info.tsv", output_dir=output_dir)

rule create_CPM:
    input:
         "input/{file_name}.txt"
    output:
         "{output_dir}/cpm/{file_name}.tsv"
    message: "Creating CPM table for {wildcards.file_name}"
    log: "{output_dir}/logs/{file_name}_CPM.log"
    shell: "Rscript scripts/create_CPM.R "
            "{input} "
            "{output} "
            "&> {log}"

rule annotate_sex:
    input:
         "{output_dir}/cpm/{file_name}.tsv"
    output:
         "{output_dir}/sex/{file_name}.tsv"
    message: "Annotating sex for {wildcards.file_name}"
    log: "{output_dir}/logs/{file_name}_sex.log"
    shell: "python3 scripts/annotate_sex.py "
            "{input} "
            "{output} "
            "&> {log}"

rule format_expression_data:
    input:
         raw="input/{file_name}.txt",
         cpm="{output_dir}/cpm/{file_name}.tsv",
         sex="{output_dir}/sex/{file_name}.tsv"
    output:
         expression="{output_dir}/expr/{file_name}_expression.tsv"
    message: "Formatting expresson data for {wildcards.file_name}"
    log: "{output_dir}/logs/{file_name}_format_expr.log"
    shell: "python3 scripts/format_expression_data.py "
            "{input.raw} "
            "{input.cpm} "
            "{input.sex} "
            "{output.expression} "
            "&> {log}"

rule merge_data:
    input:gene_inputs
    output:
         expression="{output_dir}/collections/expression.csv",
         genes="{output_dir}/collections/genes_names.csv",
         tissues="{output_dir}/collections/tissues.tsv",
         groups="{output_dir}/collections/groups.tsv",
    shell:
           """ cat {input} | awk -F ";" '{{print $1}}'| sort | uniq > {output.expression} && """
           """ cat {input} | awk -F ";" '{{print $1}}'| sort | uniq > {output.genes} && """
           """ cat {input} | awk -F ";" '{{print $2}}'| sort | uniq > {output.tissues} && """
           """ cat {input} | awk -F ";" '{{print $3}}'| sort | uniq > {output.groups}"""

rule get_gene_info:
    input:
        genes="{output_dir}/collections/genes_names.tsv"
    output:
        genes="{output_dir}/collections/genes.tsv"
    shell:
        "python3 scripts/get_gene_annotation.py {input.genes} {output.genes}"

rule create_database:
    output: "{output_dir}/database/name.txt"
    message: "Creating the working database"
    run:
        DB = db('mysql', 'pymysql', {db_host}, {db_username}, {db_password})
        name='KeyGenes_tmp_{}'.format(random_string(5))
        DB.add_db(name)
        with open(output[0], "w") as out:
            out.write(name)

rule insert_to_database:
    input:
         db="{output_dir}/database/name.txt",
         expressions="{output_dir}/collections/expression.csv",
         genes="{output_dir}/collections/genes_names.csv",
         tissues="{output_dir}/collections/tissues.tsv",
         groups="{output_dir}/collections/groups.tsv"
    output:
         db="{output_dir}/database/inserted.txt"