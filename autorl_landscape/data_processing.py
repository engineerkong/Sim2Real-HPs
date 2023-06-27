import os
import pandas as pd
import numpy as np
import json

def search_files(folder_path, target_file_extension):
    target_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(target_file_extension):
                file_path = os.path.join(root, file)
                target_files.append(file_path)
    return target_files

def get_csv_path(model_path):
    parent_dir = os.path.dirname(model_path)
    csv_path = os.path.join(parent_dir,"data.csv")
    return csv_path    

folder_path = "../data/agents_reach_4-3_20k/"
target_file_extension = '.csv'
data_files = search_files(folder_path, target_file_extension)
df_list = []
for data_file in data_files:
    sim2real_gap = []
    df = pd.read_csv(data_file, index_col=0)
    iqm_sim = json.loads(df["iqm_sim"].iloc[0])
    iqm_real = json.loads(df["iqm_real"].iloc[0])
    for i in range(len(iqm_sim["iqm"])):
        gap = iqm_sim["iqm"][i] - iqm_real["iqm"][i]
        sim2real_gap.append(gap)
    sim2real_gap_str = json.dumps(sim2real_gap)
    new_column_df = pd.DataFrame({'sim2real_gap': sim2real_gap_str}, index=df.index)
    new_df = pd.concat([df, new_column_df], axis=1)
    df_list.append(new_df)
merged_df = pd.concat([df for df in df_list], axis=0)
# print(merged_df["ls.tau"].values)
merged_df.to_csv('../data/merged.csv', index=False)
df = pd.read_csv('../data/merged.csv')
print(type(df["ls_eval/returns"].values[0]))
