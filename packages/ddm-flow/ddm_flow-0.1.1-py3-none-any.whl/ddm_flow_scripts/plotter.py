import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def get_conditions(filter_dir):
    """Map original folder names to cleaned-up condition names."""
    condition_folders = os.listdir(filter_dir)
    return {
        folder: folder.rsplit('-', 1)[0]
        for folder in condition_folders
        if os.path.isdir(os.path.join(filter_dir, folder))
    }


def process_condition_data(filter_dir, conditions):
    """Process data from CSV files for each condition."""
    data = {}
    for folder, condition in conditions.items():
        condition_path = os.path.join(filter_dir, folder)
        if not os.path.isdir(condition_path):
            continue

        for csv_file in os.listdir(condition_path):
            if csv_file.endswith(".csv"):
                filter_num = int(csv_file.split('-')[-1][1])
                csv_path = os.path.join(condition_path, csv_file)
                df = pd.read_csv(csv_path)

                avg_row_index = df[df.iloc[:, 0] == "FoV Averages:"].index[0]
                averages = df.iloc[avg_row_index + 1]

                if condition not in data:
                    data[condition] = {}
                data[condition][filter_num] = averages
    return data


def plot_data(filter_dir, data):
    """Plot the data for each condition and save the figure."""
    conditions = sorted(data.keys())
    filters = sorted(set([f for condition in data.values() for f in condition.keys()]))
    x = range(len(conditions))

    fig, ax = plt.subplots()
    for f in filters:
        for i, condition in enumerate(conditions):
            y_values = data[condition][f].astype(float).tolist()
            x_values = [i] * len(y_values)
            ax.scatter(x_values, y_values, color="purple", label=f'Filter {f}' if condition == conditions[0] else "", alpha=0.7)

    ax.axhspan(0, 30, facecolor='0.5', alpha=0.2)
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title('Average values for 9 FoVs (Suspected PCD: 11-23-115-XX)')
    ax.set_xticks(range(len(conditions)))
    ax.set_xticklabels(conditions, rotation=45)
    ax.legend()

    plt.tight_layout()
    fig.savefig(os.path.join(filter_dir, "averages_plot.png"))
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Plot data for individual filters.")
    parser.add_argument("filter_dir", help="Directory where a specific filter's folders are located.")
    args = parser.parse_args()

    conditions = get_conditions(args.filter_dir)
    data = process_condition_data(args.filter_dir, conditions)
    plot_data(args.filter_dir, data)


if __name__ == "__main__":
    main()
