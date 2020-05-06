# KeyGenes data processor

A Snakemake based workflow to fetch data from multiple batch-RNA 
datasets and submit it to a MySQL-database. 

## Requirements

The pipeline requires programs to installed: 
- MySQL (^8.0)
- Python (^3.5)
- R (^3.5)

## Installation

The workflow can be cloned from GitHub with the following command

```bash
git clone https://github.com/LUMC/KeyGenes-dataprocessor
```

The python-based requirement can be installed by using:
```shell script
pip3 install -r requirements.txt
```

Atlast, the R-based library **EdgeR** is required; [click](https://bioconductor.org/packages/release/bioc/html/edgeR.html) here for installation
instructions. 
## Instructions

The workflow strictly relies on the settings of a configuration file. All parameters all required. The DB
parameters refer to the MySQL user that can be used for interaction with the database.
All datasets that are wished to be included in the execution of the pipeline, need to be placed in the input folder.
The output folder will contain all the pipeline results. 

The config file is typically a **yaml (.yml)** file and is not restricted to a specific naming. 
```yaml
input:
  - training_adult.txt
  - training_fetal.txt
output_dir: output
DB_HOST: localhost
DB_USERNAME: user
DB_PASSWORD: password
```

##Execution
When everything is configured, the pipeline can be executing using the following
command:
```shell script
snakemake --configfile=<example.yml>
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
