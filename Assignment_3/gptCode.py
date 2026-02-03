"""
Housing Price Prediction with Linear Regression
------------------------------------------------
This program:
1) Loads housing data from a CSV file (Size and Price)
2) Prints summary statistics
3) Visualizes the data (scatter plot)
4) Trains a Linear Regression model (scikit-learn)
5) Prints coefficient, intercept, and R^2 score
6) Visualizes model fit (scatter + regression line)
7) Prompts the user for a house size and predicts price
8) Handles errors (file missing, empty file, bad input, etc.)

Run:
    python housing_price_predictor.py

Files:
    housing_data.csv (auto-created if missing/empty)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


CSV_PATH = Path(__file__).with_name("housing_data.csv")


SAMPLE_CSV_TEXT = """Size,Price
750,152000
820,165000
900,178000
980,191000
1050,205000
1120,218000
1200,232000
1280,247000
1350,259000
1420,272000
1500,286000
1580,300000
1650,313000
1720,327000
1800,342000
1950,369000
2100,396000
2250,424000
2400,452000
2550,481000
2700,510000
2850,539000
3000,568000
"""


def ensure_csv_exists(csv_path: Path) -> None:
    """Create a valid CSV if missing or empty."""
    if not csv_path.exists():
        print(f"[INFO] CSV not found. Creating sample dataset at: {csv_path}")
        csv_path.write_text(SAMPLE_CSV_TEXT, encoding="utf-8")
        return

    # If file exists but is empty (or basically empty)
    if csv_path.stat().st_size < 10:
        print(f"[INFO] CSV is empty or invalid. Rewriting sample dataset at: {csv_path}")
        csv_path.write_text(SAMPLE_CSV_TEXT, encoding="utf-8")


def load_data(csv_path: Path) -> pd.DataFrame:
    """Load housing dataset and validate required columns."""
    ensure_csv_exists(csv_path)

    # Debug print so you know EXACTLY what file is being read
    print("\n=== CSV DEBUG ===")
    print("Reading CSV from:", csv_path.resolve())
    print("File exists?:", csv_path.exists())
    print("File size (bytes):", csv_path.stat().st_size)
    try:
        preview = csv_path.read_text(encoding="utf-8", errors="replace").splitlines()[:3]
        print("First lines:", preview)
    except Exception as e:
        print("Could not preview file text:", e)
    print("=================\n")

    try:
        # utf-8-sig handles BOM weirdness
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
    except Exception as e:
        raise RuntimeError(f"ERROR: Failed to read CSV. Details: {e}")

    required = {"Size", "Price"}
    if not required.issubset(df.columns):
        raise ValueError(f"ERROR: CSV must contain columns {sorted(required)}. Found: {list(df.columns)}")

    # Convert to numeric, drop bad rows
    df = df.copy()
    df["Size"] = pd.to_numeric(df["Size"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["Size", "Price"])

    if len(df) < 20:
        raise ValueError(f"ERROR: Dataset must have at least 20 valid rows. Found {len(df)}")

    if (df["Size"] <= 0).any() or (df["Price"] <= 0).any():
        raise ValueError("ERROR: Size and Price must be positive.")

    return df


def show_basic_stats(df: pd.DataFrame) -> None:
    print("=== BASIC STATISTICS ===")
    print(df[["Size", "Price"]].describe())
    print()


def plot_scatter(df: pd.DataFrame) -> None:
    plt.figure()
    plt.scatter(df["Size"], df["Price"])
    plt.title("House Size vs Price")
    plt.xlabel("Size (sqft)")
    plt.ylabel("Price ($)")
    plt.grid(True)
    plt.show()


def train_model(df: pd.DataFrame) -> tuple[LinearRegression, float]:
    X = df[["Size"]].values
    y = df["Price"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    return model, r2


def print_model_info(model: LinearRegression, r2: float) -> None:
    slope = float(model.coef_[0])
    intercept = float(model.intercept_)

    print("=== MODEL RESULTS ===")
    print(f"Coefficient (slope):  {slope:,.4f} $ per sqft")
    print(f"Intercept:            {intercept:,.2f} $")
    print(f"R^2 score (test set): {r2:.4f}")
    print()


def plot_model_fit(df: pd.DataFrame, model: LinearRegression) -> None:
    X = df[["Size"]].values
    y = df["Price"].values

    x_line = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
    y_line = model.predict(x_line)

    plt.figure()
    plt.scatter(X, y)
    plt.plot(x_line, y_line)
    plt.title("Linear Regression Fit: Size vs Price")
    plt.xlabel("Size (sqft)")
    plt.ylabel("Price ($)")
    plt.grid(True)
    plt.show()


def get_user_size() -> float | None:
    while True:
        raw = input("Enter a house size in sqft (or 'q' to quit): ").strip().lower()
        if raw in {"q", "quit", "exit"}:
            return None
        try:
            size = float(raw)
            if size <= 0:
                print("Size must be positive. Try again.")
                continue
            return size
        except ValueError:
            print("Invalid input. Enter a number like 1500 or type 'q'.")


def predict_price(model: LinearRegression, size_sqft: float) -> float:
    return float(model.predict(np.array([[size_sqft]], dtype=float))[0])


def main() -> None:
    try:
        df = load_data(CSV_PATH)
    except Exception as e:
        print(e)
        sys.exit(1)

    show_basic_stats(df)
    plot_scatter(df)

    try:
        model, r2 = train_model(df)
    except Exception as e:
        print(f"ERROR: Model training failed. Details: {e}")
        sys.exit(1)

    print_model_info(model, r2)
    plot_model_fit(df, model)

    while True:
        size = get_user_size()
        if size is None:
            print("Goodbye.")
            break
        est_price = predict_price(model, size)
        print(f"Estimated price for {size:,.0f} sqft: ${est_price:,.2f}\n")


if __name__ == "__main__":
    main()
