from collections import Counter
from datetime import date, timedelta

import holidays
import numpy as np

from utils import *


def init_date(dataframe):
    # combined_csv = pd.read_csv('combined.csv')

    dataframe['Date'] = pd.to_datetime(dataframe['Date'],
                                       format='%Y-%m-%d %H:%M:%S', errors='coerce')
    dataframe['Created date and time'] = pd.to_datetime(dataframe['Created date and time'],
                                                        format='%Y-%m-%d %H:%M:%S',
                                                        errors='coerce')
    return dataframe


def data_integrity_check(dataframe):
    print("Checking for null values")
    nan_values = dataframe[dataframe.isna().any(axis=1)]
    if nan_values.empty():
        print("No empty values found")
    else:
        return False
    # for x in nan_values:
    #     print(x)
    # print(dataframe[dataframe.isna().any(axis=1)])
    # print("-----------------------------------------------------")
    nans = dataframe[dataframe.isna().any(axis=1)]
    if nan_values.empty():
        print("No empty values found")
    else:
        return False

    dataTypeObj = dataframe.dtypes['Amount']
    if dataTypeObj != np.float64:
        print("ERROR: Data type of column 'Amount' is not float64")
        return False
    else:
        print("SUCCESS: All values of 'Amount' column is float64")

    for item in dataframe.Amount:
        try:
            float(item)
        except ValueError:
            print(f"{dataframe[dataframe['Amount'] == item]} is not float64 type")
            return False

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
        credit = float(f"{lt_credits['Amount'].agg(np.sum):.2f}")
        debit_sum.append(debit)
        credit_sum.append(credit)
        closing_sum.append(float(f"{(debit + credit):.2f}"))

    trial_balance['GL Debits'] = debit_sum
    trial_balance['GL Credits'] = credit_sum
    trial_balance['GL Closing balance'] = closing_sum
    trial_balance['GL Difference'] = trial_balance['Closing balance'] - closing_sum
    # print(trial_balance[trial_balance['GL Difference'].equals(0.00)])
    trial_balance.to_csv("Result Trial balance_CLFL 2020.csv", index=False, encoding='utf-8-sig')


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


def out_of_bound_entries(name, dataframe, **col_names):
    """
    Finding out of bound entries
    """
    print("Out of bound entries is running...")

    dataframe = dataframe.loc[(dataframe[col_names['date']] < col_names['start']) | (
            dataframe[col_names['date']] > col_names['end'])]
    save_to_xlsx_file(name, f'out_of_bnd_{name}', dataframe)
    # dataframe = dataframe[['Journal number', 'Date', 'Created date and time']]
    # dataframe = dataframe.loc[(dataframe['Date'] < start_date) | (
    #         dataframe['Date'] > end_date)]['Journal number']
    # output_result_csv('out_of_bound_entries', dataframe, 'Journal number')
    # print(dataframe.loc[(dataframe['Date'] < '2020-02-01 00:00:00') | (
    #         dataframe['Date'] > '2020-12-31 23:59:59')]['Journal number'])


def weekend_entries(name, dataframe, week_days, **col_names):
    """
    Finding weekend entries done
    """
    print("Finding weekend is running...")
    dataframe = dataframe.loc[dataframe[col_names['date']].dt.dayofweek.isin(week_days)]
    save_to_xlsx_file(name, f'weekend_{name}', dataframe)
    # dataframe = dataframe[['Journal number', 'Created date and time']]
    # dataframe = dataframe.loc[dataframe['Created date and time'].dt.dayofweek.isin(week_days)][
    #     'Journal number']
    # output_result_csv('weekend_entries', dataframe, 'Journal number')
    # print(dataframe)


