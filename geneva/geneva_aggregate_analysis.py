import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os
import numpy as np

ROOT = "./final_output/"
FINAL_CSV = os.path.join(ROOT, "FinalOutput.csv")
PLOTS_DIR = os.path.join(ROOT, "plots")

TOP_STRATS = [
    # First 5 have highest max amp, second 5 have highest num times generated
    "[TCP:options-nop::0]-tamper{TCP:options-altchksumopt:corrupt}(duplicate,)-|",
    "[TCP:options-nop::0]-tamper{TCP:options-uto:corrupt}(tamper{TCP:seq:replace:3188742420},)-|",
    "[TCP:options-eol::0]-tamper{TCP:sport:replace:57380}-|",
    "[TCP:options-eol:]-fragment{tcp:-1:True}-|",
    "[TCP:options-nop::0]-tamper{TCP:reserved:replace:6}-|",
    "",
    "[TCP:options-sackok:]-duplicate-|",
    "[TCP:options-altchksumopt:]-duplicate-|",
    "[TCP:options-nop:]-duplicate-|",
    "[TCP:options-sack:]-duplicate-|",
    ###
]


def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = os.listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def add_indv_max_amp(df):
    df["Max Amp"] = [max([float(xx) for xx in x.strip(
        "[]").split(", ")]) for x in df["Evaluations"]]
    return df


def count_positive_amps():
    output_dir = os.path.join(ROOT, 'outputs/')
    csvs = find_csv_filenames(output_dir)
    count = 0
    check_c = 0
    total = 0
    top_counts = [0] * len(TOP_STRATS)
    check_tc = [0] * len(TOP_STRATS)
    pos_top_counts = [0] * len(TOP_STRATS)
    check_ptc = [0] * len(TOP_STRATS)

    num_suc_og = 0
    num_suc_og2 = 0
    # print(add_indv_max_amp(pd.read_csv(
    #     os.path.join(output_dir, csvs[0]))).head())
    # y = ["[-10, 1, 0, -100]", "[-10, 1, 1.5, -100]"]
    # print(sum([sum([float(xx) > 1 for xx in x.strip("[]").split(", ")]) for x in y]))
    max_amp_per_ip = []
    for csv in csvs:
        total += 1
        df = add_indv_max_amp(pd.read_csv(os.path.join(output_dir, csv)))
        df = df.fillna('')
        if sum([sum([float(xx) > 1 for xx in x.strip("[]").split(", ")]) for x in df["Evaluations"]]) >= 1:
            count += 1
        # if sum([x > 1 for x in df["Max Amp"]]):
        #     check_c += 1
        locs = [x.split("]")[0].split(":")[-1]
                == "0" for x in df["Strategy DNA"]]
        locs = np.add(locs, [x == "" for x in df["Strategy DNA"]])
        df2 = df[locs]
        df2 = df2[df2["Max Amp"] > 1]
        if len(df2) > 0:
            num_suc_og += 1

        antilocs = [x == 0 for x in locs]
        # print(sum([x == 0 for x in np.add(antilocs, locs)]))
        df2 = df[antilocs]
        df2 = df2[df2["Max Amp"] > 1]
        if len(df2) > 0:
            num_suc_og2 += 1

        # print(len(df2["Strategy DNA"].unique()))
        for i, top in enumerate(TOP_STRATS):
            df2 = df[df["Strategy DNA"] == top]
            if sum([sum([float(xx) > 1 for xx in x.strip("[]").split(", ")]) for x in df2["Evaluations"]]) >= 1:
                pos_top_counts[i] += 1
                # v = df2["Max Amp"].max()
                # print(f"{top}, {csv}, {v}")
            # if sum([x > 1 for x in df2["Max Amp"]]):
            #     check_ptc[i] += 1
            # print(f"first {csv}, {i}")
            if top in df["Strategy DNA"].unique():
                # v = df2["Max Amp"].max()
                # print(f"{top}, {csv}, {v}")
                top_counts[i] += 1
            # print(f"second {csv}")
        max_amp_per_ip.append(df["Max Amp"].max())

    print(f"num with effective amp: {count}, total: {total}")
    print(f"num occurences per strat: {top_counts}")
    print(f"num occurences per strat with effective amp: {pos_top_counts}")
    # print(check_ptc)
    max_amp_per_ip.sort(reverse=True)
    # print(max_amp_per_ip)
    # print(len(max_amp_per_ip))
    plt.plot(range(len(max_amp_per_ip)), max_amp_per_ip)
    plt.xlabel("IP Address Rank", fontweight="bold")
    plt.ylabel("Amplification Factor", fontweight="bold")
    # plt.yticks([0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4,
    #    4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5])
    plt.grid(linestyle='--')
    plt.savefig("line.png")
    plt.clf()
    print(f"PSH+ACK Seq: {num_suc_og}")
    print(f"Other Seq: {num_suc_og2}")


