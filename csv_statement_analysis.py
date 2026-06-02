import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression # type: ignore
import numpy as np
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
df = pd.read_csv("Revolut_Sep_to_Jan.csv", parse_dates=["Started Date", "Completed Date"])

# Convert "Amount" to absolute values
df["Amount"] = df["Amount"].abs()

# Ignore Money Transfers from Friends
exclude_keywords = ["transfer", "friend", "reimbursement", "split", "payback"]
df = df[~df["Description"].str.contains("|".join(exclude_keywords), case=False, na=False)]

### Monthly Spending Trends ###
df["Month"] = df["Started Date"].dt.to_period("M")
monthly_spending = df.groupby("Month")["Amount"].sum()

# Predict Next 3 Months' Spending (Simple Linear Regression)
X = np.array(range(len(monthly_spending))).reshape(-1, 1)  # Time as numeric values
y = monthly_spending.values  # Spending amounts

model = LinearRegression()
model.fit(X, y)

# Predict next 3 months
future_X = np.array(range(len(monthly_spending), len(monthly_spending) + 3)).reshape(-1, 1)
future_predictions = model.predict(future_X)

# Print Budget Predictions
future_months = pd.date_range(start=monthly_spending.index[-1].to_timestamp(), periods=3, freq="M").to_period("M")
for month, amount in zip(future_months, future_predictions):
    print(f"Predicted Spending for {month}: £{amount:.2f}")

def total_spending_per_month(df):
    """Calculate total spending per month based on Description."""
    df_copy = df.copy()
    df_copy["Month"] = df_copy["Started Date"].dt.to_period("M")
    return df_copy.groupby(["Month", "Description"])["Amount"].sum().unstack(fill_value=0)

def total_spending_per_week(df):
    """Calculate total spending per week based on Description."""
    df_copy = df.copy()
    df_copy["Week"] = df_copy["Started Date"].dt.to_period("W")
    return df_copy.groupby(["Week", "Description"])["Amount"].sum().unstack(fill_value=0)

def average_spending_per_category(df):
    """Calculate average spending per Description category."""
    df_copy = df.copy()
    return df_copy.groupby("Description")["Amount"].mean().sort_values(ascending=False)

# Call the functions and print results
monthly_spending = total_spending_per_month(df)
weekly_spending = total_spending_per_week(df)
average_spending = average_spending_per_category(df)

print("Total Spending per Month:\n", monthly_spending)
print("\nTotal Spending per Week:\n", weekly_spending)
print("\nAverage Spending per Category:\n", average_spending)

# Plot Actual vs Predicted Spending
plt.figure(figsize=(10, 5))
plt.plot(pd.Series(monthly_spending.index).astype(str), y, marker="o", label="Actual Spending")
plt.plot(future_months.astype(str), future_predictions, marker="x", linestyle="dashed", color="red", label="Predicted Spending")
plt.title("Spending Trends & Prediction")
plt.xlabel("Month")
plt.ylabel("Total Amount Spent (£)")
plt.legend()
plt.xticks(rotation=45)
plt.show()

# AI code to run when needed
def run_ai_model(prompt: str) -> str:
    API_KEY = os.getenv("GeminiAPI")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro") 
    response = model.generate_content(prompt)
    return response.text
