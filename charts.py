# Going Dark: charts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load the table we built in going_dark.py
data = pd.read_csv("going_dark_data.csv")

# CHART 1: one stock over time - price vs number of funds short
stock = data[data["Stock"] == "AAA"]
fig, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(stock["Date"], stock["Close"], color="navy")
ax1.set_ylabel("Share price")
ax2 = ax1.twinx()
ax2.bar(stock["Date"], stock["num_funds"], color="orange", alpha=0.4)
ax2.set_ylabel("Funds short")
ax1.set_xticks(ax1.get_xticks()[::50])
plt.title("AAA: share price vs number of funds short")
plt.savefig("chart1_stock.png")

# CHART 2: crowding map - how often does a squeeze follow?
table = data.pivot_table(index="num_funds",
                         columns=pd.cut(data["total_short"], bins=4),
                         values="squeeze", aggfunc="mean")
plt.figure(figsize=(8, 4))
sns.heatmap(table, annot=True, fmt=".0%", cmap="Reds")
plt.title("Squeeze rate by crowding")
plt.xlabel("Total % short")
plt.ylabel("Number of funds short")
plt.savefig("chart2_heatmap.png")

# CHART 3: old rules vs new rules
results = pd.DataFrame({
    "Rules": ["Named funds (old)", "Anonymous total (new)"],
    "Squeezes caught": [0.62, 0.41],   # replace with your real recall scores
})
plt.figure(figsize=(6, 4))
sns.barplot(data=results, x="Rules", y="Squeezes caught", hue="Rules", palette=["navy", "grey"])
plt.title("What the UK loses when shorts go anonymous")
plt.savefig("chart3_old_vs_new.png")

print("3 charts saved")
