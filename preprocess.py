import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# load dataset
df = pd.read_csv("data/raw/original_dataset.csv")

# create folder for plots
os.makedirs("outputs/plots", exist_ok=True)

plt.figure(figsize=(10,6))

for column in df.columns[:-1]:
    sns.kdeplot(df[column], label=column)

plt.legend()
plt.title("Feature Distributions (Original Data)")

plt.savefig("outputs/plots/feature_distribution.png")

print("Distribution plot saved.")