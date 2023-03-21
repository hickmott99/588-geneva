import pandas as pd
import time

FILE_PATH = "../geneva_320_data.txt"
OUTPUT_FILE = "./geneva_output.csv"

def next_word(line, running_offset):
    next_space_idx = line[running_offset:].find(" ") + running_offset
    if(next_space_idx == -1): 
        print("ERROR")
        return "", -1
    ret_val = line[running_offset:next_space_idx]
    running_offset = next_space_idx + 1

    return ret_val, running_offset


def parse_line(line):
    """ Avg. Fitness 0.0: [TCP:options-sack:]-duplicate(duplicate(,duplicate),)-| \/  (Evaluated 12 times: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) """   
    running_offset = 0

    avg_str, running_offset = next_word(line, 0)
    fitness_str, running_offset = next_word(line, running_offset)
    fitness_num, running_offset = next_word(line, running_offset)

    # Strategy while loop
    strategy = ""
    while True:
        new_idx = line[running_offset:].find(" ") + running_offset
        if(new_idx == -1): return -1, -1, -1, -1
        indi = line[running_offset:new_idx]
        if(indi == "\/"):
            break
        strategy += indi
        running_offset = new_idx + 1

    or_str, running_offset = next_word(line, running_offset)
    evaluated_str, running_offset = next_word(line, running_offset)
    evaluation_num, running_offset = next_word(line, running_offset)
    times_str, running_offset = next_word(line, running_offset)
    evaluations_arr = line[running_offset:].strip("][()").split(', ')

    return fitness_num, strategy, evaluation_num, evaluations_arr
    
df = pd.DataFrame(columns = ['Avg. Fitness', 'Strategy DNA', 'Evaluation Num', 'Evaluations'])

with open(FILE_PATH) as file:
    for line in file:
        line = line.rstrip().replace("  ", " ")
        if(line != "Results:" and len(line) != 0): 
            fitness_num, strategy, evaluation_num, evaluations_arr = parse_line(line)
            # data = {
            #     'Avg. Fitness': fitness_num,
            #     'Strategy DNA': strategy,
            #     'Evaluation Num': evaluation_num,
            #     'Evaluations': evaluations_arr
            # }
            # print(fitness_num, strategy, evaluation_num, evaluations_arr)
            # indi_df1 = pd.DataFrame(data,
            #        columns = ['Avg. Fitness', 'Strategy DNA', 'Evaluation Num', 'Evaluations'])
            df = df.append({
                'Avg. Fitness' : fitness_num[:-1], 
                'Strategy DNA' : strategy, 
                'Evaluation Num' : evaluation_num,
                'Evaluations' : evaluations_arr},
                ignore_index = True)
            # df.reset_index(drop=True, inplace=True)
            # indi_df1.reset_index(drop=True, inplace=True)
            # print(indi_df1)
            # df = pd.concat([df, indi_df1], axis=1)
            # new_df = pd.DataFrame([fitness_num, strategy, evaluation_num, evaluations_arr])
            # df = pd.concat([df, new_df], axis=0, ignore_index=True)
# print(OUTPUT_FILE)
print(df)

df.to_csv(OUTPUT_FILE, encoding='utf-8', index=False)