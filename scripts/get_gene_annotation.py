import sys
import mygene

mg = mygene.MyGeneInfo()


def get_alias(ensg_id):
    result = mg.getgenes([ensg_id], fields="name,symbol")
    try:
        return [ensg_id, result[0]['name'], result[0]['symbol']]
    except:
        if len(result) > 2:
            print(result)
            return [ensg_id, '', result[0]['symbol']]
        else:
            return [ensg_id]


def get_gene_information(input, output):
    with open(output, 'w') as f:
        for line in open(input):
            gene_id = line.replace('\n', '')
            gene_info = get_alias(gene_id)
            print(gene_info)
            f.write(";".join(gene_info)+"\n")

get_gene_information(sys.argv[1], sys.argv[2])