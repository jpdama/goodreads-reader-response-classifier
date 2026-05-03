import pandas as pd
from pathlib import Path

files = [
    "data/labels/holdout_JP.csv",
    "data/labels/holdout_Eliza.csv",
    "data/labels/holdout_Tori.csv",
    "data/labels/holdout_Eddy.csv",
    "data/labels/holdout_Ashton.csv",
]

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df.to_csv("master.csv", index=False)