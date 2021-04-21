import datetime
import glob
import os
import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:.2f}'.format

if not os.path.exists('csv_files'):
    os.makedirs('csv_files')
else:
    print('Path exists')

# To do!?
# 1-> Math accuracy summing up journal number amounts
# 2-> Data Integrity Check
# 3-> B18 Benford's Law

processed_files = []
data_folder = "data"
files = os.listdir(data_folder)
ll = 0
for f in files:
    ll += 1
    if not os.path.exists(f'csv_files/{f[:10]}v{ll}.cvs'):
        print(f + " processed")
        data_frame = pd.read_excel(f"data/{f}", index_col=None)
        data_frame = data_frame[['Journal number', 'Date', 'Ledger account', 'Amount', 'Created date and time']]
        data_frame['Ledger account'] = data_frame['Ledger account'].str.slice(0, 6)
        data_frame.to_csv('csv_files/' + f[:10] + f"v{ll}.cvs", encoding='utf-8', index=False)
        processed_files.append(f'{f[:10]}v{ll}.cvs')
    else:
        processed_files = os.listdir('csv_files/')

if not os.path.exists('combined.csv'):
    # files = [f for f in os.listdir('csv_files') if re.match(r'.*\.cvs', f)]
    # combined_csv = pd.concat([pd.read_csv(f'csv_files/{processed_files}')], join='inner')
    combined_csv = pd.concat([pd.read_csv(f'csv_files/{f}') for f in processed_files])
    combined_csv.sort_values(['Ledger account'], ascending=True, inplace=True)
    combined_csv.to_csv("combined.csv", index=False, encoding='utf-8-sig')

trial_balance = pd.read_excel("Trial balance_CLFL 2020.xlsx", index_col=None)
combined_csv = pd.read_csv('combined.csv')
grp = combined_csv.groupby(['Ledger account'])
grp_jrnlnum = combined_csv.groupby(['Journal number'])

# for i, j in grp_jrnlnum:
#     if float(f"{j['Amount'].agg(np.sum):.2f}") != 0.00:
#         print(f"{i} This entries' sum is not equal to 0.00 -> {j}")
#     else:
#         print(f"{i} Entries are equal to 0.00")
#
# if float(f"{combined_csv['Amount'].agg(np.sum):.2f}") != 0.00:
#     print("Something is wrong with sum of all Amount entries")
#     print("Plese do manual testing of each entry")
# else:
#     print("All amounts are equal to 0.00")

# print(combined_csv[combined_csv.isnull().any(axis=1)])

print(isinstance(combined_csv['Date'], pd.DatetimeIndex, format()))
# combined_csv['date'] = pd.to_datetime(combined_csv['Date'], format="%Y-%m-%d %H:%M:%S")
# if datetime.datetime.strptime([f for f in combined_csv['Date']], format='%Y-%m-%d %H:%M:%S'):
#     print("OK")

# if pd.to_datetime(combined_csv['Date'], format='%Y-%m-%d %H:%M:%S', dayfirst=True, errors='coerce').notnull().all():
#     print("OK")
# else:
#     print("NO")

# debit_sum = []
# credit_sum = []
# closing_sum = []
# k = 0
# for i, j in grp:
#     k += 1
#     gt_debits = j[j['Amount'] > 0]
#     lt_credits = j[j['Amount'] < 0]
#     debit = float(f"{gt_debits['Amount'].agg(np.sum):.2f}")
#     credit = float(f"{lt_credits['Amount'].agg(np.sum):.2f}") * (-1)
#     debit_sum.append(debit)
#     credit_sum.append(credit)
#     closing_sum.append(float(f"{(debit - credit):.2f}"))
#
# trial_balance['GL Debits'] = debit_sum
# trial_balance['GL Credits'] = credit_sum
# trial_balance['GL Closing balance'] = closing_sum
# trial_balance['GL Difference'] = trial_balance['Closing balance'] - closing_sum
# trial_balance.to_csv("Result Trial balance_CLFL 2020.csv", index=False, encoding='utf-8-sig')
