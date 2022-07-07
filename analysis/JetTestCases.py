from collections import Counter
from datetime import timedelta, datetime

import holidays
import pandas as pd


class JetTestCases:
    __slots__ = ['_dataframe', '_passed_tests', '__dict__']

    def __init__(self, df):
        self._dataframe = df
        self._passed_tests = {}
        self.date_parsed = False

    def __del__(self):
        del self._dataframe
        del self._passed_tests

    def get_out_of_bound_entries(self, **kwargs):
        """
        Finding out of bound entries done
        """
        print("get_out_of_bound_entries is running...")
        df = pd.DataFrame()
        try:
            if not self.date_parsed:
                self._dataframe[kwargs['date']] = pd.to_datetime(self._dataframe[kwargs['date']])
                self.date_parsed = True
            date = self._dataframe[kwargs['date']]
            df = self._dataframe[(date < kwargs['start']) | (kwargs['end'] < date)]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_weekend_entries(self, **kwargs):
        """
        Finding weekend entries done
        """
        print("get_weekend_entries is running...")
        df = pd.DataFrame()
        try:
            if not self.date_parsed:
                self._dataframe[kwargs['date']] = pd.to_datetime(self._dataframe[kwargs['date']])
                self.date_parsed = True
            df = self._dataframe.loc[self._dataframe[kwargs['date']].dt.dayofweek.isin(kwargs['week_days'])]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_holiday_entries(self, **kwargs):
        """
        Finding holidays done
        """
        print("get_holiday_entries is running...")
        df = pd.DataFrame()
        try:
            if not self.date_parsed:
                self._dataframe[kwargs['date']] = pd.to_datetime(self._dataframe[kwargs['date']])
                self.date_parsed = True
            holiday_years = [x for x in
                             range(self._dataframe[kwargs['date']].dt.year.min().astype(int),
                                   self._dataframe[kwargs['date']].dt.year.max().astype(int) + 1)]
            holidays_canada = holidays.CountryHoliday(kwargs['country'], prov=kwargs['province'], years=holiday_years)
            vals = list(map(lambda x: x.strftime('%Y-%m-%d'), [x for x in holidays_canada.keys()]))
            df = \
                self._dataframe.loc[self._dataframe[kwargs['date']].dt.date.astype('datetime64').isin(vals)]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_unusual_times(self, **kwargs):
        """
        Unusual times done
        """
        print("get_unusual_times is running...")
        df = pd.DataFrame()
        try:
            if not self.date_parsed:
                self._dataframe[kwargs['date']] = pd.to_datetime(self._dataframe[kwargs['date']])
                self.date_parsed = True
            df = self._dataframe.loc[(self._dataframe[kwargs['date']] > kwargs['finish_time'])]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_back_forward_date_entries(self, **kwargs):
        """
        Finding back and forward dates entries done
        """
        print("get_back_forward_date_entries is running...")
        df = pd.DataFrame()
        try:
            if not self.date_parsed:
                self._dataframe[kwargs['created_date']] = pd.to_datetime(self._dataframe['created_date'])
                self._dataframe[kwargs['posted_date']] = pd.to_datetime(self._dataframe['posted_date'])
                self.date_parsed = True
            df = self._dataframe.loc[
                abs(self._dataframe[kwargs['created_date']] - self._dataframe[kwargs['posted_date']]) >= timedelta(
                    days=kwargs['days'])]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_suspicious_description(self, **kwargs):
        """
        TO DO :Users can wish to search more than one word
        Tested working
        """
        print("get_suspicious_description is running...")
        df = pd.DataFrame()
        try:
            words = '|'.join(kwargs['words'])
            words = r'\b(?:)({})\b'.format(words)
            print(words)
            df = self._dataframe.loc[
                self._dataframe[kwargs['description']].astype(str).str.contains(pat=words,
                                                                                case=False,
                                                                                flags=0,
                                                                                na=False,
                                                                                regex=True)]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_over_scope_entries(self, overscope=0, **kwargs):
        """
        The values greater than treshold
        """
        print("get_over_scope_entries is running...")
        df = pd.DataFrame()
        try:
            df = self._dataframe.loc[abs(self._dataframe[kwargs['amount']]) > kwargs['given_amount']]
            self._passed_tests['get_over_scope_entries'] = 1
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_employee_by_name(self, **kwargs):
        """
        Finding employees by name
        """
        print("get_employee_by_name is running...")
        df = pd.DataFrame()
        try:
            df = self._dataframe.loc[self._dataframe[kwargs['created_by']].isin(kwargs['names'])]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_amount_between_range(self, treshold=15000, deviation=100, **kwargs):
        """
        Finding values which are between given ranges
        """
        print("get_amount_between_range is running...")
        df = pd.DataFrame()
        try:
            df = self._dataframe.loc[
                self._dataframe[kwargs['amount']].between(treshold - deviation, treshold + deviation,
                                                          inclusive=False)]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_whole_amounts(self, **kwargs):
        """
        Finding specific values by pattern given by users
        """
        print('get_whole_amounts is running...')
        df = pd.DataFrame()
        try:
            patterns = '|'.join(kwargs['patterns'])
            patterns = r'^.+({})'.format(patterns)
            print(patterns)
            df = self._dataframe.loc[
                self._dataframe[kwargs['amount']].astype(str).str.contains(pat=patterns,
                                                                           case=False,
                                                                           flags=0,
                                                                           na=False,
                                                                           regex=True)]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_account_estimates(self, **kwargs):
        """
        Finding specific values by pattern given by users
        """
        print('get_account_estimates is running...')
        df = pd.DataFrame()
        try:
            df = pd.DataFrame(columns=self._dataframe.columns.values.tolist())
            for i in kwargs['list']:
                df_temp = self._dataframe[
                    (self._dataframe[kwargs['estimates']] % i == 0) & self._dataframe[kwargs['estimates']] != 0]
                df = pd.concat([df, df_temp], axis=0)
                df.drop_duplicates()
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_omitted_sequential_je(self, **kwargs):
        """
        Find gaps in journal entry number sequence. (in Journal number column)
        """
        print('get_omitted_sequential_je is running...')
        df = pd.DataFrame()
        try:
            df = self._dataframe[[kwargs['journal_num']]]
            df = df.drop_duplicates()
            j_min = min(df[kwargs['journal_num']])
            j_max = max(df[kwargs['journal_num']])

            pref = j_max[:j_max.index('-')] + '-'

            zero_len = len(j_max[j_max.index('-') + 1:])
            # print(zero_len)

            j_min = int(j_min[j_min.index('-') + 1:])
            j_max = int(j_max[j_max.index('-') + 1:])

            print(j_min, j_max)
            j_list = range(j_min, j_max + 1, 1)
            result = []
            for i in range(len(j_list)):
                result.append(pref + ('0' * abs(len(str(j_list[i])) - zero_len)) + str(j_list[i]))
                # print(j_list[i])
            result = set(result) ^ set(self._dataframe[kwargs['journal_num']].tolist())
            series = pd.Series(list(result))
            df = pd.DataFrame({'Journal number': series})
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_duplicate_amounts(self, **kwargs):
        """
        Finding specific values by pattern given by users
        """
        print('get_duplicate_amounts is running...')
        df = pd.DataFrame()
        try:
            df = self._dataframe.loc[self._dataframe.duplicated(subset=kwargs['list'], keep=False)]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_suspensed_accounts(self, **kwargs):
        """
        Identify journal entries made to suspense accounts (Account Name contains "DO NOT USE")
        """
        print('get_suspensed_accounts is running...')
        df = pd.DataFrame()
        try:
            df = self._dataframe.loc[
                self._dataframe[kwargs['text_col']].str.contains(r'DO\sNOT\sUSE', na=False)]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_no_description(self, **kwargs):
        """
        Recorded at the end of the period or as post-closing entries that have no description
        """
        print('get_no_description is running...')
        df = pd.DataFrame()
        try:
            if not self.date_parsed:
                self._dataframe[kwargs['date']] = pd.to_datetime(self._dataframe[kwargs['date']])
                self.date_parsed = True
            df = self._dataframe.loc[self._dataframe[kwargs['date']] == kwargs['chosen_date']]
            df = df[df[kwargs['description']].isnull()]
            # df = df[df.isna().any(axis=1)]
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False

    def get_word_freq(self, **kwargs):
        """
        Word analysis based on word frequency
        HAS SIDE EFFECT
        """
        print('get_word_analysis_in_image is running...')
        # name = kwargs['name']
        df = pd.DataFrame()
        # less_used, more_used = None, None
        try:
            word_list = self._dataframe[kwargs['description']].dropna()
            words = []
            for i in word_list:
                for j in i.split():
                    if j.isalpha():
                        words.append(j)
            ll = sorted(list(Counter(words).items()), key=lambda x: x[1])
            word_freq = ll[:10] + ll[len(ll) - 10:]
            # more_used = ll[len(ll) - 10:]
            df = pd.DataFrame(word_freq, columns=['Words', 'Words count'])
            # print(df)
            print(word_freq)
            # print(more_used)
            return df, True
        except Exception as ex:
            print(ex)
            print('Something went wrong, Test parameters are incorrect!')
            return df, False
