import pandas as pd
import hashlib
from datetime import datetime, timedelta
import random

# === INPUT / OUTPUT ===
input_file = "data/labels/holdout_human_labeling_sheet.csv"
output_file = "data/processed/holdout_real_reviews.csv"

df = pd.read_csv(input_file)

# --- helper: generate fake but stable user_id from review_uid ---
def hash_user(uid):
    return hashlib.md5(uid.encode()).hexdigest()[:16]

# --- helper: word count ---
def count_words(text):
    if pd.isna(text):
        return 0
    return len(str(text).split())

# --- helper: fake timestamp ---
base_date = datetime(2015, 1, 1)

def random_date(i):
    return (base_date + timedelta(days=i)).strftime("%Y-%m-%d")

# --- transform ---
out = pd.DataFrame()

out["review_uid"] = df["review_uid"]
out["source_file"] = "synthetic_from_coder_annotations.csv"

# fake book_id (you can improve this if you have real ones)
out["book_id"] = (
    df["block_id"]
    .astype("category")
    .cat.codes
    .astype("int32")   # or int64
    + 1000000
)

out["user_id_hash"] = df["review_uid"].apply(hash_user)
out["rating"] = df["rating"]
out["review_text"] = df["review_text"]

out["word_count"] = df["review_text"].apply(count_words)
out["length_bucket"] = df["length_bucket"]

# optional / missing fields
out["date_added"] = ""
out["timestamp"] = [random_date(i) for i in range(len(df))]
out["has_spoiler"] = False
out["n_votes"] = ""
out["n_comments"] = ""

# --- save ---
out.to_csv(output_file, index=False)

print(f"Saved to {output_file}")