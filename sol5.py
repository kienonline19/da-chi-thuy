import pandas as pd

df = pd.read_csv("sol1.csv")


df["_ts"] = pd.to_datetime(df["action_timestamp"], errors="coerce")

keys = ["userid", "_ts", "live_policies"]

multi_ticket = df.groupby(keys)["ticket_id"].transform("nunique").gt(1)

out_df = df[multi_ticket].copy()

out_df.to_csv("sol5.csv", index=False)
