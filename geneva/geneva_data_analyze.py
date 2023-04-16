import os
import csv
import pandas as pd


INPUT_DIR = "./final_output/"
OUTPUT_FILE = "./final_output/FinalOutput.csv"


# key = strategy, value = [(Avg Fitness, Num Times Evaluated, [Evaluations]), (), ...]
strategy_found_in_all = {}
max_evaluation_strategy = {}  # key = strategy, value = max evaluation


for ii, file in enumerate(os.listdir(INPUT_DIR)):
    if file.startswith("idx") and file[-3:] == "csv":
        file_path = INPUT_DIR + file
        with open(file_path) as file:
            csv_reader = csv.reader(file, delimiter=',')
            for line in csv_reader:
                if line[0][0] != "A" and len(line) >= 4:
                    strat = line[1]
                    if strat not in strategy_found_in_all:
                        strategy_found_in_all[strat] = [
                            [float(line[0]), float(line[2]), (line[3])]]
                    else:
                        strategy_found_in_all[strat].append(
                            [float(line[0]), float(line[2]), (line[3])])

# total = 0
# for strat in strategy_found_in_all:
#     for gen in strategy_found_in_all[strat]:
#         total += gen[1]

# print(total)

# exit()

# print(strategy_found_in_all[""])

for strat in strategy_found_in_all:
    max_evaluation = -99999999
    for indi_genetic_run in strategy_found_in_all[strat]:
        strat_indirun_evaluations = indi_genetic_run[2]
        res = strat_indirun_evaluations.strip('][').split(', ')
        max_strat = max([float(x) for x in res])

        if (max_strat > max_evaluation):
            max_evaluation = max_strat
    max_evaluation_strategy[strat] = max_evaluation

count = 0
results = []
for strat in strategy_found_in_all:
    total_amp = 0
    total_count = 0
    for indi_genetic_run in strategy_found_in_all[strat]:
        strat_indirun_evaluations = indi_genetic_run[2]
        res = strat_indirun_evaluations.strip('][').split(', ')
        res = [float(x) for x in res]
        assert (indi_genetic_run[0] == sum(
            res) / indi_genetic_run[1])
        assert (indi_genetic_run[1] == len(res))
        total_amp += sum(res)
        total_count += indi_genetic_run[1]
    avg_amp = total_amp / total_count
    results.append([strat, total_amp, total_count, avg_amp,
                   max_evaluation_strategy[strat]])
    count += total_count
assert (count == 10*250*257)
df = pd.DataFrame(columns=['Strategy DNA', 'Total Amplification',
                  'Num Times Generated', 'Average Amplification', 'Max Amplification'], data=results)
print(df['Max Amplification'])
df.to_csv(OUTPUT_FILE, encoding='utf-8', index=False)


# sort = sorted(strategy_found_in_all.items(),
#               key=lambda x: len(x[1]), reverse=True)

# # for each strategy
# for ii, val in enumerate(sort):
#     strat = val[0]
#     # val[1] is list of tuples (Avg Fitness, Num Times Evaluated, [Evaluations])

#     total_amp = 0
#     total_count = 0
#     # for each IP, Website pair with this strategy
#     for val2 in val[1]:
#         prod = val2[0]*val2[1]
#         total += prod

#     sort[ii] = [strat, total_amp, num, total_amp /
#                 num, max_evaluation_strategy[strat]]

# df = pd.DataFrame(columns=['Strategy DNA', 'Total Amplification',
#                   'Num Times Generated', 'Average Amplification', 'Max Amplification'], data=sort)
# df.to_csv(OUTPUT_FILE, encoding='utf-8', index=False)
