import pandas as pd

df = pd.read_csv("decision.csv")


mask_base = df["funds_stolen"].eq(False) & df["false_negative"].eq(True)


tickets_with_withdraw = df.loc[
    mask_base & df["policy_set"].eq("withdraw-funds"),
    "ticket_id"
].unique()


out_df = df.loc[
    mask_base & df["ticket_id"].isin(tickets_with_withdraw)
].copy()

out_df.to_csv("sol4.csv", index=False)
