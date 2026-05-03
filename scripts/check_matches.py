# import os

# # Verify it's set
# print(os.environ.get("OPENAI_API_KEY", "NOT SET"))

# # Test the API directly
# import openai
# client = openai.OpenAI()
# response = client.messages.create(
#     model="gpt-4.1-mini",
#     max_tokens=10,
#     messages=[{"role": "user", "content": "say hi"}]
# )
# print(response.content)

import os
from openai import OpenAI


client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Say hi in one short sentence."
)

print(response.output_text)

######

# import os

# import anthropic
# client = anthropic.Anthropic()
# response = client.messages.create(
#     model="claude-sonnet-4-6",
#     max_tokens=50,
#     temperature=0,
#     messages=[{"role": "user", "content": "say hi in JSON like {\"message\": \"hi\"}"}]
# )
# print(response.content)

########

# import pandas as pd

# #file1 = "data/processed/holdout_real_reviews.csv"
# file1 = "data/results/holdout_anthropic_claude-sonnet-4-6.csv"
# file2 = "data/results/holdout_human_consensus.csv"

# df1 = pd.read_csv(file1)
# df2 = pd.read_csv(file2)

# # Normalize IDs (important!)
# uids1 = set(df1["review_uid"].astype(str).str.strip())
# uids2 = set(df2["review_uid"].astype(str).str.strip())

# matches = uids1 & uids2
# only_in_1 = uids1 - uids2
# only_in_2 = uids2 - uids1

# print(f"File 1 total: {len(uids1)}")
# print(f"File 2 total: {len(uids2)}")
# print(f"Matches: {len(matches)}")
# print(f"Only in file 1: {len(only_in_1)}")
# print(f"Only in file 2: {len(only_in_2)}")

# # Show a few examples to sanity-check
# print("\nSample matches:", list(matches)[:5])
# print("Sample only in file 1:", list(only_in_1)[:5])
# print("Sample only in file 2:", list(only_in_2)[:5])