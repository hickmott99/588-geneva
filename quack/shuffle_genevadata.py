import pandas as pd

def main():
    INPUT_PATH = "./genevadata.txt"
    OUTPUT_PATH = "./shuffled_genevadata.csv"

    shuffled_pairs = {"IP": [], "URL":[]}
    with open(INPUT_PATH) as f:
        for line in f:
            ip, url = line.split(' ')
            shuffled_pairs["IP"].append(ip)
            # remove newline character from url in txt file
            shuffled_pairs["URL"].append(url[:-1])
            
        # has index column
        df = pd.DataFrame.from_dict(shuffled_pairs)
        print(df.head())
        # shuffles and adds new index column
        df = df.sample(frac=1).reset_index()
        print(df.head())
        df.to_csv(OUTPUT_PATH)

if __name__ == "__main__":
    main()