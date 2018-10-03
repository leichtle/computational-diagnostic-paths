import pandas as pd
from model.imputation.imputation_helper import selectively_impute
import datetime

mi_df = pd.read_csv('../data/raw_myocardial_ischemia.csv', header=0)  # read data from csv

print("Performing imputation...")
mi_df = selectively_impute(mi_df)  # perform selective imputation
print("...Done.")

print("----------------------")
print("Imputed data for inspection:")
print(mi_df.head())                 # print data for sanity check

file_name = './imputations/' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '-mi-imputation.csv'
mi_df.to_csv(file_name, index=False)

