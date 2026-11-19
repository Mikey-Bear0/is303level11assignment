# Michael Cunningham
# Level 11 Assignment: Catalog manager
# 11/18/26

from pathlib import Path

import pandas as pd

# Designating the proper file path for da CSV
RAW_FILE = Path(__file__).with_name("video_games_raw.csv")
CLEANED_FILE = Path(__file__).with_name("video_games_cleaned.csv")
VALID_STATUSES = {"Backlog", "Playing", "Completed", "Dropped"}


def main():
    # Run the interactive catalog update.
    games = pd.read_csv(RAW_FILE)

    # Announcing presence/how many catalog games there are
    print("VIDEO GAME CATALOG MANAGER")
    print(f"There are {len(games)} games in the catalog.")

    # Loop to run through while the user looks through the catalog
    while True:
        try:
            row_number = int(
                input(f"Enter a row number to inspect (0-{len(games) - 1}): ")
            )
        # ValueError to indicate "hey pal, wrong input"
        except ValueError:
            print("Please enter a whole number.")
            continue
        
        # Check if the row number is valid
        if 0 <= row_number < len(games):
            break
        print(f"Choose a row number from 0 to {len(games) - 1}.")

    # .iloc[] to access a row by its position in the DataFrame
    selected_game = games.iloc[row_number]
    print("\nSelected Game:")
    print(selected_game.to_string())

    # Loop to get a valid new status from the user
    while True:
        new_status = input(
            "\nEnter a new status (Backlog, Playing, Completed, or Dropped): "
        ).strip().title()
        if new_status in VALID_STATUSES:
            break
        print("Enter Backlog, Playing, Completed, or Dropped.")

    # .at[] changes the Status value for this one selected row
    games.at[selected_game.name, "Status"] = new_status

    # Start with No, then use .loc[] to mark every qualifying game Yes
    games["Recommended"] = "No"
    meets_recommendation_criteria = (
        (pd.to_numeric(games["Rating"], errors="coerce") >= 8)
        & (pd.to_numeric(games["Price"], errors="coerce") <= 40)
    )
    games.loc[meets_recommendation_criteria, "Recommended"] = "Yes"

    # .query[] filters the DataFrame to show only recommended games
    recommended_games = games.query('Recommended == "Yes"')
    print("\nRecommended Games:")
    if recommended_games.empty:
        print("No games meet both recommendation criteria.")
    else:
        print(recommended_games[["Title", "Platform", "Price", "Rating"]].to_string())

    # Save to a new file so video_games_raw.csv stays unchanged
    games.to_csv(CLEANED_FILE, index=False)
    print(f"\nThe catalog has been updated and saved as {CLEANED_FILE.name}.")


if __name__ == "__main__":
    main()
