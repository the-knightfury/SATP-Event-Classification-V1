import pandas as pd
import path

if __name__ == "__main__":

    source_root = path.TAGTOG_PRE_ANNOTATION
    source_file = "TagTog_Data/sampled_9000_relevant_data.csv"
    source_path = source_root + source_file
    destination = path.TAGTOG_PRE_ANNOTATION + "TagTog_Data/"
    total_data = 9000
    file_prefix = 'news_satp_'

    data = pd.read_csv(source_path, header=[0])
    data.drop(columns=["Relevance"], inplace=True)


    chunk_size = int(data.shape[0] / 18)
    i = 10
    for start in range(0, data.shape[0], chunk_size):
        df_subset = data.iloc[start:start + chunk_size]
        df_subset.to_csv(destination + file_prefix + str(i) + '.tsv', index=False, header=True, sep='\t')
        i += 1
        print(df_subset.shape)
