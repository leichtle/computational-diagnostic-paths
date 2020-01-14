import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegressionCV
from sklearn.model_selection import KFold
import re

df = pd.read_csv('./data/processed/no_hormones_preprocessed_onehot.csv')

feature_cols1 = ['Cycle.LP..day_4', 'Cycle.LP..day_NA', 'MIDKINE.ng.mL', 'BMI', 'Cycle.LP..day_36', 'Cycle.LP..day_3', 'VEGF.pg.mL', 'Mens..Pain.VAS.0.10', 'Defensin.pg.mL',
                'Cycle.LP..day_26', 'Cycle.LP..day_hysterect.', 'Later.available_DMSO', 'Cycle.LP..day_6.weeks', 'Cycle.LP..day_11', 'Cycle.LP..day_34', 'Cycle.LP..day_menomet.',
                'Later.available_Yes.', 'CRP.ng.mL', 'PAIN_High.menstrual.pain.level', 'Cycle.LP..day_Postmenop']

feature_cols2 = list(df.columns)

feature_cols3 = []

for col1 in feature_cols1:
    for col2 in feature_cols2:
        if re.match(col1, col2) is not None:
            feature_cols3.append(col2)
            break

X = df[feature_cols3].values
y = df['GROUP'].values

clf = LogisticRegressionCV(cv=5, random_state=0).fit(X, y)
print(clf.score(X, y))

#model = LinearRegression()
# scores = []
# kfold = KFold(n_splits=3, shuffle=True, random_state=42)
# for i, (train, test) in enumerate(kfold.split(X, y)):
#     model.fit(X.iloc[train, :], y.iloc[train, :])
#     score = model.score(X.iloc[test, :], y.iloc[test, :])
#     scores.append(score)
# print(scores)
