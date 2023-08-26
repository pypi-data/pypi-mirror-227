from html import unescape
from unicodedata import name

from aenum import Enum, NoAlias

class AtScaleColumnTypes(Enum):
    """Values are substrings to look for in type field of AtScale column definition.
    """
    #examples
    #[('DATE', 'DateTime'), ('PREDICTION', 'Decimal(38,0)')]
    Date = 'Date'
    DateTime = 'DateTime'
    Decimal = 'Decimal'
    String = 'String'


class DMVColumnBaseClass(Enum):
    def requires_translation(self):
        if self in self.internal_func_dict():
            return True
        return False

    def to_regex(self):
        return f'<{self.value}>(.*?)</{self.value}>'

    def translate(self, val):
        """ Translates the parsed output from a DMV response into a user interpretable format. If a field has a specific
        translation, Hierarcy.dimension: [dimension_name] -> dimension_name for example, it must be declared in the
        respective class's internal_func_dict() method. If no specific function is declared there, the value will be
        converted from html string encoding changes that may have occured since its original input. For example,
        &quot gets converted to " and \\' gets converted to \'"""
        func_dict = self.internal_func_dict()
        if self in func_dict:
            func = func_dict[self]
            return func(val)
        else:
            return unescape(val).encode('utf-8').decode('unicode_escape')  # unescape &quote; encode so we can decode \\


class Hierarchy(DMVColumnBaseClass):
    description = 'DESCRIPTION'
    name = 'HIERARCHY_NAME'
    caption = 'HIERARCHY_CAPTION'
    visible = 'HIERARCHY_IS_VISIBLE'
    type = 'DIMENSION_TYPE'
    folder = 'HIERARCHY_DISPLAY_FOLDER'
    dimension = 'DIMENSION_UNIQUE_NAME'
    secondary_attribute = 'STRUCTURE'

    @property
    def schema(self):
        return "$system.MDSCHEMA_HIERARCHIES"

    @property
    def where(self):
        return " WHERE [HIERARCHY_NAME] &lt;&gt; 'Measures' AND [CUBE_NAME] = @CubeName"

    def internal_func_dict(self):
        def hierarchy_type_func(type_number: str):
            if type_number == '1':
                return 'Time'
            elif type_number == '3':
                return 'Standard'
            else:
                return None

        return {
            self.__class__.type: (lambda x: hierarchy_type_func(x)),
            self.__class__.dimension: (lambda x: x[1:-1]),
            self.__class__.secondary_attribute: (lambda x: False if x == '1' else True),
            }


class Measure(DMVColumnBaseClass):
    name = 'MEASURE_NAME'
    description = 'DESCRIPTION'
    caption = 'MEASURE_CAPTION'
    visible = 'MEASURE_IS_VISIBLE'
    type = 'MEASURE_AGGREGATOR'
    folder = 'MEASURE_DISPLAY_FOLDER'
    expression = 'EXPRESSION'

    @property
    def schema(self):
        return "$system.MDSCHEMA_MEASURES"

    @property
    def where(self):
        return ' WHERE [CUBE_NAME] = @CubeName'  # need to specify only fields for our cube for all query types

    def internal_func_dict(self):
        return {
            self.__class__.type: (lambda x: 'Calculated' if x == '9' else 'Aggregate'),
            }


class Level(DMVColumnBaseClass):
    _settings_ = NoAlias  # necessary for different fields with the same value but different func

    description = 'DESCRIPTION'
    name = 'LEVEL_NAME'
    caption = 'LEVEL_CAPTION'
    visible = 'LEVEL_IS_VISIBLE'
    type = 'LEVEL_TYPE'
    dimension = 'HIERARCHY_UNIQUE_NAME'
    hierarchy = 'HIERARCHY_UNIQUE_NAME'
    level_number = 'LEVEL_NUMBER'

    @property
    def schema(self):
        return "$system.mdschema_levels"

    @property
    def where(self):
        return " WHERE [CUBE_NAME] = @CubeName and [LEVEL_NAME] &lt;&gt; '(All)' and [DIMENSION_UNIQUE_NAME] " \
               "&lt;&gt; '[Measures]'"

    def internal_func_dict(self):
        return {
            self.__class__.level_number: (lambda x: int(x)),
            self.__class__.hierarchy: (lambda x: x.split('].[')[1][:-1]),
            self.__class__.dimension: (lambda x: x.split('].[')[0][1:]),
            self.__class__.type: (lambda x: LevelType(int(x)).name)
            }

class LevelType(Enum):
    """Translates the numeric level indicator from the data model json into a string form
    """
    Standard = 0
    TimeYears = 20
    TimeHalfYears = 36
    TimeQuarters = 68
    TimeTrimesters = 4722
    TimeMonths = 132
    TimeWeeks = 260
    TimeDays = 516
    TimeHours = 772
    TimeMinutes = 1028
    TimeSeconds = 2052
    Undefined = 4100

