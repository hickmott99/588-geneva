import subprocess
import csv

# constants
COOPER_START_IDX = 0
parent_output_dir = "./output_elandg/output_elandg_pop250_1"
csv_path = "../quack/shuffled_genevadata.csv"


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


# read IP Website CSV data
csv_data = []
with open(csv_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if row[0] != "":
            csv_data.append(row)

# run geneva on each desired pair
for ii, line in enumerate(csv_data):
    if ii > COOPER_START_IDX:
        printProgressBar(ii - 1 - COOPER_START_IDX, len(csv_data)-COOPER_START_IDX-1, prefix="IP:" +
                         line[2] + "   Website:" + line[3] + '  Progress:', suffix='Complete', length=50)

        file = parent_output_dir+"/idx-"+str(ii)+".txt"

        cmd = ["sudo", "python3", "evolve.py", "--test-type", "amplification",
               "--population", "250", "--generations", "10", "--dst", line[2], "--site", line[3]]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output) = process.communicate()
        with open(file, 'w') as f:
            f.write("IP:" + line[2] + "   Website:" + line[3] + "\n\n")
            f.write(output[1].decode('utf-8'))

printProgressBar(len(csv_data), len(csv_data),
                 prefix='\rProgress:', suffix='Complete', length=50)
