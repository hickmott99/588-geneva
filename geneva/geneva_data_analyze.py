import os
import csv
import pandas as pd

INPUT_DIR = "./output_hickmott/output_hickmott_pop250_1/"
OUTPUT_FILE = "./output_hickmott/CooperFinalOutput.csv"


strategy_found_in_all = {}

for ii, file in enumerate(os.listdir(INPUT_DIR)):
    if file.startswith("idx") and file[-3:]=="csv":
        file_path = INPUT_DIR + file

        with open(file_path) as file:
            csv_reader = csv.reader(file, delimiter=',')
            for line in csv_reader:
                if line[0][0] != "A" and len(line)>=4:
                    strat = line[1]
                    if strat not in strategy_found_in_all:
                        strategy_found_in_all[strat] = [[float(line[0]), float(line[2]), (line[3])]]
                    else:
                        strategy_found_in_all[strat].append([float(line[0]), float(line[2]), (line[3])])



sort = sorted(strategy_found_in_all.items(), key=lambda x:len(x[1]), reverse=True)

# for each strategy
for ii, val in enumerate(sort):
    prod = val[1][0][0]*val[1][0][1]

    average = 0
    # for each IP, Website pair with this strategy
    for val2 in val[1]:
        prod = val2[0]*val2[1]
        average += prod


    sort[ii] = [sort[ii][0], average, len(sort[ii][1]), average/len(sort[ii][1])]

df = pd.DataFrame(columns = ['Strategy DNA', 'Total Amplification', 'Num Times Generated', 'Average Amplification'], data=sort)
df.to_csv(OUTPUT_FILE, encoding='utf-8', index=False)

