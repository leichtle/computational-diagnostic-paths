Computational Diagnostic Paths: Deriving efficient, evidence-based Diagnostic Paths from Past Diagnoses using Bayesian Model Averaging
------------

Diagnostic Paths constitute the basic guidelines of laboratory diagnostics in an ICD10-funded hospital environment.
Although they are designed to lead to diagnosis along the analytes of highest known significance thus avoiding unnecessary tests, they are based on agreements among experts and therefore reflect opinions, not scientific evidence.
In this project, we derive the importance of analytes from previously collected lab measurements and the resulting diagnoses using an algorithmic framework called Bayesian Model Averaging (BMA).
To overcome the sparsity of the feature matrix, the matrix is first completed with artificial measurements provided by multiple imputation.
Using BMA, the features are then included into regression models in a stepwise manner to determine how well the label can be predicted based on the set of features.
To avoid computing the 2^n model selectivities, the method samples the model space and drops out models with a low selectivity and a high number of included variables.
The result is a limited set of models with complementary selectivity, which allow calculating the marginal probability of an analyte, constituting its overall inclusion probability.
Under the assumption that a low inclusion probability expresses a low diagnostic value, the results could be used to drop unnecessary lab measurements and make diagnosis more efficient.

Our data consisted of 207874 patient cases from the years 2012 and 2019 29897 of them had a diagnosis within the ICD-range of myocardial ischemia,
leaving 177977 patient cases as a part of the control group. These patient cases allowed us to include 1929 laboratory analytes into our study. 
From the total of 1929 analyte values, 8 were missing in less than 20% of cases, 26 in less than 40% of cases, 59 in less than 60% of the cases, 110 in less than 80% of the cases.

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short ```-``` delimited description, e.g.
    │                         ```1.0-jqp-initial-data-exploration```.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with ```pip freeze > requirements.txt```
    ├── requirements.r    <- The requirements file for reproducing the analysis environment, e.g.
    │                         an r script to run in order to install dependencies
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── [add script descriptions]
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── [add script descriptions]
    │   │
    │   ├── models         <- Scripts to make predictions
    │   │   ├── [add script descriptions]
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── dataset.py          <- main script to download and generate data (Uses code from data folder)
    ├── feature.py          <- main script to turn raw data into features for modelling (Uses code from features folder)
    ├── experiment.py       <- main script to make predictions (Uses code from models folder)
    └── tox.ini             <- tox file with settings for running tox; see tox.testrun.org


