#!/bin/sh
cp ./myocardial_ischemia_1929.csv ./myocardial_ischemia_1929_fixed.csv

# add NA between two ; (first two), then add NA at the beginning and end of the line
sed -i 's/\;\;/\;NA\;/g
s/\;\;/\;NA\;/g
s/\;$//g
s/^\;/NA\;/g
s/\;N$//g' myocardial_ischemia_1929_fixed.csv

