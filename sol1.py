import pandas as pd

df = pd.read_csv("decision.csv")

required = {"login", "add-withdrawal-address", "withdraw-funds"}

base_A = df[df["funds_stolen"].eq(True)].copy()

distinct_cnt_A = (
    base_A["policy_set"].where(base_A["policy_set"].isin(required))
          .groupby([base_A["userid"], base_A["ticket_id"]])
          .transform("nunique")
)

target_A = base_A[distinct_cnt_A.ge(2)].copy()

has_true_A = target_A.groupby(["userid", "ticket_id"])["true_positive"].transform("any")
final_A = target_A[(target_A["true_positive"].eq(True)) | (~has_true_A)].copy()


base_B = df[df["funds_stolen"].eq(False)].copy()

gcols_B = ["userid", "ticket_id"]

policy_nuniq_B = base_B.groupby(gcols_B)["policy_set"].transform("nunique")
has_true_B = base_B.groupby(gcols_B)["true_positive"].transform("any")
has_false_B = base_B.groupby(gcols_B)["true_positive"].transform(lambda s: (~s).any())

target_B = base_B[policy_nuniq_B.ge(2) & has_true_B & has_false_B].copy()

final_B = target_B[
    target_B["true_positive"].eq(True) &
    target_B["live_policies"].fillna("").ne("default")
].copy()

rest = df.drop(index=target_A.index.union(target_B.index))

final_df = pd.concat([rest, final_A, final_B]).sort_index()

final_df.to_csv("sol1.csv", index=False)