def main():
    df = pd.read_csv(FINAL_CSV)
    # df = df[df["Num Times Generated"] > 1]
    # df = df[df["Total Amplification"] > 0]
    count_positive_amps()
    print(f"{sum([x > 1 for x in df['Max Amplification']])}")
    print(f"total starts {len(df)}")
    df = df.fillna('')
    # df2 = df[sum([sum([float(xx) > 1 for xx in x.strip("[]").split(", ")])
    #              for x in df["Evaluations"]]) >= 1]
    # df2 = df2.sort_values(by="Num Times Generated", ascending=False)

    df = df.sort_values(by="Num Times Generated", ascending=False)
    print(df.head())

    # locs = [x.split("]")[0].split(":")[-1]
    #         == "0" for x in df["Strategy DNA"]]
    # df[locs].to_csv("check.csv")

    df = df.sort_values(by="Max Amplification", ascending=False)
    filterd_df = df[df["Max Amplification"] > 1]
    plt.hist(filterd_df["Max Amplification"], bins=[
             1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75,
             #    4, 4.25, 4.5, 4.75, 5, 5.25, 5.5, 5.75, 6, 6.25, 6.5, 6.75, 7, 7.25, 7.5, 7.75, 8, 8.25, 8.5
             ])
    plt.xlabel('Max Amplification')
    plt.ylabel('# Strategies')
    plt.savefig("hist.png")
    plt.clf()
    plt.boxplot(filterd_df["Max Amplification"])
    plt.xticks([], [])
    plt.ylabel("Amplification Factor")
    plt.subplots_adjust(left=0.5)
    plt.savefig("box.png")
    plt.clf()
    # sns.kdeplot(filterd_df["Max Amplification"])
    # plt.savefig("density.png")
    # plt.clf()

    return

    column_names = ["Total Amplification",
                    "Num Times Generated", "Average Amplification", "Max Amplification"]
    for column_name in column_names:
        df = df.sort_values(by=column_name, ascending=False)
        print(f"Sorted by {column_name}")
        print(df.head())
        print(f"Min: {df[column_name].min()}, Max: {df[column_name].max()}")
        # hist = df.hist(column=column_name)
        acr = ''.join([word[0] for word in column_name.split(' ')]).lower()
        if column_name != "Num Times Generated":
            plt.scatter(df[column_name], df["Num Times Generated"])
            plt.savefig(PLOTS_DIR + acr + "_sp" + ".png")
            plt.clf()
        # else:
        plot_ = sns.countplot(x=df[column_name])
        num_ticks = len(df[column_name].unique()) // 5
        plot_.xaxis.set_major_locator(ticker.MultipleLocator(num_ticks))
        plot_.xaxis.set_major_formatter(lambda x, pos: str(round(x) + 1))
        plt.savefig(PLOTS_DIR + acr + "_cp" + ".png")
        plt.clf()
        # plt.boxplot(df[column_name])
        # plt.savefig(PLOTS_DIR + acr + "_bp" + ".png")
        # plt.clf()

    # df_ta = df.sort_values(by="Total Amplification", ascending=False)
    # print(df_ta.head())
    # print(f"Min: {df['Total Amplification'].min(axis=1)}, Max: {df['Total Amplification'].max(axis=1)}")
    # plt.hist(df["Total Amplification"], bins=100)
    # plt.savefig(PLOTS_DIR + "ta.png")

    # df_ntg = df.sort_values(by="Num Times Generated", ascending=False)
    # print(df_ntg.head())
    # print(f"Min: {df['Num Times Generated'].min(axis=1)}, Max: {df['Num Times Generated'].max(axis=1)}")
    # plt.hist(df["Num Times Generated"], bins=100)
    # plt.savefig(PLOTS_DIR + "ntg.png")

    # df_aa = df.sort_values(by="Average Amplification", ascending=False)
    # print(df_aa.head())
    # print(f"Min: {df['Average Amplificatio'].min(axis=1)}, Max: {df['Average Amplificatio'].max(axis=1)}")
    # plt.hist(df["Average Amplification"], bins=100)
    # plt.savefig(PLOTS_DIR + "aa.png")


if __name__ == "__main__":
    main()
