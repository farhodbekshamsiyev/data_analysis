import os
import re
from datetime import time, date, timedelta

import numpy as np
import pandas as pd
import holidays

from utils import *


def completness_check(file_name):
    trial_balance = pd.read_excel("Trial balance_CLFL 2020.xlsx", index_col=None)
    combined_csv = pd.read_csv(file_name)
    grp = combined_csv.groupby(['Ledger account'])
    debit_sum = []
    credit_sum = []
    closing_sum = []
    k = 0
    for i, j in grp:
        k += 1
        gt_debits = j[j['Amount'] > 0]
        lt_credits = j[j['Amount'] < 0]
        debit = float(f"{gt_debits['Amount'].agg(np.sum):.2f}")
        credit = float(f"{lt_credits['Amount'].agg(np.sum):.2f}") * (-1)
        debit_sum.append(debit)
        credit_sum.append(credit)
        closing_sum.append(float(f"{(debit - credit):.2f}"))

    trial_balance['GL Debits'] = debit_sum
    trial_balance['GL Credits'] = credit_sum
    trial_balance['GL Closing balance'] = closing_sum
    trial_balance['GL Difference'] = trial_balance['Closing balance'] - closing_sum
    # print(trial_balance[trial_balance['GL Difference'].equals(0.00)])
    trial_balance.to_csv("Result Trial balance_CLFL 2020.csv", index=False, encoding='utf-8-sig')


def math_accuracy(dataframe):
    equal_journal_nums = False
    dataframe = dataframe[['Journal number', 'Amount']]
    grp_jrnlnum = dataframe.groupby(['Journal number'])
    for i, j in grp_jrnlnum:
        if float(f"{j['Amount'].agg(np.sum):.2f}") != 0.00:
            print(f"{i} This entries' sum is not equal to 0.00 -> {j}")
            equal_journal_nums = True
        # else:
        #     print(f"{i} Entries are equal to 0.00")

    if equal_journal_nums:
        if float(f"{dataframe['Amount'].agg(np.sum):.2f}") != 0.00:
            print("Something is wrong with sum of all Amount entries")
            print("Please, do manual testing of each entry")
        else:
            print("All amounts are equal to 0.00")
    else:
        print(float(f"{dataframe['Amount'].agg(np.sum):.2f}"))
        print("All amounts are equal to 0.00")


def data_integrity_check(dataframe):
    print("Checking for null values")
    nan_values = dataframe[dataframe.isna().any(axis=1)]
    # if nan_values.empty():
    #     print("No empty values found")
    # for x in nan_values:
    #     print(x)
    print(dataframe[dataframe.isna().any(axis=1)])
    print("-----------------------------------------------------")

    dataTypeObj = dataframe.dtypes['Amount']
    if dataTypeObj != np.float64:
        print("ERROR: Data type of column 'Amount' is not float64")
    else:
        print("SUCCESS: All values of 'Amount' column is float64")

    for item in dataframe.Amount:
        try:
            float(item)
        except ValueError:
            print(f"{dataframe[dataframe['Amount'] == item]} is not float64 type")

    # cc = list(filter(combined_csv['Amount'].map(type) != str))
    # for y in combined_csv.Amount:
    #     if (agg[y].dtype == np.float64 or agg[y].dtype == np.int64):
    #         treat_numeric(agg[y])
    #     else:
    #         treat_str(agg[y])
    # print(floats.dtypes)
    #
    # for i, j in floats.iterrows():
    #     if not isinstance(j[0], np.float64):
    #         print(j[0].dtype)

    # for item in floats.Amount:
    #     if isinstance(item, float):
    #         continue
    #     else:
    #         print(f'{item}')
    # print(*aa)
    # print(combined_csv['Amount'].map(type) != np.float64)

    # aa = [filter(lambda x: x != np.float64, combined_csv['Amount'])]


