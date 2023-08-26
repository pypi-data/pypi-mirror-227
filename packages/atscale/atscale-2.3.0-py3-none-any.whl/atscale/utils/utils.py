import pandas as pd

from atscale.errors import *
import re

def prompt_yes_no(question: str) -> bool:
    need_a_good_answer: str = True
    while need_a_good_answer:
        answer: str = input(f'{question} y/n: ').lower()
        if answer.lower() in ['yes', 'y']:
            return True
        elif answer.lower() in ['no', 'n']:
            return False
        else:
            question = 'The input was not recognized. ' + question

def check_single_element(feature, check_list, errmsg=None):
    """ Checks that a given feature exists within a given list of features.

    :param str feature: The feature being checked.
    :param list or dict of str check_list: The list of features against which the feature is being checked.
    :param str errmsg: A custom error message displayed if feature isn't in check_list. If not specified otherwise, the standard message will be displayed.
    """
    if feature not in check_list:
        if errmsg:
            raise UserError(errmsg)
        else:
            raise UserError(f'Feature: \'{feature}\' not in model.'
                            ' Make sure each feature has been published and is correctly spelled')

def check_multiple_features(features, check_list, catch_duplicates=False, errmsg=None):
    """ Checks that the given feature(s) exist(s) within a specified list of features.

    :param list of str features: The features being checked.
    :param list of str check_list: The list of features against which the features are being checked.
    :param bool catch_duplicates: Whether the function should alert the user if duplicate features exist.
    Defaults to False.
    :param str errmsg: A custom error message displayed if the function finds an error. If not specified otherwise,
    the standard message will be displayed.
    """
    if catch_duplicates:
        check_dict = {}

        for item in check_list:
            check_dict[item] = 0

        error = ''

        try:
            for f in features:
                error = f
                check_dict[f] += 1
        except KeyError:
            if errmsg:
                raise UserError(errmsg)
            else:
                raise UserError(f'Feature: \'{error}\' not in model. Make sure each feature has been published and is '
                                'correctly spelled')
        for item in check_dict:
            if check_dict[item] > 1:
                raise UserError(f'Feature: \'{item}\' occurs multiple times. Please remove duplicates or check that '
                                'features are spelled correctly')
    else:
        for f in features:
            error = f
            if f not in check_list:
                if errmsg:
                    raise UserError(errmsg)
                else:
                    raise UserError(f'Feature: \'{error}\' not in model. Make sure each feature has been published and is'
                                    ' correctly spelled')

def parse_query_response(response):
        """ Parses a query response.

        :param requests.Response response: The response used to formulate the dataframe that the function returns.
        :return: A pandas DataFrame.
        :rtype: pandas.DataFrame
        """
        content = str(response.content)

        if re.search('<succeeded>(.*?)</succeeded>', content).group(1) == 'false':
            raise Exception(re.search('<error-message>(.*?)</error-message>', ' '.join(content.split('\n'))).group(1))
        column_names = re.findall('<name>(.*?)</name>', content)
        row_text = re.findall('<row>(.*?)</row>', content)
        rows = []
        for row in row_text:
            row = row.replace('<column null="true"/>', '<column></column>')
            cells = re.findall('<column>(.*?)</column>', row)
            rows.append(cells)
        df = pd.DataFrame(data=rows, columns=column_names)
        for column in df.columns:
            df[column] = pd.to_numeric(df[column].values, errors='ignore')
        return df

