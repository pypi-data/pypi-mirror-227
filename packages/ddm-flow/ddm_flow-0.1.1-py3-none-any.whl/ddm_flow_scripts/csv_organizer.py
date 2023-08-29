import os
import shutil
import pandas as pd
import re
import argparse


def organize_csv(parent_dir):
    analysis_dir = os.path.join(parent_dir, 'analysis-individual-filter')
    if not os.path.exists(analysis_dir):
        os.makedirs(analysis_dir)

    for subdir, dirs, files in os.walk(parent_dir):
        if "OutputsDDM" in dirs:
            ddm_dir = os.path.join(subdir, "OutputsDDM")
            for file in os.listdir(ddm_dir):
                if file.endswith(".csv"):
                    file_path = os.path.join(ddm_dir, file)

                    match = re.search(r'F(\d+)', file)
                    if not match:
                        continue

                    F_number = 'F' + match.group(1)

                    F_folder = os.path.join(analysis_dir, F_number)
                    if not os.path.exists(F_folder):
                        os.makedirs(F_folder)

                    subfolder_name = os.path.basename(os.path.dirname(ddm_dir))
                    subfolder_path = os.path.join(F_folder, subfolder_name)
                    if not os.path.exists(subfolder_path):
                        os.makedirs(subfolder_path)

                    shutil.copy(file_path, subfolder_path)


def main():
    parser = argparse.ArgumentParser(description="Organize CSV files from a specified directory.")
    parser.add_argument("parent_dir", help="The path to the parent directory to organize.")
    args = parser.parse_args()

    organize_csv(args.parent_dir)


if __name__ == "__main__":
    main()