class TimeLevels(Enum):

    _init_ = 'index, atscale_type, val, steps, sql_op, sql_name'

    def get_sql_expression(self, col):
        return f'{self.sql_op}({self.sql_name}, {col})'

    # Only handling AtScale time levels that are also in ANSI SQL and are date_trunc 
    # compatible right now; trying to be as generic as possible.
    Year = 0, 'TimeYears',20, [1, 2], 'date_trunc', 'year'
    Quarter = 1, 'TimeQuarters', 68, [1, 4], 'date_trunc', 'quarter'
    Month = 2, 'TimeMonths', 132, [1, 3, 6, 12], 'date_trunc', 'month'
    Week = 3, 'TimeWeeks', 260, [1, 4], 'date_part', 'week' #this one acts weird with date_trunc, so using date_part
    Day = 4, 'TimeDays', 516, [1, 7, 28], 'date_trunc', 'day'
    Hour = 5, 'TimeHours', 772, [1, 12, 24], 'date_trunc', 'hour'
    Minute = 6, 'TimeMinutes', 1028, [1, 60], 'date_trunc', 'minute'
    Second = 7, 'TimeSeconds', 2052, [1, 60], 'date_trunc', 'second'


class TimeSteps(Enum):
    """Translates the time levels into usable step sizes.
    """
    TimeSeconds = [1, 60]
    TimeMinutes = [1, 60]
    TimeHours = [1, 12, 24]
    TimeDays = [1, 7, 28]
    TimeWeeks = [1, 4]
    TimeMonths = [1, 3, 6, 12]
    TimeQuarters = [1, 4]
    TimeTrimesters = [1, 3]
    TimeHalfYears = [1, 2]
    TimeYears = [1, 2]


class Aggs(Enum):
    """Holds constant string representations for the supported aggregation methods of numerical aggregate features
     SUM: Addition
     AVG: Average
     MAX: Maximum
     MIN: Mininum
     DISTINCT_COUNT: Distinct-Count (count of unique values)
     DISTINCT_COUNT_ESTIMATE: An estimate of the distinct count to save compute
     NON_DISTINCT_COUNT: Count of all values
     STDDEV_SAMP: standard deviation of the sample
     STDDEV_POP: population standard deviation
     VAR_SAMP: sample variance
     VAR_POP: population variance
     """
    SUM = 'SUM'
    AVG = 'AVG'
    MAX = 'MAX'
    MIN = 'MIN'
    DISTINCT_COUNT = 'DC'
    DISTINCT_COUNT_ESTIMATE = 'DCE'
    NON_DISTINCT_COUNT = 'NDC'
    STDDEV_SAMP = 'STDDEV_SAMP'
    STDDEV_POP = 'STDDEV_POP'
    VAR_SAMP = 'VAR_SAMP'
    VAR_POP = 'VAR_POP'


class MDXAggs(Enum):
    SUM = 'Sum'
    STANDARD_DEVIATION = 'Stdev'
    MEAN = 'Avg'
    MAX = 'Max'
    MIN = 'Min'


class PandasTableExistsActionType(Enum):
    """Potential actions to take if a table already exists when trying to write a dataframe to that database table.
    APPEND: Append the rows to the end of the existing table
    REPLACE: Completely replace the existing table
    FAIL: raise an error
    """
    APPEND = 'append' 
    REPLACE = 'replace' 
    FAIL = 'fail' 

class PysparkTableExistsActionType(Enum):
    """Potential actions to take if a table already exists when trying to write a pyspark dataframe to that database table.
    APPEND: Append content of the pyspark dataframe to existing data or table
    OVERWRITE: Overwrite existing data with the content of pyspak dataframe
    IGNORE: Ignore current write operation if data/ table already exists without any error
    ERROR: Throw an exception if data or table already exists
    """
    APPEND = 'append'
    OVERWRITE = 'overwrite'
    IGNORE = 'ignore'
    ERROR = 'error'



class PlatformType(Enum):
    """PlatformTypes describe a type of supported data warehouse"""
    SNOWFLAKE = 'snowflake'
    REDSHIFT = 'redshift'
    GBQ = 'gbq'
    DATABRICKS = 'databricks'
    IRIS = 'iris'
    SYNAPSE = 'synapse'
    MSSQL = 'mssql'


class FeatureFormattingType(Enum):
    """How the value of a feature gets formatted before output"""
    GENERAL_NUMBER = 'General Number'
    STANDARD = 'Standard'
    SCIENTIFIC = 'Scientific'
    FIXED = 'Fixed'
    PERCENT = 'Percent'


class FeatureType(Enum):
    """Used for specifying all features or only numerics or only categorical"""
    ALL = 0
    NUMERIC = 1
    CATEGORICAL = 2


class RequestType(Enum):
    """Used for specifying type of http request"""
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
