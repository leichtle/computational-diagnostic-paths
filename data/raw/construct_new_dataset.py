import pandas as pd

import argparse
import logging

from src.common.json_logging import setup_logging

setup_logging("src/common/logging.json")  # setup logger
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    # configure parser and parse arguments
    parser = argparse.ArgumentParser(description='Prepare dataset for bayesian variable selection.')
    parser.add_argument('--case_lab_dataset', type=str, help='The path to the lab values per case dataset file pulled from the db using pull_new_dataset.py', required=True)
    parser.add_argument('--case_diagnosis_dataset', type=str, help='The path to the diagnoses per case dataset file pulled from the db using pull_new_dataset.py', required=True)
    parser.add_argument('--chunksize', type=int, default=100000, help='The chunk size to process in order to not overload the memory')

    args = parser.parse_args()
    case_lab_data_file = args.case_lab_dataset
    case_diagnosis_data_file = args.case_diagnosis_dataset
    chunk_size = args.chunksize

    # read lab values of cases and pivot them into a values per case form
    lab_data_df = None
    rows_processed = 0
    next_rows_threshold = 0

    for chunk in pd.read_csv(case_lab_data_file, chunksize=chunk_size, delimiter=';', encoding='Latin-1'):  # Time: O(chunk_qty * chunksize), Size: O(1)
        lab_values_per_case = chunk.pivot_table("WERT", ["CASEPSEUDOID"], "ANALYSE") # pivot into values per case form
        #TODO: Check how many different measuring units are used across different columns (There mostly one, rarely two, considered noise)

        if lab_data_df is None:                                             # if this is the first pivotation chunk, keep it as is
            lab_data_df = lab_values_per_case
        else:                                                               # else, combine the former table with the new chunk
            lab_data_df = lab_data_df.combine_first(lab_values_per_case)

        rows_processed += chunk_size

        # log progress periodically
        if rows_processed > next_rows_threshold:
            logger.info(str(next_rows_threshold) + "lab value rows processed.")
            next_rows_threshold += chunk_size

    case_diagnosis_df = None
    rows_processed = 0
    next_rows_threshold = 0
    # read diagnoses of cases
    for chunk in pd.read_csv(case_diagnosis_data_file, chunksize=chunk_size, delimiter=';'):  # Time: O(chunk_qty * chunksize), Size: O(1)
        diagnosis_list_df = chunk.groupby("CASEPSEUDOID")["DKEY1"].apply(list).to_frame()

        # merge new diagnoses with old ones
        if case_diagnosis_df is None:
            case_diagnosis_df = diagnosis_list_df
        else:
            case_diagnosis_df = pd.merge(case_diagnosis_df, diagnosis_list_df, on='CASEPSEUDOID', sort=False, how='outer')

            # fill Nan with empty lists
            case_diagnosis_df["DKEY1_x"] = case_diagnosis_df["DKEY1_x"].apply(lambda d: d if isinstance(d, list) else [])
            case_diagnosis_df["DKEY1_y"] = case_diagnosis_df["DKEY1_y"].apply(lambda d: d if isinstance(d, list) else [])

            case_diagnosis_df['DKEY1'] = case_diagnosis_df['DKEY1_x'] + case_diagnosis_df['DKEY1_y']    # combine
            case_diagnosis_df = case_diagnosis_df.drop(['DKEY1_x', 'DKEY1_y'], axis=1)

    rows_processed += chunk_size

    # log progress periodically
    if rows_processed > next_rows_threshold:
        logger.info(str(next_rows_threshold) + " diagnosis rows processed.")
        next_rows_threshold += chunk_size

    # join panda dfs
    case_lab_diagnosis_df = lab_data_df.join(case_diagnosis_df, on="CASEPSEUDOID", how='inner')
    case_lab_diagnosis_df.to_csv('20181218_case_lab_diagnosis_data.csv')