def holiday_entries(name, dataframe, **col_names):
    """
    Finding holidays done
    """
    print("Finding holidays is running...")
    holiday_years = [x for x in
                     range(dataframe[col_names['date']].dt.year.min().astype(int),
                           dataframe[col_names['date']].dt.year.max().astype(int) + 1)]
    holidays_canada = holidays.CountryHoliday(col_names['country'], prov=col_names['province'], years=holiday_years)
    vals = list(map(lambda x: x.strftime('%Y-%m-%d'), [x for x in holidays_canada.keys()]))
    dataframe = \
        dataframe.loc[dataframe[col_names['date']].dt.date.astype('datetime64').isin(vals)]
    save_to_xlsx_file(name, f'holiday_{name}', dataframe)
    # output_result_csv('holiday_entries', dataframe, 'Journal number')
    # print(dataframe.loc[dataframe['Created date and time'].dt.date.astype('datetime64').isin(vals)][
    #           'Journal number'])


def unusual_times(name, dataframe, **col_name):
    """
    Unusual times done
    """
    print("Unusual times is running...")
    # print(dataframe.loc[(dataframe['Created date and time'] < '08:00:00') | (
    #         dataframe['Created date and time'] > '17:59:59')]['Journal number'])
    # dataframe = dataframe.loc[(dataframe['Created date and time'].dt.time > time(17, 59, 59))][
    #     'Journal number']
    dataframe = dataframe.loc[(dataframe[col_name['date']] > col_name['finish_time'])]
    save_to_xlsx_file(name, f'unusual_{name}', dataframe)
    # output_result_csv('unusual_times', dataframe, 'Journal number')
    # print(dataframe.loc[(dataframe['Created date and time'].dt.time > time(17, 59, 59))][
    #           'Journal number'])


def back_forward_date_entries(name, dataframe, **col_names):
    """
    Finding back and forward dates entries done
    """
    print("back and forward dates is running...")
    dataframe = dataframe.loc[
        abs(dataframe[col_names['created']] - dataframe[col_names['date']]) >= timedelta(days=col_names['days'])]
    save_to_xlsx_file(name, f'back_date_{name}', dataframe)
    # output_result_csv('back_forward_date_entries', dataframe, 'Journal number')
    # print(dataframe.loc[
    #           abs(dataframe['Created date and time'] - dataframe['Date']) >= timedelta(days=40)][
    #           'Journal number'])


def dismissed_employee(name, dataframe):
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


def suspicious_desc(name, dataframe, **col_names):
    """
    TO DO :Users can wish to search more than one word
    Tested working
    """
    words = '|'.join(col_names['words'])
    words = r'\b(?:)({})\b'.format(words)
    print(words)
    # words = '(?i)(\W|^)(' + words + ')(\W|$)'
    # x = pd.Series()
    # if not words:
    #     dataframe = \
    #         dataframe[
    #             dataframe[col_names['description']].astype(str).str.contains(pat=r'\b(?:)({})\b'.format(words),
    #                                                                          case=False, flags=0, na=False, regex=True)]
    #     dataframe = \
    #     dataframe.loc[dataframe['Description'].str.contains('|'.join(words))][
    #         'Journal number']
    #
    # print(dataframe)
    ww = r"(?i)(\W|^)(per|error|correct|clear|write\soff|writeoff|write-off|wash\soff|write\sdown|lobbying|lobby" \
         "|business\sdevelopment|impair|impairment|adjust|fraud|help|reverse|ceo|cfo|directors|director|fix" \
         "|correction|correct|restate|variance)(\W|$)"

    dataframe = dataframe.loc[
        dataframe[col_names['description']].astype(str).str.contains(pat=words, case=False, flags=0, na=False,
                                                                     regex=True)]
    save_to_xlsx_file(name, f'suspicious_{name}', dataframe)
    # series = []
    # for i in words:
    #     series.append(dataframe.loc[
    #                       dataframe['Description'].str.contains(pat=i, case=False, flags=0,
    #                                                             na=False)]['Journal number'])
    # x = \
    # dataframe.loc[dataframe['Description'].str.contains(pat=i, case=False, flags=0, na=False)][
    #     'Journal number']
    # print(x)

    # dataframe = pd.concat(series)
    # print(dataframe)
    # dataframe.drop_duplicates(keep='first', inplace=True)
    # print(dataframe)
    # output_result_csv('suspicious_description', dataframe, 'Journal number')
    # print(combined_csv.loc[
    #               combined_csv['Description'].str.contains(pat=r'[a-zA-Z]*(reversal)[a-zA-Z]*',
    #                                                        case=False, flags=0, na=False)]['Journal number'])


