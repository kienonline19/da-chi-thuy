import pandas as pd

df = pd.read_csv("decision.csv")

required = ["login", "add-withdrawal-address", "withdraw-funds"]
required_set = set(required)


base = df[df["funds_stolen"].eq(True)].copy()


all_fn_true = base.groupby("ticket_id")["false_negative"].transform("all")
base2 = base[all_fn_true].copy()


present_sets = (
    base2[base2["policy_set"].isin(required)]
    .groupby("ticket_id")["policy_set"]
    .apply(lambda s: set(s.astype(str)))
)

tickets = pd.Index(base2["ticket_id"].unique(), name="ticket_id")

rows = []
for tid in tickets:
    present = present_sets.get(tid, set())
    missing = sorted(required_set - set(present))
    if missing:
        rows.append({
            "ticket_id": tid,
            "missing_policy_set": ", ".join(missing),
            "missing_count": len(missing)
        })

out_df = (pd.DataFrame(rows)
          .sort_values(["missing_count", "ticket_id"], ascending=[False, True])
          .reset_index(drop=True))


exploded = out_df.assign(
    missing_policy_set=out_df["missing_policy_set"].str.split(r"\s*,\s*")
).explode("missing_policy_set")
exploded.to_csv("sol2.csv", index=False)
