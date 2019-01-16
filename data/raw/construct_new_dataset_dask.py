import dask.dataframe as dd
from dask.diagnostics import ProgressBar

if __name__ == "__main__":

    rows_processed = 0
    next_rows_threshold = 0

    # chunk_size = 100000
    # read lab values of cases
    lab_data_df = dd.read_csv("20181218_case_lab_data.csv", delimiter=';', encoding='Latin-1')  # Time: O(chunk_qty * chunksize), Size: O(1)

    with ProgressBar():
        lab_data_df = lab_data_df.categorize(columns=['ANALYSE'])

    with ProgressBar():
        lab_data_df = lab_data_df.pivot_table(values="WERT", index="CASEPSEUDOID", columns="ANALYSE")

    with ProgressBar():
        lab_data_df = lab_data_df.compute()

    # read diagnoses of cases
    case_diagnosis_df = dd.read_csv("20181218_case_diagnosis_data.csv", delimiter=';')  # Time: O(chunk_qty * chunksize), Size: O(1)

    with ProgressBar():
        case_diagnosis_df = case_diagnosis_df.groupby("CASEPSEUDOID")["DKEY"].apply(list)

    # join panda dfs
    with ProgressBar():
        case_lab_diagnosis_df = lab_data_df.join(case_diagnosis_df, on="CASEPSEUDOID", how='inner')

    case_lab_diagnosis_df.to_csv('20181218_case_lab_diagnosis_data_*.csv')