def over_scope_entries(name, dataframe, overscope=1500000, **col_names):
    """
    The values greater than treshold
    """
    print("Over scope entries is running...")
    dataframe = dataframe.loc[dataframe[col_names['amount']] > overscope]
    save_to_xlsx_file(name, f'over_scope{name}', dataframe)
    # output_result_csv('over_scope_entries', dataframe, 'Journal number')
    # print(aa)


def user_analysis(name, dataframe, names, **col_names):
    """
    Finding employees by name
    """
    print("Finding employees is running...")
    dataframe = dataframe.loc[dataframe[col_names['created_by']].isin(names)]
    save_to_xlsx_file(name, f'user_anlys_{name}', dataframe)
    # output_result_csv('user_analysis', dataframe, 'Journal number')


# user_analysis(get_dataframe('converted.csv'))


def treshold_analysis(name, dataframe, treshold=15000, deviation=100, **col_names):
    """
    Finding values which are between given ranges
    """
    print("Treshold analysis is running...")
    dataframe = dataframe.loc[
        dataframe[col_names['treshold']].between(treshold - deviation, treshold + deviation, inclusive=False)]
    save_to_xlsx_file(name, f'treshood_anlys{name}', dataframe)
    # output_result_csv('treshold_analysis', dataframe, 'Journal number')
    # print(dataframe.loc[dataframe['Amount'].between(treshold - deviation, treshold + deviation,
    #                                                 inclusive=False)][
    #           'Journal number'])


def whole_amounts(name, dataframe, patterns, **col_names):
    """
    Finding specific values by pattern given by users
    """
    patterns = '|'.join(patterns)
    patterns = r'^.+({})'.format(patterns)
    print(patterns)
    dataframe = dataframe.loc[
        dataframe[col_names['amount']].astype(str).str.contains(pat=patterns, case=False, flags=0, na=False,
                                                                regex=True)]
    # dataframe = \
    #     dataframe.loc[
    #         dataframe[col_names['amount']].astype(str).str.contains(pat=patterns, case=False, flags=0, na=False)]
    save_to_xlsx_file(name, f'whole_am{name}', dataframe)
    # print(dataframe)
    # print(dataframe.loc[len(set(dataframe['Amount'])) == 2]['Journal number'])
    # print(dataframe.loc[dataframe['Amount'].apply(lambda x: len(set(str(abs(x)))) == 2)][
    #           'Journal number'])


def acc_estimates(name, dataframe, list_estimates, **col_names):
    """
    Finding specific values by pattern given by users
    """
    print(f'10 -> Account estimates is running {len(dataframe)}')
    df = pd.DataFrame(columns=dataframe.columns.values.tolist())
    for i in list_estimates:
        df_temp = dataframe[dataframe[col_names['estimates']] % i == 0]
        df = pd.concat([df, df_temp], axis=0)
    save_to_xlsx_file(name, f'acc_estimates{name}', df)
    # df = dataframe[dataframe['Amount'] % 1000000 == 0]
    # if len(df):
    #     res = f'{len(df) / (len(dataframe) / 100):.2f}%'
    #     print(res)
    #     dataframe = {'Posting type': 'Total percentage', 'Posting layer': res}
    #     dataframe = df.append(dataframe, ignore_index=True)
    # dataframe_a = dataframe.loc[dataframe[col_names['estimates']].isin(list_estimates)]
    # if dataframe_a:
    #     print(f'{len(dataframe_a) / (len(dataframe) / 100):.2f}%')
    # save_to_xlsx_file(name, f'acc_estimates{name}', dataframe)
    # output_result_csv('account_estimates', dataframe_a, 'Journal number')


