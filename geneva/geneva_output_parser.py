import pandas as pd
import time
import os

### Converts idx-*.txt files in INPUT_DIR to idx-*.csv ###

INPUT_DIR = "./output_hickmott/output_hickmott_pop250_1/"


def next_word(line, running_offset):
    """ Returns substring until next space char of line after running_offset index. """
    next_space_idx = line[running_offset:].find(" ") + running_offset
    if(next_space_idx == -1):
        print("ERROR")
        return "", -1
    ret_val = line[running_offset:next_space_idx]
    running_offset = next_space_idx + 1

    return ret_val, running_offset


def parse_line(line):
    """ Parses a single line of Geneva output.
    Line Format: Avg. Fitness 0.0: [TCP:options-sack:]-duplicate(duplicate(,duplicate),)-| \/  (Evaluated 12 times: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    """
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


def parse_single_output(file_path):
    OUTPUT_FILE = file_path[:-3]+"csv" # "./output_hickmott/output_hickmott_pop250_1/idx-153.csv"


    df = pd.DataFrame(columns = ['Avg. Fitness', 'Strategy DNA', 'Evaluation Num', 'Evaluations'])

    with open(file_path) as file:
        for line in file:
            line = line.rstrip().replace("  ", " ")
            if(len(line) != 0 and line[0]=="A"):
                fitness_num, strategy, evaluation_num, evaluations_arr = parse_line(line)
                evaluations_arr = [eval(i) for i in evaluations_arr]

                df = df.append({
                    'Avg. Fitness' : fitness_num[:-1],
                    'Strategy DNA' : strategy,
                    'Evaluation Num' : evaluation_num,
                    'Evaluations' : evaluations_arr},
                    ignore_index = True)

    df.to_csv(OUTPUT_FILE, encoding='utf-8', index=False)


for ii, file in enumerate(os.listdir(INPUT_DIR)):
    if file.startswith("idx") and file[-3:]=="txt":
        file_path = INPUT_DIR + file
        parse_single_output(file_path)
