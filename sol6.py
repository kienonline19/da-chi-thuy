import pandas as pd

sol1 = pd.read_csv("sol1.csv")

# normalize timestamp để group chuẩn
sol1["_ts"] = pd.to_datetime(sol1["action_timestamp"], errors="coerce")

# normalize true_positive nếu là string "TRUE"/"FALSE"
if sol1["true_positive"].dtype == object:
    sol1["_tp"] = (sol1["true_positive"].astype(str).str.strip().str.lower()
                   .map({"true": True, "false": False}))
else:
    sol1["_tp"] = sol1["true_positive"]

keys = ["userid", "_ts", "live_policies"]

mask = (
    sol1.groupby(keys)["ticket_id"].transform("nunique").gt(1) &
    sol1.groupby(keys)["_tp"].transform("nunique").ge(2)
)

out_df = sol1[mask].drop(columns=["_ts", "_tp"])

out_df.to_csv("sol6.csv", index=False)
