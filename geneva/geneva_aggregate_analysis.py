import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

def main():
    FINAL_CSV = "./output_hickmott/CooperFinalOutput.csv"
    PLOTS_DIR = "./output_elandg/"
    df = pd.read_csv(FINAL_CSV)
    df = df[df["Num Times Generated"] > 1]
    df = df[df["Total Amplification"] > 0]

    column_names = ["Total Amplification", "Num Times Generated", "Average Amplification"]
    for column_name in column_names:
        df = df.sort_values(by=column_name, ascending=False)
        print(df.head())
        print(f"Min: {df[column_name].min()}, Max: {df[column_name].max()}")
        # hist = df.hist(column=column_name)
        acr = ''.join([word[0] for word in column_name.split(' ')]).lower()
        plot_ = sns.countplot(x=df[column_name])
        num_ticks = len(df[column_name].unique()) // 5
        plot_.xaxis.set_major_locator(ticker.MultipleLocator(num_ticks))
        plot_.xaxis.set_major_formatter(lambda x, pos: str(round(x) + 1))
        plt.savefig(PLOTS_DIR + acr + "_cp" + ".png")
        plt.clf()
        plt.boxplot(df[column_name])
        plt.savefig(PLOTS_DIR + acr + "_bp" + ".png")
        plt.clf()

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