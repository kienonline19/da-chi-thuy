import pandas as pd

df = pd.read_csv("decision.csv")
df["_ts"] = pd.to_datetime(df["action_timestamp"], errors="coerce")


base = df[(df["funds_stolen"]) & (df["false_negative"])]


pivot = (
    base[base["policy_set"].isin(
        ["login", "add-withdrawal-address", "withdraw-funds"])]
    .groupby(["ticket_id", "policy_set"])["_ts"]
    .min()
    .unstack()
)


bad_ticket = pivot[
    (pivot["login"] > pivot["add-withdrawal-address"]) |
    (pivot["login"] > pivot["withdraw-funds"])
].index


result = base[base["ticket_id"].isin(bad_ticket)]

result.to_csv("sol3.csv", index=False)
