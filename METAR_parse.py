from metpy.io import parse_metar_to_dataframe
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def METAR_parse_ogimet(filename):
    date_length = 22
    METAR_df = pd.DataFrame()
    error_report = []
    with open(filename, 'r') as file:
        num_lines = len(file.readlines())
    with open(filename, 'r') as file:
        for line in tqdm(file, total = num_lines, desc="METARS processed"):
            try:
                line = line.strip()
                date = line[:date_length-1]
                METAR = line[date_length:]
                year = date[5:9]
                month = date[10:12]
                data = parse_metar_to_dataframe(METAR, month = int(month), year = int(year))
                METAR_df = pd.concat([METAR_df,     data], axis = 0)
            except KeyError as e:
                error_report.append(f"Skipping {line} due to {e}")
                continue
    METAR_df = METAR_df.reset_index(drop=True)
    print(METAR_df)
    METAR_df.to_csv(f"{filename}.csv", index=False)
    if error_report:
        print("\n---------------------------- Error Report ---------------------------------------------")
        for error in error_report:
            print(error)
        print("---------------------------------------------------------------------------------------")    
    else:
        print("No errors occurred.")
    return

METAR_parse_ogimet('metar_LBSF_2005-01-01_2024-12-31.txt')