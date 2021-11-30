# How to run this code

Requirements for the dataset:
* the data should be without missigness, which can be solved through data imputation
* the label must be encoded in a separate column

experiment.r --dataset ./data/processed/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mi_nIter_150_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_3_label.csv --label diagnostic_outcome --niter 10000000 --burnIn 2000000 --lambda 1