def sequential(name, dataframe, **col_names):
    """
    Find gaps in journal entry number sequence. (in Journal number column)
    """
    dataframe = dataframe[[col_names['journal_num']]]
    dataframe = dataframe.drop_duplicates()
    j_min = min(dataframe[col_names['journal_num']])
    j_max = max(dataframe[col_names['journal_num']])

    pref = j_max[:j_max.index('-')] + '-'

    zero_len = len(j_max[j_max.index('-') + 1:])
    # print(zero_len)

    j_min = int(j_min[j_min.index('-') + 1:])
    j_max = int(j_max[j_max.index('-') + 1:])

    print(j_min, j_max)
    j_list = np.arange(j_min, j_max + 1, 1)
    result = []
    for i in range(len(j_list)):
        result.append(pref + ('0' * abs(len(str(j_list[i])) - zero_len)) + str(j_list[i]))
        # print(j_list[i])
    result = set(result) ^ set(dataframe[col_names['journal_num']].tolist())
    series = pd.Series(list(result))
    dataframe = pd.DataFrame({'Journal number': series})
    print(dataframe)
    save_to_xlsx_file(name, f'sequential_{name}', dataframe)
    # dataframe.to_csv(f'results/sequential.csv', index=False, encoding='utf-8')


def duplicate_amounts(name, dataframe, args):
    """
    Finding specific values by pattern given by users
    """
    dataframe = dataframe.loc[dataframe.duplicated(subset=args, keep=False)]
    save_to_xlsx_file(name, f'duplicate_{name}', dataframe)
    # output_result_csv('duplicate_amounts', dataframe, 'Journal number')


def suspense_accounts(name, dataframe, **col_names):
    """
    Identify journal entries made to suspense accounts (Account Name contains "DO NOT USE")
    """
    dataframe = dataframe.loc[dataframe[col_names['suspense']].str.contains(r'DO\sNOT\sUSE', na=False)]
    # dataframe = dataframe[dataframe['Account name'].str.contains(r'Undeposited\sfunds')]['Journal number']
    save_to_xlsx_file(name, f'suspense_acc_{name}', dataframe)
    # output_result_csv('suspense_accounts', dataframe, 'Journal number')


def no_description(name, dataframe, chosen_date, **col_names):
    """
    Recorded at the end of the period or as post-closing entries that have no description
    """
    dataframe = dataframe[dataframe[col_names['date']] == chosen_date]
    dataframe = dataframe[dataframe[col_names['description']].isnull()]
    # dataframe = dataframe[(dataframe['Description'].isnull()) and (dataframe['Description'].values == '')]['Journal number']
    dataframe = dataframe[dataframe.isna().any(axis=1)]
    save_to_xlsx_file(name, f'no_descr{name}', dataframe)
    # output_result_csv('no_description', dataframe, 'Journal number')


def word_analysis(name, dataframe, **col_names):
    """
    Word analysis based on word frequency
    """
    word_list = dataframe[col_names['description']].dropna()
    words = []
    for i in word_list:
        for j in i.split():
            if j.isalpha():
                words.append(j)
    ll = sorted(list(Counter(words).items()), key=lambda x: x[1])
    less_used = ll[:10]
    more_used = ll[len(ll) - 10:]
    print(less_used)
    print(more_used)
    # xs = [x for x, y in more_used]
    # ys = [y for x, y in more_used]
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.bar([x for x, y in more_used], [y for x, y in more_used])
    ax1.set(xlabel="Words",
            ylabel="Word frequency")
    fig1.suptitle("Word Analysis", fontsize=18, fontweight="bold")

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.bar([x for x, y in less_used], [y for x, y in less_used])
    ax2.set(xlabel="Words",
            ylabel="Word frequency")
    fig2.suptitle("Word Analysis", fontsize=18, fontweight="bold")
    fig1.savefig(f"results/{name}/word_anlys_{name}1.png")
    fig2.savefig(f"results/{name}/word_anlys_{name}2.png")
