import re

import pandas as pd


def parse_rest_query_response(response) -> pd.DataFrame:
    """ Parses results from a rest api SQL query response into a Dataframe.

        :param: requests.Response response The response used to formulate the dataframe that the function returns.
        :raises: Exception if the query returned an error
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
