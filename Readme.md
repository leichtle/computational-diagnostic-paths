Computational Diagnostic Paths: Deriving efficient, evidence-based Diagnostic Paths from Past Diagnoses using Bayesian Model Averaging
==============================

Diagnostic Paths constitute the basic guidelines of laboratory diagnostics in an ICD10-funded hospital environment. Although they are designed to lead to diagnosis along the analytes of highest known significance thus avoiding unnecessary tests, they are based on agreements among experts and therefore reflect opinions, not scientific evidence. In this project, we derive the importance of analytes from previously collected lab measurements and the resulting diagnoses using an algorithmic framework called Bayesian Model Averaging (BMA). To overcome the sparsity of the feature matrix, the matrix is first completed with artificial measurements provided by multiple imputation. BMA identifies highly predictive combinations of analytes by iteratively building regression model from the features to determine how well the label can be predicted. To avoid computing the selectivities of 2^n models, the method samples the model space and drops out models with a low selectivity and a high number of included variables. The result is a limited set of models with complementary selectivity, which allow calculating the marginal probability of an analyte, constituting its overall inclusion probability. Under the assumption that a low inclusion probability expresses a lowdiagnostic value, the results could be used to drop unnecessary lab measurements and make diagnosis more efficient.

## Current State of Project

Results from a proof-of-concept (POC) could not exactly be reproduced, since BMA does not converge at all over multiple runs with applied parameters. However, using a higher number of iterations to make BMA converge results in a different set of inclusion probabilities, of which several are similar to the ones found with the POC. When trying to apply the same method to a higher number of features, the multiple imputation step diverges, thus making the method not directly applicable to larger datasets. Additionally, analysis of the POC resulted in a list of conceptual problems which need to be discussed before the project can continue. The discussion thereof is done in a separate section below.

## Problems to be discussed

* **BUSINESS** What would we do based on the calculated inclusion probabilities to improve diagnostics?
* **DATA** Does following a diagnostic path to choose an analyte result in predicting high inclusion probability thereof?
* **DATA** Can we impute a value that is only set in negative samples? The data is definitely not missing at random. Since the domain is different between positive and negative samples, this knowledge can not be transferred
* **FEATURE** The main diagnosis is not necessarily the full label of the sample, instead we should get the full set of diagnoses
* **EXPERIMENT** Does BMA require only positive samples or does it require positive and negative samples?
* **EXPERIMENT** Is inclusion probability really similar to feature importance?

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
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
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
