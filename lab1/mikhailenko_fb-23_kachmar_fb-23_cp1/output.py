import pandas as pd
import glob

csv_files = glob.glob("*.csv")

for file in csv_files:
    print(f"Файл: {file}")
    df = pd.read_csv(file)
    print(df.head(), "\n")
