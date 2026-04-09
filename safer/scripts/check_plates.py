import pandas as pd


def main(path: str = "output/results.csv"):
    df = pd.read_csv(path)
    print(df["status"].value_counts())


if __name__ == "__main__":
    main()
