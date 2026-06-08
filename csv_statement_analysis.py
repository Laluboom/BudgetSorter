import os

import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sklearn.linear_model import LinearRegression  # type: ignore

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


def load_statement_data(csv_path="Revolut_Sep_to_Jan.csv"):
    df = pd.read_csv(csv_path, parse_dates=["Started Date", "Completed Date"])
    df["Amount"] = df["Amount"].abs()

    exclude_keywords = ["transfer", "friend", "reimbursement", "split", "payback"]
    return df[
        ~df["Description"].str.contains("|".join(exclude_keywords), case=False, na=False)
    ]


def predict_future_spending(df):
    monthly_spending = df.copy()
    monthly_spending["Month"] = monthly_spending["Started Date"].dt.to_period("M")
    monthly_totals = monthly_spending.groupby("Month")["Amount"].sum()

    X = np.array(range(len(monthly_totals))).reshape(-1, 1)
    y = monthly_totals.values

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.array(
        range(len(monthly_totals), len(monthly_totals) + 3)
    ).reshape(-1, 1)
    future_predictions = model.predict(future_X)
    future_months = pd.date_range(
        start=monthly_totals.index[-1].to_timestamp(), periods=3, freq="M"
    ).to_period("M")

    return monthly_totals, y, future_months, future_predictions


def plot_spending_trends(monthly_spending, y, future_months, future_predictions):
    plt.figure(figsize=(10, 5))
    plt.plot(
        pd.Series(monthly_spending.index).astype(str),
        y,
        marker="o",
        label="Actual Spending",
    )
    plt.plot(
        future_months.astype(str),
        future_predictions,
        marker="x",
        linestyle="dashed",
        color="red",
        label="Predicted Spending",
    )
    plt.title("Spending Trends & Prediction")
    plt.xlabel("Month")
    plt.ylabel("Total Amount Spent (£)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()


def main():
    load_dotenv()
    df = load_statement_data()
    monthly_spending, y, future_months, future_predictions = predict_future_spending(df)

    for month, amount in zip(future_months, future_predictions):
        print(f"Predicted Spending for {month}: £{amount:.2f}")

    monthly_breakdown = total_spending_per_month(df)
    weekly_spending = total_spending_per_week(df)
    average_spending = average_spending_per_category(df)

    print("Total Spending per Month:\n", monthly_breakdown)
    print("\nTotal Spending per Week:\n", weekly_spending)
    print("\nAverage Spending per Category:\n", average_spending)

    plot_spending_trends(monthly_spending, y, future_months, future_predictions)

# AI code to run when needed
def run_ai_model(prompt: str) -> str:
    API_KEY = os.getenv("GeminiAPI")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro") 
    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    main()
