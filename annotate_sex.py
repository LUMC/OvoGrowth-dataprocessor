import pandas as pd
import numpy as np
import sys


def annotate_sex(dataset, outputfile):
    ds = pd.read_table(dataset, index_col=0).astype(float)
    xist_gene_expression = ds.loc['ENSG00000229807'].values.tolist()
    rps4y1_gene_expression = ds.loc['ENSG00000129824'].values.tolist()
    diff = np.array(xist_gene_expression) - np.array(rps4y1_gene_expression)
    with open(outputfile, 'w') as f:
        for i in range(len(ds.columns)):
            sex = 'F' if diff[i] > 0 else 'M'
            f.write('{sex}\t{sample}\n'.format(sex=sex, sample=ds.columns[i]))


annotate_sex(sys.argv[1], sys.argv[2])