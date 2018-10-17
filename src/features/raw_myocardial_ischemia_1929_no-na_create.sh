#!/bin/sh
cp ../raw/raw_myocardial_ischemia_1929.csv ./raw_myocardial_ischemia_1929_no-na.csv
sed -i 's/\;NA\;/\;\;/g
s/\;NA\;/\;\;/g
s/\;NA$/\;/g
s/^NA\;/\;/g' raw_myocardial_ischemia_1929_no-na.csv