def init_date(dataframe):
    # combined_csv = pd.read_csv('combined.csv')

    dataframe['Date'] = pd.to_datetime(dataframe['Date'],
                                       format='%Y-%m-%d %H:%M:%S', errors='coerce')
    dataframe['Created date and time'] = pd.to_datetime(dataframe['Created date and time'],
                                                        format='%Y-%m-%d %H:%M:%S',
                                                        errors='coerce')
    return dataframe


def finding_wrong_entries(dataframe):
    """
    Finding wrong entries
    """
    print("Out of bound entries is running...")
    dataframe = dataframe[['Journal number', 'Date', 'Created date and time']]
    dataframe = \
        dataframe[pd.isnull(dataframe['Date']) | pd.isnull(dataframe['Created date and time'])][
            'Journal number']
    output_result_csv('finding_wrong_entries', dataframe, 'Journal number')
    # print(dataframe)
    # print(dataframe.loc[dataframe['Created date and time'].isnull()]['Journal number'])


# finding_wrong_entries(get_dataframe('converted.csv'))


def out_of_bound_entries(dataframe, start_date='2020-02-01 00:00:00',
                         end_date='2020-12-31 23:59:59'):
    """
    Finding out of bound entries
    """
    print("Out of bound entries is running...")
    dataframe = dataframe[['Journal number', 'Date', 'Created date and time']]
    dataframe = dataframe.loc[(dataframe['Date'] < '2020-02-01 00:00:00') | (
            dataframe['Date'] > '2020-12-31 23:59:59')]['Journal number']
    output_result_csv('out_of_bound_entries', dataframe, 'Journal number')
    # print(dataframe.loc[(dataframe['Date'] < '2020-02-01 00:00:00') | (
    #         dataframe['Date'] > '2020-12-31 23:59:59')]['Journal number'])


def weekend_entries(dataframe):
    """
    Finding weekend entries done
    """
    print("Finding weekend is running...")
    dataframe = dataframe[['Journal number', 'Created date and time']]
    dataframe = dataframe.loc[dataframe['Created date and time'].dt.dayofweek > 4][
        'Journal number']
    output_result_csv('weekend_entries', dataframe, 'Journal number')
    # print(dataframe)
    # print(len(dataframe))


def holiday_entries(dataframe):
    """
    Finding holidays done
    """
    print("Finding holidays is running...")
    dataframe = dataframe[['Journal number', 'Created date and time']]
    holiday_years = [x for x in
                     range(dataframe['Created date and time'].dt.year.min().astype(int),
                           dataframe['Created date and time'].dt.year.max().astype(int) + 1)]
    holidays_canada = holidays.CountryHoliday('CA', prov='AB', years=holiday_years)
    vals = list(map(lambda x: x.strftime('%Y-%m-%d'), [x for x in holidays_canada.keys()]))
    dataframe = \
        dataframe.loc[dataframe['Created date and time'].dt.date.astype('datetime64').isin(vals)][
            'Journal number']
    output_result_csv('holiday_entries', dataframe, 'Journal number')
    # print(dataframe.loc[dataframe['Created date and time'].dt.date.astype('datetime64').isin(vals)][
    #           'Journal number'])


def unusual_times(dataframe):
    """
    Unusual times done
    """
    print("Unusual times is running...")
    dataframe = dataframe[['Journal number', 'Created date and time']]
    # print(dataframe.loc[(dataframe['Created date and time'] < '08:00:00') | (
    #         dataframe['Created date and time'] > '17:59:59')]['Journal number'])
    dataframe = dataframe.loc[(dataframe['Created date and time'].dt.time > time(17, 59, 59))][
        'Journal number']
    output_result_csv('unusual_times', dataframe, 'Journal number')
    # print(dataframe.loc[(dataframe['Created date and time'].dt.time > time(17, 59, 59))][
    #           'Journal number'])


def back_forward_date_entries(dataframe):
    """
    Finding back and forward dates entries done
    """
    print("back and forward dates is running...")
    dataframe = dataframe[['Journal number', 'Date', 'Created date and time']]
    dataframe = dataframe.loc[
        abs(dataframe['Created date and time'] - dataframe['Date']) >= timedelta(days=40)][
        'Journal number']
    output_result_csv('back_forward_date_entries', dataframe, 'Journal number')
    # print(dataframe.loc[
    #           abs(dataframe['Created date and time'] - dataframe['Date']) >= timedelta(days=40)][
    #           'Journal number'])


