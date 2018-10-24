
import re

if __name__ == "__main__":

    with open("myocardial_ischemia_1929.csv", "r") as source:
        lines = source.readlines()
    with open("myocardial_ischemia_1929_fixed_2.csv", "w") as destination:
        for line in lines:
            line = re.sub(r';;', ';NA;', line)
            line = re.sub(r';;', ';NA;', line)
            line = re.sub(r'^;', 'NA;', line)
            line = re.sub(r';$', '', line)
            line = re.sub(r';N$', '', line)  # remove strange ;N column at the end
            destination.write(line)
