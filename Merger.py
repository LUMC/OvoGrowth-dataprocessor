import pandas as pd
import mygene
import sys

mg = mygene.MyGeneInfo()


class GeneAliasRetriever:
    @staticmethod
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



class DataFormater:

    def __init__(self, raw_file, cpm_file, sex_file, data_groups):
        self.raw_file = raw_file
        self.cpm_file = cpm_file
        self.sex_file = sex_file
        self.data_groups = data_groups
        self.genesIDs = []



    def get_gene_refs(self):
        unique_ids = list(set(self.genesIDs))
        ngnenes = len(unique_ids)
        n=0
        with open('gene_ref_data.txt', 'w') as gene_file:
            for gene_index in range(0, len(unique_ids)):
                n+=1
                print('Gene ID {current}/{total}'.format(current=n, total=ngnenes))
                gene_file.write(';'.join(GeneAliasRetriever.get_alias(unique_ids[gene_index]))+"\n")
        gene_file.close()

    def get_sex(self):
        pass

    def format_transcription_data(self):
        df_raw = pd.read_table(self.raw_file, index_col=0).astype(float)
        df_cpm = pd.read_table(self.cpm_file, index_col=0).astype(float)
        column_names = df_cpm.columns
        row_file=0
        row = 0
        line_n = len(df_cpm)
        with open('transcription_data.txt', 'w') as file:
            for gene_index, counts in df_cpm.iterrows():
                row_file+=1
                print('Formatting line {n}/{total}'.format(n=row_file, total=line_n))
                self.genesIDs.append(gene_index)
                raw_counts = df_raw.loc[gene_index]
                for column_index in range(0, len(column_names)):
                    row+=1
                    name_items = column_names[column_index].split("_")
                    sample_name = name_items[0]
                    phase = name_items[1].split(".")[0]
                    data_group = self.get_phase(phase)
                    file.write(';'.join([gene_index, sample_name, data_group,
                                         str(counts[column_index]), str(raw_counts[column_index])])+'\n')
        file.close()

    def get_phase(self, tissue_ref):

        for index, item in self.data_groups.items():
            if tissue_ref in item:
                return index
        raise SystemError


if __name__ == '__main__':
    raw_file = 'input/training_fetal.txt'
    cpm_file = 'output/cpm/training_fetal.tsv'
    sex_file = 'output/sex/training_fetal.tsv'
    data_groups = {
        'adult': ['adult'],
        '9-weeks': ['9'],
        '16:18-weeks': ['16', '18'],
        '22-weeks': ['22'],
    }
    data_formater = DataFormater(raw_file, cpm_file, sex_file, data_groups)
    data_formater.format_transcription_data()

