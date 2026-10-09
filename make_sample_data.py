"""Generates SAMPLE (synthetic) survey + funnel data so the pipeline runs end-to-end.
REPLACE data/survey.csv and data/funnel_events.csv with your REAL Google Form export
and sign-up tracking before using any numbers on your resume."""
import numpy as np, pandas as pd
rng = np.random.default_rng(11)

# ---- survey ----
n = 120
survey = pd.DataFrame({
    "respondent": range(1, n+1),
    "year": rng.choice(["2nd","3rd","4th"], n, p=[.25,.4,.35]),
    "branch_group": rng.choice(["CSE/IT/ECE","Core Engg","Biotech/Chem","Other"], n, p=[.35,.3,.2,.15]),
    "internship_confidence_1to5": rng.integers(1, 6, n),
    "did_internship_before": rng.choice([0,1], n, p=[.6,.4]),
    "pain_point": rng.choice(["No real project experience","Don't know where to apply","Resume gets ignored","No mentor/guidance"], n, p=[.3,.25,.25,.2]),
    "would_try_free_sprint_1to5": rng.integers(1, 6, n),
    "preferred_channel": rng.choice(["WhatsApp","Instagram","LinkedIn","Club/Friends"], n, p=[.35,.2,.15,.3]),
})
survey.to_csv("data/survey.csv", index=False)

# ---- funnel events (one row per student reached) ----
channels = {"WhatsApp":(220,.34,.62,.55,.0), "Instagram":(180,.18,.55,.5,300), "LinkedIn":(120,.22,.6,.58,200), "Club/Referral":(90,.45,.68,.6,0)}
rows = []; sid = 0
for ch,(reach,p_sign,p_apply,p_comp,cost) in channels.items():
    for _ in range(reach):
        sid += 1
        week = int(rng.integers(1, 5))
        signup = rng.random() < p_sign
        applied = signup and rng.random() < p_apply
        completed = applied and rng.random() < p_comp
        weeks_to_complete = int(rng.integers(1, 4)) if completed else None
        rows.append(dict(student_id=sid, channel=ch, reached_week=week, signed_up=int(signup),
                         applied_sprint=int(applied), completed_sprint=int(completed),
                         weeks_to_complete=weeks_to_complete,
                         referred_by=int(rng.integers(1, sid)) if (signup and rng.random()<.18 and sid>1) else None))
pd.DataFrame(rows).to_csv("data/funnel_events.csv", index=False)
pd.DataFrame([{"channel":c,"spend_inr":v[4]} for c,v in channels.items()]).to_csv("data/channel_costs.csv", index=False)
