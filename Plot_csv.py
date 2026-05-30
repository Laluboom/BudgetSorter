import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("Revolut_Sep_to_Jan.csv", parse_dates=["Started Date", "Completed Date"])

total_spent = df["Amount"].sum()
print(f"Total Spent: £{total_spent:.2f}")

# Spending breakdown by Type
spending_by_type = df.groupby("Type")["Amount"].sum()
print("\nSpending Breakdown by Type:")
print(spending_by_type)

# Spending breakdown by Description
spending_by_desc = df.groupby("Description")["Amount"].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Expenses by Description:")
print(spending_by_desc)

# Fees Analysis
total_fees = df["Fee"].sum()
print(f"\nTotal Fees Paid: £{total_fees:.2f}")

### 2. Time-Based Analysis ###
# Monthly Spending Trends
df["Month"] = df["Started Date"].dt.to_period("M")
monthly_spending = df.groupby("Month")["Amount"].sum()

# Plot Monthly Spending
plt.figure(figsize=(10, 5))
monthly_spending.plot(kind="bar", color="skyblue")
plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Total Amount Spent (£)")
plt.xticks(rotation=45)
plt.show()

# Daily Average Spending
daily_avg_spending = df.groupby(df["Started Date"].dt.date)["Amount"].sum().mean()
print(f"\nAverage Daily Spending: £{daily_avg_spending:.2f}")

# Weekly Spending Trends
df["Week"] = df["Started Date"].dt.to_period("W")
weekly_spending = df.groupby("Week")["Amount"].sum()

# Plot Weekly Spending
plt.figure(figsize=(10, 5))
weekly_spending.plot(kind="line", marker="o", color="green")
plt.title("Weekly Spending Trend")
plt.xlabel("Week")
plt.ylabel("Total Amount Spent (£)")
plt.grid()
plt.show()

### Combination: Most Expensive Categories Over Time ###
df["Year-Month"] = df["Started Date"].dt.to_period("M")
category_trends = df.groupby(["Year-Month", "Type"])["Amount"].sum().unstack().fillna(0)

# Plot category trends
category_trends.plot(kind="line", figsize=(12, 6), marker="o")
plt.title("Spending Trends by Category Over Time")
plt.xlabel("Month")
plt.ylabel("Total Amount Spent (£)")
plt.legend(title="Category")
plt.grid()
plt.show()
