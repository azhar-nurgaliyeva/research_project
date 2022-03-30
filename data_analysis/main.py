import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_leakages = pd.read_csv('C:/Users/aznur/PycharmProjects/research_project/2018_Leakages.csv', decimal=',', sep=';',
                          index_col='Timestamp')
df_leakages_1 = pd.read_csv('C:/Users/aznur/PycharmProjects/research_project/2019_Leakages.csv', decimal=',', sep=';',
                          index_col='Timestamp')

# Dataframe with both 2018 and 2019 leakages
result = pd.concat([df_leakages, df_leakages_1], axis=0)
result = result.fillna(0)

df_pressures = pd.read_csv('C:/Users/aznur/PycharmProjects/research_project/2018_SCADA_Pressures.csv', decimal=',',
                           sep=';', index_col='Timestamp')

df_flows = pd.read_csv('C:/Users/aznur/PycharmProjects/research_project/2018_SCADA_Flows.csv', decimal=',',
                           sep=';', index_col='Timestamp')

df_demands = pd.read_csv('C:/Users/aznur/PycharmProjects/research_project/2018_SCADA_Demands.csv', decimal=',',
                           sep=';', index_col='Timestamp')

df_columns_pressures = list(df_pressures.columns.values)
columns_new = []

for i in df_columns_pressures:
    if i in list(df_demands.columns.values):
        columns_new.insert(len(columns_new)+1, i)

df_columns_pressures = columns_new
df_demands_new = df_demands[df_columns_pressures[2]]
df_pressures_new = df_pressures[df_columns_pressures]

fig = plt.figure(figsize=(16,8),dpi=300)
df_demands_new.plot(ax=plt.gca())
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0)
plt.savefig('C:/Users/aznur/PycharmProjects/research_project/analysis/2018_demands_pressure_n31.png')
plt.show()

# fig = plt.figure(figsize=(16,8),dpi=300)
# result.plot(ax=plt.gca())
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0)
# plt.savefig('C:/Users/aznur/PycharmProjects/research_project/analysis/2018_and_2019_leakages.png')
# plt.show()

# fig = plt.figure(figsize=(16,8),dpi=300)
# df_pressures.plot(ax=plt.gca())
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0)
# plt.savefig('C:/Users/aznur/PycharmProjects/research_project/analysis/2018_pressures.png')
# plt.show()

# fig = plt.figure(figsize=(16,8),dpi=300)
# df_demands.plot(ax=plt.gca())
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0)
# plt.savefig('C:/Users/aznur/PycharmProjects/research_project/analysis/2018_demands.png')
# plt.show()

# fig = plt.figure(figsize=(16,8),dpi=300)
# df_flows.plot(ax=plt.gca())
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0)
# plt.savefig('C:/Users/aznur/PycharmProjects/research_project/analysis/2018_flows.png')
# plt.show()


