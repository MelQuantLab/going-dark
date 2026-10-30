# Going Dark: does knowing WHO is short help predict squeezes?
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# STEP 1: load the data
shorts = pd.read_csv("fca_short_positions.csv")
prices = pd.read_csv("prices.csv")

# STEP 2: crowding - how many funds are short, and how much in total
crowding = shorts.groupby(["Date", "Stock"]).agg(
    num_funds=("Fund", "count"),
    total_short=("Short %", "sum"),
).reset_index()

# STEP 3: did the price jump 20%+ over the next 20 trading days?
prices = prices.sort_values(["Stock", "Date"])
prices["future_price"] = prices.groupby("Stock")["Close"].shift(-20)
prices["future_return"] = prices["future_price"] / prices["Close"] - 1
prices["squeeze"] = prices["future_return"] > 0.20

data = crowding.merge(prices, on=["Date", "Stock"]).dropna()

# STEP 4: split by time - learn from the past, test on the future
train = data[data["Date"] < "2024-01-01"]
test = data[data["Date"] >= "2024-01-01"]

# STEP 5: two models - "old rules" vs "new rules"
def test_model(features):
    model = DecisionTreeClassifier(max_depth=3)
    model.fit(train[features], train["squeeze"])
    score = model.score(test[features], test["squeeze"])
    return score

named = test_model(["num_funds", "total_short"])
anonymous = test_model(["total_short"])

print("Old rules (we know the funds):", round(named * 100, 1), "%")
print("New rules (anonymous total):  ", round(anonymous * 100, 1), "%")
print("Accuracy lost:", round((named - anonymous) * 100, 1), "points")