def dismissed_employee(dataframe):
    """
    Dismissed employees analysis done
    """
    dataframe = dataframe[['Journal number', 'Date', 'Created by', 'Created date and time']]
    # # created_by = pd.read_csv('Created_by.csv')
    # dataframe['Date'] = pd.to_datetime(dataframe['Date'],
    #                                    format='%Y-%m-%d %H:%M:%S', errors='coerce')
    # dataframe['Created date and time'] = pd.to_datetime(dataframe['Created date and time'],
    #                                                     format='%Y-%m-%d %H:%M:%S',
    #                                                     errors='coerce')
    fired_emp = ['mabrown', 'fgilmour', 'nmartinez']
    dismiss_date = ['2020-09-01']
    aa = dataframe.loc[dataframe['Created by'].isin(fired_emp)]
    bb = aa.loc[aa['Created date and time'].dt.date > date(2020, 9, 1)]['Journal number']
    print(bb)


def suspicious_desc(dataframe):
    """
    TO DO :Users can wish to search more than one word
    """
    dataframe = dataframe[['Journal number', 'Description']]
    word = ['reversal']
    print(dataframe.loc[
              dataframe['Description'].str.contains(pat='reversal', case=False, flags=0, na=False)][
              'Journal number'])
    # print(combined_csv.loc[
    #               combined_csv['Description'].str.contains(pat=r'[a-zA-Z]*(reversal)[a-zA-Z]*',
    #                                                        case=False, flags=0, na=False)]['Journal number'])


def over_scope_entries(dataframe, treshold=1500000):
    """
    The values greater than treshold
    """
    print("Over scope entries is running...")
    dataframe = dataframe[['Journal number', 'Amount']]
    dataframe = dataframe.loc[dataframe['Amount'] > treshold]['Journal number']
    output_result_csv('over_scope_entries', dataframe, 'Journal number')
    # print(aa)


def user_analysis(dataframe):
    """
    Finding employees by name
    """
    print("Finding employees is running...")
    dataframe = dataframe[['Journal number', 'Created by']]
    employee = ['mabrown', 'fgilmour', 'nmartinez']
    dataframe = dataframe.loc[dataframe['Created by'].isin(employee)]['Journal number']
    output_result_csv('user_analysis', dataframe, 'Journal number')


# user_analysis(get_dataframe('converted.csv'))


def treshold_analysis(dataframe, treshold=15000, deviation=100):
    """
    Finding values which are between given ranges
    """
    print("Treshold analysis is running...")
    dataframe = dataframe[['Journal number', 'Amount']]
    dataframe = dataframe.loc[
        dataframe['Amount'].between(treshold - deviation, treshold + deviation, inclusive=False)][
        'Journal number']
    output_result_csv('treshold_analysis', dataframe, 'Journal number')
    # print(dataframe.loc[dataframe['Amount'].between(treshold - deviation, treshold + deviation,
    #                                                 inclusive=False)][
    #           'Journal number'])


def whole_amounts(dataframe):
    """
    Finding specific values by pattern given by users
    """
    dataframe = dataframe[['Journal number', 'Amount']]
    # print(dataframe.loc[len(set(dataframe['Amount'])) == 2]['Journal number'])
    print(dataframe.loc[dataframe['Amount'].apply(lambda x: len(set(str(abs(x)))) == 2)][
              'Journal number'])

# def reversal_entries(dataframe):
#     dataframe = dataframe[['Journal number', 'Ledger account', 'Amount']]
#     dataframe = dataframe.groupby(['Ledger account'])
#     dataframe = dataframe.loc[dataframe['Amount'].apply(lambda x: len(set(str(abs(x)))) == 2)]['Journal number']
#     print(dataframe['Amount'].value_counts())
