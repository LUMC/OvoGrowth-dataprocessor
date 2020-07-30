import sys
import mygene

mg = mygene.MyGeneInfo()


def get_alias(symbol):
    result = mg.query(symbol, fields="name,symbol")
    try:
        return result['hits'][0]['name']
    except:
        return "NA"


def get_gene_information(input, output):
    with open(output, 'w') as f:
        for line in open(input):
            gene_items = line.replace('\n', '').replace('"', '').split('\t')
            gene_description = get_alias(gene_items[1])
            gene_info = [gene_items[0], gene_items[1], gene_description]
            f.write(";".join(gene_info)+"\n")


get_gene_information(sys.argv[1], sys.argv[2])