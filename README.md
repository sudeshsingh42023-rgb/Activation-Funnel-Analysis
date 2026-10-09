# Student Acquisition & Activation Funnel (Campus-to-Corporate Platform)

**Goal:** Learn what students need, test which channels activate them cheaply, and produce a playbook to roll out to more campuses.

**Stack:** Google Forms, Python (pandas, matplotlib)

## Run
```
pip install pandas matplotlib
python make_sample_data.py   # SAMPLE data. Replace data/survey.csv, data/funnel_events.csv, data/channel_costs.csv with real data
python analysis.py           # personas, channel funnel, cost per activated student, K-factor, cohorts -> outputs/
```
Use `survey_questions.md` to build the Google Form and export responses as `data/survey.csv` (match the column names).

## funnel_events.csv columns
student_id, channel, reached_week, signed_up, applied_sprint, completed_sprint, weeks_to_complete, referred_by
(Track each channel with its own link/form so you know where every sign-up came from.)

## Method notes
- Personas: rule-based on interest in the free sprint, confidence, and prior internship.
- Cost per activated student = (cash spend + effort proxy at Rs 100/hr, 1 hr per 10 students reached) / students who completed. Change the proxy in analysis.py as you see fit.
- K-factor = referred sign-ups / total sign-ups.

## Resume entry (fill brackets with YOUR real numbers)
**Student Acquisition & Activation Funnel Analysis | Google Forms, Python, Pandas**
- Surveyed **[N]** students on internship-readiness blockers and segmented them into **[4]** personas, identifying **[top pain point]** as the key messaging hook.
- Ran a campus pilot across **[4]** channels (WhatsApp, Instagram, LinkedIn, clubs/referrals) and tracked reach -> sign-up -> sprint application -> completion; **[channel]** delivered the lowest cost per activated student at **Rs [X]** vs **Rs [Y]** for the weakest.
- Measured a referral K-factor of **[0.XX]**, built a weekly cohort-completion analysis, and wrote a 10-campus rollout playbook with ambassador and referral mechanics.
