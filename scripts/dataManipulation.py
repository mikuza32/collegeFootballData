import os
import json

import matplotlib.pyplot as plt
import pandas as pd

class dataManipulation:

    def __init__ (self, data_dir, output_dir):
        self.data_dir = data_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def loadData(self, week):
        filePath = os.path.join(self.data_dir, f'week{week}.json')
        try:
            with open(filePath, 'r') as jsonFile:
                data = json.load(jsonFile)
                print(f"Loaded data for {week}")
                return data
        except FileNotFoundError:
            print("Could not retrieve data file {week}")
            return None

    def dataCharts(self, metrics, week):
        # Extract the offensive and defensive metrics from the designated week
        offensiveData = metrics['offense']
        defensiveData = metrics['defense']

        # Prints a verification to show that the particular data for each week has been retrieved and manipulated
        print(f"Offensive Data for Week {week}: {offensiveData}")
        print(f"Defensive Data for Week {week}: {defensiveData}")

        #
        offensive_series = pd.Series(offensiveData).apply(pd.to_numeric, errors='coerce').dropna()
        defensive_series = pd.Series(defensiveData).apply(pd.to_numeric, errors='coerce').dropna()

        figures, axes = plt.subplots(2, 2, figsize=(10, 10))
        figures.suptitle(f'Week {week} Colorado Football Data Charts', fontsize=20)

        offensive_series.plot(kind='bar', ax=axes[0, 0])
        axes[0, 0].set_title('Colorado Football Team Offensive Metrics')
        axes[0, 0].set_ylabel('Values')

        defensive_series.plot(kind='bar', ax=axes[0, 1])
        axes[0, 1].set_title('Colorado Football Team Defensive Metrics')
        axes[0, 1].set_ylabel('Values')

        combinedDataFrame = pd.DataFrame({'Offense': offensive_series, 'Defense': defensive_series})
        combinedDataFrame.plot(kind='line', marker='o', ax=axes[1, 0])
        axes[1, 0].set_title('Colorado Football Offensive vs. Defensive Statistics Comparison')
        axes[1, 0].set_xlabel('Metrics')
        axes[1, 0].set_ylabel('Values')

        if 'Total Yards' in offensiveData and 'Total Yards Allowed' in defensiveData:
            total_yards = pd.to_numeric(offensiveData['Total Yards'], errors='coerce')
            yards_allowed = pd.to_numeric(defensiveData['Total Yards Allowed'], errors='coerce')
            axes[1, 1].scatter(total_yards, yards_allowed)
            axes[1, 1].set_title('Total Yards vs Total Yards Allowed')
            axes[1, 1].set_xlabel('Total Yards Gained')
            axes[1, 1].set_ylabel('Total Yards Allowed')
            axes[1, 1].grid(True)

        # Save the figure
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        filePath = os.path.join(self.output_dir, f'week_{week}_charts.png')
        plt.savefig(filePath, dpi=300)
        print(f'Saved all charts and graphs for week {week} to {filePath}')
        plt.close()

    def showAllWeeksData(self):
        for week in range (1, 9):
            metrics = self.loadData(week)
            if metrics:
                print(f"Showing all offensive and defensive data for {week}")
                self.dataCharts(metrics, week)

if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../reports')

    # Initialize the visualizer with directories
    displayData = dataManipulation(DATA_DIR, OUTPUT_DIR)

    # Run the visualization process for all weeks
    displayData.showAllWeeksData()