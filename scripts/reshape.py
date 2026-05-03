import pandas as pd

df = pd.read_csv("data/labels/master.csv")

rows = []
for review_uid, group in df.groupby("review_uid", sort=False):
    group = group.reset_index(drop=True)
    row = {
        "review_uid": review_uid,
        "block_id": group["block_id"].iloc[0],
        "rating": group["rating"].iloc[0],
        "length_bucket": group["length_bucket"].iloc[0],
        "review_text": group["review_text"].iloc[0],
    }
    for i, r in group.iterrows():
        row[f"coder_{i+1}_commitment"]     = r["commitment"]
        row[f"coder_{i+1}_recommendation"] = r["recommendation"]
        row[f"coder_{i+1}_emotions"]       = r["emotions"]
    rows.append(row)

reshaped = pd.DataFrame(rows)
reshaped.to_csv("data/labels/holdout_human_labeling_sheet.csv", index=False)
print(f"Done! {len(reshaped)} reviews written.")