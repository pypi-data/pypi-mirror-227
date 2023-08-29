import pandas as pd
import os
import argparse


def read_and_aggregate_sheets(file_path):
    """Read specified sheets from an Excel file and aggregate them."""
    with pd.ExcelFile(file_path) as xls:
        all_sheet_names = xls.sheet_names

    sheets_to_read = [sheet for sheet in all_sheet_names if sheet.startswith("CBFfromDDMFile")]

    df = pd.DataFrame()

    for sheet in sheets_to_read:
        sheet_df = pd.read_excel(file_path, sheet_name=sheet, usecols="A", skiprows=0, nrows=12, names=[sheet])
        df = pd.concat([df, sheet_df], axis=1)

    return df


def save_aggregated_data(df, output_path):
    """Save the aggregated data with the FoV average to a CSV."""
    averages = df.mean()
    average_df = pd.DataFrame(columns=df.columns)
    average_df.loc[0] = ["FoV Averages:"] + [None] * (len(df.columns) - 1)
    average_df.loc[1] = averages.values

    df = pd.concat([df, average_df], ignore_index=True)
    df.to_csv(output_path, index=False)


def aggregate_multisheets(parent_dir, output_name_prefix):
    """Aggregate data from multiple sheets in Excel files in the specified directory."""
    for subdir, dirs, files in os.walk(parent_dir):
        if "OutputsDDM" in dirs:
            ddm_dir = os.path.join(subdir, "OutputsDDM")

            for file in [f for f in os.listdir(ddm_dir) if f.endswith(".xlsx")]:
                file_path = os.path.join(ddm_dir, file)

                df = read_and_aggregate_sheets(file_path)

                base_name = os.path.splitext(os.path.basename(file_path))[0]
                base_name = base_name.replace("DDMOutputsSummary", "").replace("-00_", "")
                output_csv = os.path.join(ddm_dir, output_name_prefix + base_name + ".csv")

                save_aggregated_data(df, output_csv)

                print(f"Processed {file_path} and saved to {output_csv}")


def main():
    """Entry point of the script."""
    parser = argparse.ArgumentParser(description="Aggregate multiple Excel sheets from a directory.")
    parser.add_argument('directory', type=str, help='The parent directory containing Excel files to process')
    parser.add_argument('-o', '--output', type=str, default="Filter-FoV-Average",
                        help='Prefix for the output CSV file name')

    args = parser.parse_args()

    if os.path.exists(args.directory) and os.path.isdir(args.directory):
        aggregate_multisheets(args.directory, args.output)
    else:
        print(f"Error: Directory {args.directory} does not exist or is not a directory.")


if __name__ == "__main__":
    main()


