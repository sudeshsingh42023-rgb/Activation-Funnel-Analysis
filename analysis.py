"""Student acquisition & activation funnel: personas, channel funnel, CAC, cohorts, referral loop."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sv = pd.read_csv("data/survey.csv")
ev = pd.read_csv("data/funnel_events.csv")
cost = pd.read_csv("data/channel_costs.csv")

# ---------- 1. Personas (rule-based segmentation) ----------
def persona(r):
    if r.would_try_free_sprint_1to5 >= 4 and r.internship_confidence_1to5 <= 2: return "Eager Strugglers"
    if r.would_try_free_sprint_1to5 >= 4: return "Confident Climbers"
    if r.did_internship_before == 1: return "Experienced Skeptics"
    return "Passive Browsers"
sv["persona"] = sv.apply(persona, axis=1)
pers = sv.groupby("persona").agg(n=("respondent","count"),
        top_pain=("pain_point", lambda s: s.mode().iat[0]),
        top_channel=("preferred_channel", lambda s: s.mode().iat[0]),
        avg_interest=("would_try_free_sprint_1to5","mean")).round(2)
pers["share_%"] = (100*pers.n/pers.n.sum()).round(1)
print("== Personas ==\n", pers.to_string()); pers.to_csv("outputs/personas.csv")
print("\nTop pain points (%):\n", (100*sv.pain_point.value_counts(normalize=True)).round(1).to_string())

# ---------- 2. Channel funnel ----------
f = ev.groupby("channel").agg(reached=("student_id","count"), signed_up=("signed_up","sum"),
        applied=("applied_sprint","sum"), completed=("completed_sprint","sum"))
f["signup_%"] = (100*f.signed_up/f.reached).round(1)
f["apply_of_signup_%"] = (100*f.applied/f.signed_up).round(1)
f["complete_of_apply_%"] = (100*f.completed/f.applied).round(1)
f["activation_%"] = (100*f.completed/f.reached).round(1)   # reached -> completed
f = f.join(cost.set_index("channel"))
f["cost_per_activated_inr"] = (f.spend_inr / f.completed).round(0)
# time-cost proxy for free channels: assume 1 hr of volunteer effort per 10 reached @ Rs 100/hr
f["effort_cost_inr"] = (f.reached/10*100).round(0)
f["total_cost_per_activated_inr"] = ((f.spend_inr+f.effort_cost_inr)/f.completed).round(0)
print("\n== Channel funnel ==\n", f.to_string()); f.to_csv("outputs/channel_funnel.csv")
best = f.sort_values("total_cost_per_activated_inr").index[0]
print(f"\nLowest total cost per activated student: {best}")

# ---------- 3. Referral loop (viral coefficient) ----------
signed = ev[ev.signed_up==1]
k = ev.referred_by.notna().sum() / max(len(signed),1)
print(f"\nReferral K-factor (referred sign-ups per sign-up): {k:.2f}")

# ---------- 4. Cohort completion by reach-week ----------
c = ev[ev.signed_up==1].copy()
c["completed_within"] = c.weeks_to_complete
cohort = pd.DataFrame({f"within_{w}w_%": c.groupby("reached_week").apply(
        lambda g, w=w: 100*((g.weeks_to_complete<=w)).sum()/len(g), include_groups=False) for w in [1,2,3]}).round(1)
print("\n== Cohort: % of signed-up students completing within N weeks ==\n", cohort.to_string())
cohort.to_csv("outputs/cohort_completion.csv")

# ---------- Charts ----------
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
f[["reached","signed_up","applied","completed"]].T.plot.bar(ax=ax[0]); ax[0].set_title("Funnel by channel"); ax[0].tick_params(axis='x', rotation=0)
f["total_cost_per_activated_inr"].sort_values().plot.barh(ax=ax[1], color="#2a6f97"); ax[1].set_title("Cost per activated student (Rs)")
cohort.plot.bar(ax=ax[2]); ax[2].set_title("Cohort completion by week reached"); ax[2].set_xlabel("reach week"); ax[2].tick_params(axis='x', rotation=0)
plt.tight_layout(); plt.savefig("outputs/student_funnel.png", dpi=150)