The following measures lead to finding predictive analytes to diagnose Myocardial Ischemia (MI):
* Build a dataset of all lab data of all cases
* Filter the dataset to only contain cases where Troponin (TNT) was measured, since this is the current go-to analyte to detect MI. Then drop all columns that lack more than na_drop_threshold amount of data.
  * ```sbatch ./cluster/submit_dataset.sh "--dataset ./data/raw/20181218000000_case_lab_diagnosis_data.csv --diagnosis_indicator_column 638 --na_drop_threshold 0.8 --skip_imputation"```
  * ```sbatch ./cluster/submit_dataset.sh "--dataset ./data/raw/20181218000000_case_lab_diagnosis_data.csv --diagnosis_indicator_column 638 --na_drop_threshold 0.6 --skip_imputation"```
  * ```sbatch ./cluster/submit_dataset.sh "--dataset ./data/raw/20181218000000_case_lab_diagnosis_data.csv --diagnosis_indicator_column 638 --na_drop_threshold 0.4 --skip_imputation"```
  * ```sbatch ./cluster/submit_dataset.sh "--dataset ./data/raw/20181218000000_case_lab_diagnosis_data.csv --diagnosis_indicator_column 638 --na_drop_threshold 0.2 --skip_imputation"```
  * 638 = ng/L;Troponin-T-hs;TNThsn;67151-1 (https://r.details.loinc.org/LOINC/67151-1.html?sections=Comprehensive)
* This results in datasets of size:
  * 0.2: (29897, 8)
  * 0.4: (29897, 26)
  * 0.6: (29897, 59)
  * 0.8: (29897, 110)
* Based on this new dataset, perform imputation. examples:
  * mi:
    * ```sbatch ./cluster/submit_dataset_r.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2.csv --maxIterations 30 --imputationPackage mi --processingCoreQty 3 --chainQty 3 --untilConvergence TRUE --rHatsConvergence 1.1 --storeAllImputations TRUE"```
    * ```sbatch ./cluster/submit_dataset_r.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.4.csv --maxIterations 30 --imputationPackage mi --processingCoreQty 3 --chainQty 3 --untilConvergence TRUE --rHatsConvergence 1.1 --storeAllImputations TRUE"```
  
  * mice:
    * ```sbatch ./cluster/submit_dataset_r.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2.csv --imputationPackage mice --imputationMethod cart --maxIterations 80 --processingCoreQty 3 --chainQty 1 --clusterSeed 7 --storeAllImputations TRUE"```
  
* Assuming the imputation does not diverge, build diagnostic output feature:

  * Missingness < 0.2 dataset (mice):
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mice_nIter_80_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_1.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mice_nIter_80_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_2.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mice_nIter_80_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_3.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```

    * Missingness < 0.4 dataset (mice):
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.4_impType_mice_nIter_800_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_1.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.4_impType_mice_nIter_800_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_2.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.4_impType_mice_nIter_800_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_3.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
  
  * Missingness < 0.2 dataset (mi):
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mi_nIter_90_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_1.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mi_nIter_90_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_2.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mi_nIter_90_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_3.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
  
  * Missingness < 0.4 dataset (mi):
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.4_impType_mi_nIter_150_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_1.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.4_impType_mi_nIter_150_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_2.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.4_impType_mi_nIter_150_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_3.csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```

* perform ODA/BMA, then calculate confidence intervals:

  * Missingness < 0.2 dataset (mice):
  * ```sbatch ./cluster/submit_experiment_r.sh "--dataset ./data/processed/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mice_nIter_80_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_1_label.csv --label diagnostic_outcome --niter 1000000 --burnIn 200000 --lambda 1"```
  * ```sbatch ./cluster/submit_experiment_r.sh "--dataset ./data/processed/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mice_nIter_80_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_2_label.csv --label diagnostic_outcome --niter 1000000 --burnIn 200000 --lambda 1"```
  * ```sbatch ./cluster/submit_experiment_r.sh "--dataset ./data/processed/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mice_nIter_80_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_3_label.csv --label diagnostic_outcome --niter 1000000 --burnIn 200000 --lambda 1"```
  
  * Missingness < 0.2 dataset (mi):
  * ```sbatch ./cluster/submit_experiment_r.sh "--dataset ./data/processed/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mi_nIter_150_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_1_label.csv --label diagnostic_outcome --niter 10000000 --burnIn 2000000 --lambda 1"```
  * ```sbatch ./cluster/submit_experiment_r.sh "--dataset ./data/processed/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mi_nIter_150_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_2_label.csv --label diagnostic_outcome --niter 10000000 --burnIn 2000000 --lambda 1"```
  * ```sbatch ./cluster/submit_experiment_r.sh "--dataset ./data/processed/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.2_impType_mi_nIter_150_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_3_label.csv --label diagnostic_outcome --niter 10000000 --burnIn 2000000 --lambda 1"```
  
  * Missingness < 0.4 dataset (mi):
  * ```sbatch ./cluster/submit_experiment_r.sh "--dataset ./data/processed/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.4_impType_mi_nIter_150_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_1_label.csv --label diagnostic_outcome --niter 10000000 --burnIn 2000000 --lambda 1"```
  * ```sbatch ./cluster/submit_experiment_r.sh "--dataset ./data/processed/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.4_impType_mi_nIter_150_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_2_label.csv --label diagnostic_outcome --niter 10000000 --burnIn 2000000 --lambda 1"```
  * ```sbatch ./cluster/submit_experiment_r.sh "--dataset ./data/processed/20181218000000_case_lab_diagnosis_data_indicatorColumns_['638']_naDropThreshold_0.4_impType_mi_nIter_150_chainQty_3_rHatsConvergence_1.1_normImputation_FALSE_3_label.csv --label diagnostic_outcome --niter 10000000 --burnIn 2000000 --lambda 1"```

* Finally, we produce a bootstrapped result:
  * Bootstrap (0.4)
  *  ```bootstrap.py --dataset "./data/processed/bootstraps/0.4/1.csv" --dataset "./data/processed/bootstraps/0.4/2.csv" --dataset "./data/processed/bootstraps/0.4/3.csv" --save-path "./data/processed/bootstraps/0.4/inclusion_probabilities.png"```

### Alternative Approach
* Build a dataset of all lab data of all cases
* Filter the dataset to only contain cases where Troponin (TNT) was measured, since this is the current go-to analyte to detect MI. Then drop all columns that contain no data.
  * ```sbatch ./cluster/submit_dataset.sh "--dataset ./data/raw/20181218000000_case_lab_diagnosis_data.csv --diagnosis_indicator_column 638 --na_drop_threshold 1.0 --skip_imputation"```
* Based on this new dataset, build diagnostic output feature
  * ```sbatch ./cluster/submit_feature.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_naDropThreshold_1.0_indicatorColumns_['638'].csv --diagnosis_col_name DKEY1 --diagnosis_code_min 200 --diagnosis_code_max 259"```
* Assess feature importance using xgboost
  * ```sbatch ./cluster/submit_experiment.sh "--dataset ./data/interim/20181218000000_case_lab_diagnosis_data_naDropThreshold_1.0_indicatorColumns_['638']_label.csv --importance_method xgb"```

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
