from pathlib import Path
import matplotlib.pyplot as plot
import pandas

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

DATA_FILE = "housing_data.csv"

#Load housing data from CSV file
def load_data(filename):
    try: 
        df = pandas.read_csv(filename)
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return None
    
    if "Size" not in df.columns or "Price" not in df.columns:
        print("Error: CSV is in the wrong format.")
        return
    
    return df

#Show basic statistics of dataset
def show_stats(df):
    print("\nBasic statistics:")
    print(df.describe())

#Size vs Price Graph
def plot_data(df):
    plot.scatter(df["Size"], df["Price"])
    plot.xlabel("House Size (sqft)")
    plot.ylabel("House Price ($usd)")
    plot.title("House Size vs Price")
    plot.grid(True)
    plot.show()

def ml_training(df):
    x = df[["Size"]]
    y = df["Price"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    r2 = r2_score(y_test, predictions)

    return model, r2

def show_model_results(model, r2):
    print("\nModel results:")
    print(f"Slope (price per sqft): {model.coef_[0]:.2f}")
    print(f"Intercept: {model.intercept_:.2f}")
    print(f"R^2 score: {r2:.4f}")

def main():
    df = load_data(DATA_FILE)

    if df is None:
        print("Failed to load data.")
        return
    
    print("Data loaded successfully.\n")
    print("First 5 rows:")
    print(df.head())

    show_stats(df)
    plot_data(df)

    model, r2 = ml_training(df)
    show_model_results(model, r2)
    
if __name__ == "__main__":
    main()
