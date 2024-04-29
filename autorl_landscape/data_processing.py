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

folder_path = "/home/lingxiao/Desktop/evaluating_models/gym_sac_hps/"
target_file_extension = '.csv'
data_files = search_files(folder_path, target_file_extension)
df_list = []
data = []
for data_file in data_files:
    df = pd.read_csv(data_file, index_col=0)
    sim = json.loads(df["sim"].iloc[0])
    data.append(sim["iqm"])
data = np.array(data)
mean = data.mean()
std = data.std()

for data_file in data_files:
    sim2real_gap = []
    df = pd.read_csv(data_file, index_col=0)
    sim = json.loads(df["sim"].iloc[0])
    real = json.loads(df["real"].iloc[0])
    for i in range(len(sim["iqm"])):
        gap = sim["iqm"][i] - real["iqm"][i]
        sim2real_gap.append(gap)
    normalized_iqm = list((sim["iqm"] - mean)/std)
    sim_len = sim["len"]
    sim_iqm_str = json.dumps(normalized_iqm)
    sim_len_str = json.dumps(sim_len)
    sim2real_gap_str = json.dumps(sim2real_gap)
    new_column_df1 = pd.DataFrame({'sim_iqm': sim_iqm_str}, index=df.index)
    new_column_df2 = pd.DataFrame({'sim_len': sim_len_str}, index=df.index)
    new_column_df3 = pd.DataFrame({'sim2real_gap': sim2real_gap_str}, index=df.index)
    new_df = pd.concat([df, new_column_df1, new_column_df2, new_column_df3], axis=1)
    df_list.append(new_df)
merged_df = pd.concat([df for df in df_list], axis=0)
# print(merged_df["ls.tau"].values)
merged_df.to_csv('/home/lingxiao/Desktop/evaluating_models/merged.csv', index=False)
df = pd.read_csv('/home/lingxiao/Desktop/evaluating_models/merged.csv')
print(type(df["ls_eval/returns"].values[0]))
