import pandas as pd
import sys

data_groups = {
    'adult': ['adult'],
    '9-weeks': ['9'],
    '16:18-weeks': ['16', '18'],
    '22-weeks': ['22'],
}


def get_phase(tissue_ref):
    for index, item in data_groups.items():
        if tissue_ref in item:
            return index
    raise SystemError


def format_transcription_data(raw_file, cpm_file, sex_file, out_transcription):
    df_raw = pd.read_table(raw_file, index_col=0).astype(float)
    df_cpm = pd.read_table(cpm_file, index_col=0).astype(float)
    column_names = df_cpm.columns
    row_file = 0
    row = 0
    line_n = len(df_cpm)
    sex_name = []
    sex = []
    with open(sex_file) as sex_file:
        for line in sex_file:
            line = line.replace('\n', '').split('\t')
            sex_name.append(line[1])
            sex.append(line[0])
    print(sex_name)
    with open(out_transcription, 'w') as file:
        for gene_index, counts in df_cpm.iterrows():
            row_file += 1
            print('Formatting line {n}/{total}'.format(n=row_file, total=line_n))
            raw_counts = df_raw.loc[gene_index]
            for column_index in range(0, len(column_names)):
                row += 1
                name_item = column_names[column_index]
                sex_index = sex_name.index(name_item)
                name_items = column_names[column_index].split("_")
                sample_name = name_items[0]
                phase = name_items[1].split(".")[0]
                data_group = get_phase(phase)
                file.write(';'.join([gene_index, sample_name, data_group,
                                     str(counts[column_index]), str(round(raw_counts[column_index], 3)), sex[sex_index]]) + '\n')


format_transcription_data(
    sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
)


