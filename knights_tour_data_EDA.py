import sqlite3
import pandas as pd

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)

def run_analysis():
    conn = sqlite3.connect('knights_tour_results.db')
    # read the simulation table into a DataFrame
    df = pd.read_sql_query("SELECT * FROM simulations WHERE board_length = "
                           "128",
                           conn)
    # testing basic functionality with head()
    print(df)

    # Testing row count for the 8x8 board
    # dimensions should match the DIM param in the agent
    count_8x8 = len(df[(df['board_length'] == 8) & (df['board_width'] == 8)])
    print(f"\nTotal runs for 8x8 board: {count_8x8}")

    # qick aggregate success rate
    # 'solved' is a boolean metric captured by the agent during the tour
    print("\n--- Success Rate by Depth (k) ---")
    print(df.groupby('k_depth')['solved'].mean())

    conn.close()


if __name__ == "__main__":
    run_analysis()