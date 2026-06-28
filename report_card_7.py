import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from groq import Groq
import os

GROQ_KEY = os.environ.get("GROQ_KEY", "")

scores = pd.read_csv("evasion_scores.csv", index_col=0)
patient_id = scores.index[0]
patient = scores.loc[patient_id]

mechanisms = [
    "Checkpoint Upregulation",
    "MHC Downregulation",
    "T-cell Exclusion",
    "Immunosuppressive Cytokines",
    "Regulatory T-cell Recruitment"
]

plain_labels = {
    "Checkpoint Upregulation":       "Sending Don't Attack Me Signals",
    "MHC Downregulation":            "Hiding Tumor Identity",
    "T-cell Exclusion":              "Blocking Immune Cells",
    "Immunosuppressive Cytokines":   "Poisoning Immune Environment",
    "Regulatory T-cell Recruitment": "Recruiting Immune Suppressors"
}

icons = {
    "Checkpoint Upregulation":       "🚩",
    "MHC Downregulation":            "🎭",
    "T-cell Exclusion":              "🚧",
    "Immunosuppressive Cytokines":   "☁️",
    "Regulatory T-cell Recruitment": "🤝"
}

mech_scores = {m: round(float(patient[m]), 2)
               for m in mechanisms if m in patient.index}
overall = round(float(patient.get("Overall_Disguise_Score",
                np.mean(list(mech_scores.values())))), 2)

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#0f1117")
ax.set_facecolor("#1a1a2e")

mechs_list = list(mech_scores.keys())
values = [mech_scores[m] for m in mechs_list]
labels = [f"{icons[m]}  {plain_labels[m]}" for m in mechs_list]
colors = ["#e74c3c" if v >= 7 else "#f39c12" if v >= 4
          else "#2ecc71" for v in values]

bars = ax.barh(labels, values, color=colors, height=0.5)
for bar, val in zip(bars, values):
    ax.text(val+0.1, bar.get_y()+bar.get_height()/2,
            f"{val:.1f}", va="center", color="white", fontsize=10)

ax.set_xlim(0, 10)
ax.set_xlabel("Evasion Activity (0-10)", color="white")
ax.tick_params(colors="white")
plt.tight_layout()
plt.savefig(f"report_card_{patient_id[:12]}.png",
            dpi=150, facecolor="#0f1117")
plt.show()
print(f"Report card saved for {patient_id}")
print(f"Overall score: {overall}")