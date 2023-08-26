from random import random
from itertools import product
from atscale.utils.enums import PlatformType
from atscale.atscale_errors import EDAException
from typing import List

POWER_METHOD_ITERATIONS=12

def _get_pca_sql(table_name:str, table_cols:List[str], pc_num:int, platform_type:PlatformType) -> str:
    """Generates a SQL query that performs principal component analysis (PCA) on the data contained in the
       specified table

    Args:
        table_name (str): The table containing the data to be analyzed
        table_cols (list[str]): The columns corresponding to the features to be analyzed. (Must be numeric)
        pc_num (int): The number of principal components to be returned from the analysis. Must be in 
                      the range of [1, # of features to be analyzed] (inclusive)
        platform_type (PlatformType): The type of warehouse connection passed to the PCA function

    Returns:
        str: The SQL query that performs PCA
    """

    query_statements = []
    drop_statements = []
    display_statements = {'PCs': '',
                          'Weights': ''}

    dim = len(table_cols)
    iter_num = POWER_METHOD_ITERATIONS

    # Error checking
    if iter_num <= 0 or type(iter_num) != int:
        raise EDAException('Number of Power Method iterations must be some positive integer')

    # DROP IF EXISTS string to clear tables/views in case prior run stopped short

    query_statements.append(f'DROP VIEW IF EXISTS {table_name}_outer_product; ')
    query_statements.append(f'DROP TABLE IF EXISTS {table_name}_outer_product_calc; ')
    query_statements.append(f'DROP TABLE IF EXISTS {table_name}_pc_vals; ')
    query_statements.append(f'DROP TABLE IF EXISTS {table_name}_magnitude_reciprocal; ')
    query_statements.append(f'DROP TABLE IF EXISTS {table_name}_pre_norm_division; ')

    for i in range(dim, 0, -1):
        query_statements.append(f'DROP VIEW IF EXISTS {table_name}_mult_column_{i}; ')
    query_statements.append(f'DROP VIEW IF EXISTS {table_name}_eigenvalue_total; ')
    for i in range(dim, 0, -1):
        query_statements.append(f'DROP TABLE IF EXISTS {table_name}_pc_{i}; ')
    for i in range(dim, 0, -1):
        query_statements.append(f'DROP TABLE IF EXISTS {table_name}_eigenvalue_{i}; ')
    query_statements.append(f'DROP TABLE IF EXISTS {table_name}_covariance; ')
    query_statements.append(f'DROP TABLE IF EXISTS {table_name}_covariance_calc; ')
    query_statements.append(f'DROP TABLE IF EXISTS {table_name}_rowcol; ')
    query_statements.append(f'DROP TABLE IF EXISTS {table_name}_removed_mean; ')

    # Mean-removed view
    mean_removed_string = f'CREATE TABLE {table_name}_removed_mean AS SELECT '
    for col in table_cols:
        mean_removed_string += f'{table_name}.{col} - (SELECT AVG({table_name}.{col}) ' + \
                               f'FROM {table_name}) AS {col}, '
    mean_removed_string = mean_removed_string[:-2] + f' FROM {table_name}; '

    query_statements.append(mean_removed_string)

    drop_statements = [f'DROP TABLE {table_name}_removed_mean; '] + drop_statements

    # Create table representing row/column indices
    query_statements.append(f'CREATE TABLE {table_name}_rowcol (id INT IDENTITY (1, 1), r INT, c INT); ')

    rowcol_string = f'INSERT INTO {table_name}_rowcol (r, c) VALUES '
    for pair in product(range(1, dim + 1), range(1, dim + 1)):
        rowcol_string += f'({pair[0]}, {pair[1]}), '
    rowcol_string = rowcol_string[:-2] + '; '

    query_statements.append(rowcol_string)
    
    drop_statements = [f'DROP TABLE {table_name}_rowcol; '] + drop_statements

    # Calculate and structure covariance matrix
    covariance_calc_string = f'CREATE TABLE {table_name}_covariance_calc AS '
    counter = 1
    for pair in product(table_cols, table_cols):
        covariance_calc_string += f'SELECT {counter} AS id, (1. / COUNT(*)) * SUM ({pair[0]} * {pair[1]}) AS vals FROM ' + \
                                  f'{table_name}_removed_mean UNION ALL '
        counter += 1
    covariance_calc_string = covariance_calc_string[:-11] + '; '

    query_statements.append(covariance_calc_string)

    drop_statements = [f'DROP TABLE {table_name}_covariance_calc; '] + drop_statements

    covariance_string = f'CREATE TABLE {table_name}_covariance AS ' + \
                        f'SELECT {table_name}_rowcol.id, {table_name}_rowcol.r, {table_name}_rowcol.c, cf.vals FROM ' + \
                        f'(SELECT {table_name}_covariance_calc.id AS id, vals FROM {table_name}_covariance_calc) ' + \
                        f'AS cf JOIN {table_name}_rowcol ON {table_name}_rowcol.id = cf.id; '

    query_statements.append(covariance_string)

    drop_statements = [f'DROP TABLE {table_name}_covariance; '] + drop_statements

    # Power Method iterations with Hotelling Deflation
    power_method_string = ''
    for d in range(1, dim + 1):
        # Initialize PC to random-valued vector prior to iterations
        power_method_string = f'CREATE TABLE {table_name}_pc_{d} (place INT IDENTITY (1, 1), vals DOUBLE PRECISION); '

        query_statements.append(power_method_string)

        power_method_string = f'INSERT INTO {table_name}_pc_{d} (vals) VALUES '

        for _ in range(1, dim + 1):
            power_method_string += f'({random()}), '
        power_method_string = power_method_string[:-2] + '; '

        query_statements.append(power_method_string)

        for i in range(iter_num):
            # Multiply covariance matrix by eventual PC
            ### Multiply covariance matrix columns (produces dim vectors)
            for col in range(1, dim + 1):
                power_method_string = f'CREATE VIEW {table_name}_mult_column_{col} AS ' + \
                                      f'SELECT temp.place AS place, (vec_vals * cov_vals) AS vals FROM ' + \
                                      f'(SELECT {table_name}_covariance.r AS place, {table_name}_covariance.r, ' + \
                                      f'{table_name}_covariance.c, {table_name}_pc_{d}.vals AS vec_vals, ' + \
                                      f'{table_name}_covariance.vals AS cov_vals ' + \
                                      f'FROM {table_name}_pc_{d} JOIN {table_name}_covariance ' + \
                                      f'ON {table_name}_pc_{d}.place = {table_name}_covariance.c ' + \
                                      f'WHERE {table_name}_covariance.c = {col} ' + \
                                      f'ORDER BY {table_name}_covariance.r ASC) AS temp; '

                query_statements.append(power_method_string)

            ### Add columns found above (produces one vector)
            power_method_string = f'CREATE TABLE {table_name}_pre_norm_division AS ' + \
                                  f'SELECT temp.place AS place, vals AS vals FROM ' + \
                                  f'(SELECT {table_name}_mult_column_{col}.place AS place, ('
            for col in range(1, dim + 1):
                power_method_string += f'{table_name}_mult_column_{col}.vals + '
            power_method_string = power_method_string[:-3] + ') AS vals '
            power_method_string += f'FROM {table_name}_mult_column_1 '
            for col in range(2, dim + 1):
                power_method_string += f'JOIN {table_name}_mult_column_{col} ON ' + \
                                       f'{table_name}_mult_column_1.place = {table_name}_mult_column_{col}.place '
            power_method_string = power_method_string[:-1] + ') AS temp; '

            query_statements.append(power_method_string)

            ### Find reciprocal of magnitude of vector found above (produces scalar)
            power_method_string = f'CREATE TABLE {table_name}_magnitude_reciprocal AS '
            for row in range(dim - 1, -1, -1):
                power_method_string += f'(SELECT COUNT(place) - {row} AS place, ' + \
                                       f'(1 / SQRT(SUM(POWER(vals, 2)))) AS vals FROM ' + \
                                       f'{table_name}_pre_norm_division) UNION ALL '
            power_method_string = power_method_string[:-11] + '; '

            query_statements.append(power_method_string)

            ### Normalize vector via quantity found above
            power_method_string = f'CREATE TABLE {table_name}_pc_vals AS ' + \
                                  f'SELECT temp.place AS place, temp.vals AS vals FROM ' + \
                                  f'(SELECT {table_name}_pre_norm_division.place AS place, ' + \
                                  f'({table_name}_pre_norm_division.vals * {table_name}_magnitude_reciprocal.vals) AS vals ' + \
                                  f'FROM {table_name}_pre_norm_division JOIN {table_name}_magnitude_reciprocal ' + \
                                  f'ON {table_name}_pre_norm_division.place = {table_name}_magnitude_reciprocal.place) AS temp; '

            query_statements.append(power_method_string)

            ### Get eigenvalue, store in table form
            if i == iter_num - 1:
                power_method_string = f'CREATE TABLE {table_name}_eigenvalue_{d} AS ' + \
                                      f'SELECT {table_name}_pre_norm_division.place AS id, ({table_name}_pre_norm_division.vals * ' + \
                                      f'(1 / {table_name}_pc_{d}.vals)) AS vals FROM ' + \
                                      f'{table_name}_pre_norm_division JOIN {table_name}_pc_{d} ON ' + \
                                      f'{table_name}_pre_norm_division.place = {table_name}_pc_{d}.place; '

                query_statements.append(power_method_string)

            ### Update vector with vector normalized above
            for p in range(1, dim + 1):
                power_method_string = f'UPDATE {table_name}_pc_{d} SET vals = (SELECT vals FROM ' + \
                                      f'{table_name}_pc_vals WHERE place = {p}) WHERE place = {p}; '

                query_statements.append(power_method_string)

            # Destroy all views used to update the PC, but keep the PC itself
            query_statements.append(f'DROP TABLE {table_name}_pc_vals; ')
            query_statements.append(f'DROP TABLE {table_name}_magnitude_reciprocal; ')
            query_statements.append(f'DROP TABLE {table_name}_pre_norm_division; ')

            for col in range(dim, 0, -1):
                power_method_string = f'DROP VIEW {table_name}_mult_column_{col}; '

                query_statements.append(power_method_string)

        # Deflate covariance matrix
        power_method_string = f'CREATE TABLE {table_name}_outer_product_calc AS '
        for i in range(1, dim + 1):
            power_method_string += f'SELECT {table_name}_eigenvalue_{d}.id + {dim * (i - 1)} AS id, ' + \
                                   f'(SELECT vals FROM {table_name}_pc_{d} WHERE place = {i}) * {table_name}_pc_{d}.vals * ' + \
                                   f'{table_name}_eigenvalue_{d}.vals AS vals ' + \
                                   f'FROM {table_name}_pc_{d} ' + \
                                   f'JOIN {table_name}_eigenvalue_{d} ON {table_name}_pc_{d}.place = {table_name}_eigenvalue_{d}.id UNION ALL '
        power_method_string = power_method_string[:-11] + '; '

        query_statements.append(power_method_string)

        power_method_string = f'CREATE VIEW {table_name}_outer_product AS SELECT ' + \
                              f'{table_name}_rowcol.r, {table_name}_rowcol.c, vals FROM {table_name}_outer_product_calc ' + \
                              f'JOIN {table_name}_rowcol ON {table_name}_outer_product_calc.id = {table_name}_rowcol.id; '

        query_statements.append(power_method_string)

        for pair in product(range(1, dim + 1), range(1, dim + 1)):
            power_method_string = f'UPDATE {table_name}_covariance ' + \
                                  f'SET vals = (SELECT ({table_name}_covariance.vals - {table_name}_outer_product.vals) AS vals ' + \
                                  f'FROM {table_name}_covariance JOIN {table_name}_outer_product ' + \
                                  f'ON {table_name}_covariance.r = {table_name}_outer_product.r ' + \
                                  f'AND {table_name}_covariance.c = {table_name}_outer_product.c ' + \
                                  f'AND {table_name}_covariance.r = {pair[0]} ' + \
                                  f'AND {table_name}_covariance.c = {pair[1]}) ' + \
                                  f'WHERE r = {pair[0]} and c = {pair[1]}; '

            query_statements.append(power_method_string)    

        query_statements.append(f'DROP VIEW {table_name}_outer_product;') 
        query_statements.append(f'DROP TABLE {table_name}_outer_product_calc; ')     
    
    # Return PCs and their weights
    ### Display PCs
    pc_display_string = 'SELECT '
    for p in range(1, pc_num + 1):
        pc_display_string += f'{table_name}_pc_{p}.vals AS pc_{p}, '
    pc_display_string = pc_display_string[:-2] + f' FROM {table_name}_pc_1 '
    for p in range(2, pc_num + 1):
        pc_display_string += f'JOIN {table_name}_pc_{p} ON ' + \
                         f'{table_name}_pc_1.place = {table_name}_pc_{p}.place '
    pc_display_string = pc_display_string[:-1] + '; '

    display_statements['PCs'] = pc_display_string

    ### Define total of eigenvalues
    eigval_total_string = f'CREATE VIEW {table_name}_eigenvalue_total AS ' + \
                          f'SELECT {table_name}_eigenvalue_1.id, ('
    for d in range(1, dim + 1):
        eigval_total_string += f'{table_name}_eigenvalue_{d}.vals + '
    eigval_total_string = eigval_total_string[:-3] + f') AS total FROM {table_name}_eigenvalue_1 '
    for d in range(2, dim + 1):
        eigval_total_string += f'JOIN {table_name}_eigenvalue_{d} ON {table_name}_eigenvalue_1.id = {table_name}_eigenvalue_{d}.id '
    eigval_total_string = eigval_total_string[:-1] + '; '

    query_statements.append(eigval_total_string) 

    ### Display relative weights of PCs
    weight_display_string = 'SELECT '
    for p in range(1, pc_num + 1):
        weight_display_string += f'({table_name}_eigenvalue_{p}.vals / {table_name}_eigenvalue_total.total * 100) AS pc_{p}_percent_weight, '
    weight_display_string = weight_display_string[:-2] + f' FROM {table_name}_eigenvalue_total '
    for p in range(1, pc_num + 1):
        weight_display_string += f'JOIN {table_name}_eigenvalue_{p} ON {table_name}_eigenvalue_total.id = 1 AND {table_name}_eigenvalue_{p}.id = 1 '
    weight_display_string = weight_display_string[:-1] + '; '

    display_statements['Weights'] = weight_display_string

    # Drop views, tables used above to drop string
    for p in range(1, dim + 1):
        drop_statements = [f'DROP TABLE {table_name}_pc_{p}; '] + drop_statements
    for d in range(1, dim + 1):
        drop_statements = [f'DROP TABLE {table_name}_eigenvalue_{d}; '] + drop_statements
    drop_statements = [f'DROP VIEW {table_name}_eigenvalue_total; '] + drop_statements

    # Capitalize everything if DB is Snowflake
    if platform_type == PlatformType.SNOWFLAKE:
        for ind in range(len(query_statements)):
            query_statements[ind] = query_statements[ind].upper()
        for ind in range(len(drop_statements)):
            drop_statements[ind] = drop_statements[ind].upper()

        display_statements['PCs'] = display_statements['PCs'].upper()
        display_statements['Weights'] = display_statements['Weights'].upper()

    return [query_statements, drop_statements, display_statements]
    