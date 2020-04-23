from Database import db
import random
import string

# Config section
input_files = config['input']
input_file_names = [file_name.split('.')[0] for file_name in input_files]
output_dir = config['output_dir']
db_host = config['DB_HOST']
db_username = config['DB_USERNAME']
db_password = config['DB_PASSWORD']


def random_string(string_length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


# Rule section
rule all:
    input:
         expand("{output_dir}/sex/{file_name}.tsv",
                    output_dir=output_dir,
                    file_name=input_file_names,
                )

rule create_CPM:
    input:
         "input/{file_name}.txt"
    output:
         "{output_dir}/cpm/{file_name}.tsv"
    message: "Creating CPM table for {wildcards.file_name}"
    log: "{output_dir}/logs/{file_name}_CPM.log"
    shell: "Rscript create_CPM.R "
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
    shell: "python3 annotate_sex.py "
            "{input} "
            "{output} "
            "&> {log}"

# rule create_database:
#     output: "{output_dir}/db_name.txt".format(output_dir=config['output_dir'])
#     message: "Creating the working database"
#     run:
#         DB = db('mysql', 'pymysql', config['DB_HOST'], config['DB_USERNAME'], config['DB_PASSWORD'])
#         name='KeyGenes_tmp_{}'.format(random_string(5))
#         DB.add_db(name)
#         config['DB_name'] = name
#         with open(output[0], "w") as out:
#             out.write(name)
