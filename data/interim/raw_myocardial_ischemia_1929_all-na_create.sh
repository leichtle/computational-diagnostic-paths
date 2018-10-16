#!/bin/sh
cp ../raw/raw_myocardial_ischemia_1929.csv ./raw_myocardial_ischemia_1929_all-na.csv

# add NA between two ; (first two), then add NA at the beginning and end of the line
sed -i 's/\;\;/\;NA\;/g
s/\;\;/\;NA\;/g
s/\;$//g
s/^\;/NA\;/g
s/\;N$//g' raw_myocardial_ischemia_1929_all-na.csv