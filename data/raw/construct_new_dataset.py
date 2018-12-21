import idsc
from idsc.cdwh import common, queries
import pandas as pd
import numpy as np

if __name__ == "__main__":

    rows_processed = 0
    next_rows_threshold = 0

    lab_data_df = None
    chunk_size = 100000
    # read lab values of cases
    for chunk in pd.read_csv("20181218_case_lab_data.csv", chunksize=chunk_size, delimiter=';', encoding='Latin-1'):  # Time: O(chunk_qty * chunksize), Size: O(1)
        lab_values_per_case = chunk.pivot_table("WERT", ["CASEPSEUDOID"], "ANALYSE")
        #TODO: Check how many different measuring units are used across different columns

        if lab_data_df is None:
            lab_data_df = lab_values_per_case
        else:
            lab_data_df = lab_data_df.combine_first(lab_values_per_case)
        # for _, row in chunk.iterrows():
        #     case_id = row[0]  # get case id of row
        #
        #     # add case if not existing
        #     if case_id not in case_value_map:
        #         case_value_map[case_id] = {}
        #
        #     # get lab value id and the value itself
        #     lab_value = row[2]  # lab value
        #     lab_value_id = row[3]  # analysis type id
        #
        #     if lab_value is not np.nan and lab_value_id not in name_map:
        #         # CASEPSEUDOID;ANALYSE;WERT;EINHEIT;ERMITTLUNG;BEZ;KBZ;LOINC
        #         if row[6] is not np.nan:
        #             lab_value_name = row[6] + "/"  # short descriptor
        #         else:
        #             lab_value_name = ''
        #
        #         lab_value_name += row[5]  # long descriptor
        #         if row[7] is not np.nan:
        #             lab_value_name += " (" + str(row[7]) + ")"  # LOINC
        #         if row[3] is not np.nan:
        #             lab_value_name += " [" + str(row[3]) + "]"  # unit
        #
        #         name_map[lab_value_id] = lab_value_name
        #
        #     if lab_value is not np.nan:
        #         case_value_map[case_id][lab_value_id] = lab_value

        rows_processed += chunk_size
        if rows_processed > next_rows_threshold:
            print(str(next_rows_threshold) + " rows processed.")
            next_rows_threshold += chunk_size

    case_diagnosis_df = None
    # read diagnoses of cases
    for chunk in pd.read_csv("20181218_case_diagnosis_data.csv", chunksize=chunk_size, delimiter=';'):  # Time: O(chunk_qty * chunksize), Size: O(1)
        diagnosis_list_df = chunk.groupby("CASEPSEUDOID")["DKEY"].apply(list)

        # merge new diagnoses with old ones
        if case_diagnosis_df is None:
            case_diagnosis_df = diagnosis_list_df
        else:
            case_diagnosis_df = pd.merge(case_diagnosis_df, diagnosis_list_df, on='CASEPSEUDOID', sort=False, how='outer')
            case_diagnosis_df['DKEY'] = case_diagnosis_df['DKEY_x'] + case_diagnosis_df['DKEY_y']
            case_diagnosis_df = case_diagnosis_df.drop(['DKEY_x', 'DKEY_y'], axis=1)

    # join panda dfs
    case_lab_diagnosis_df = lab_data_df.join(case_diagnosis_df, on="CASEPSEUDOID", how='inner')
    case_lab_diagnosis_df.to_csv('20181218_case_lab_diagnosis_data.csv')



