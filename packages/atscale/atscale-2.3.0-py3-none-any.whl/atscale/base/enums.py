from html import unescape

from aenum import Enum, NoAlias

class DMVColumnBaseClass(Enum):
    """The base class for our various dmv query enums. Defines consistent functionality.
    """
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
    """An enum to represent the metadata of a hierarchy object for use in dmv queries.
    description: the description field
    name: the name field
    caption: the caption field
    visible: the visible field
    type: the type field
    folder: the folder field
    dimension: the dimension field
    secondary_attribute: the secondary_attribute field 
    """
    description = 'DESCRIPTION'
    name = 'HIERARCHY_NAME'
    caption = 'HIERARCHY_CAPTION'
    visible = 'HIERARCHY_IS_VISIBLE'
    type = 'DIMENSION_TYPE'
    folder = 'HIERARCHY_DISPLAY_FOLDER'
    dimension = 'DIMENSION_UNIQUE_NAME'
    secondary_attribute = 'HIERARCHY_ORIGIN'

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
    """An enum to represent the metadata of a measure object for use in dmv queries.
    name: the name field
    description: the description field
    caption: the caption field
    visible: the visible field
    type: the type field
    folder: the folder field
    expression: the expression field
    """
    name = 'MEASURE_NAME'
    description = 'DESCRIPTION'
    caption = 'MEASURE_CAPTION'
    visible = 'MEASURE_IS_VISIBLE'
    type = 'MEASURE_AGGREGATOR'
    folder = 'MEASURE_DISPLAY_FOLDER'
    expression = 'EXPRESSION'
    data_type = 'DATA_TYPE'

    @property
    def schema(self):
        return "$system.MDSCHEMA_MEASURES"

    @property
    def where(self):
        return ' WHERE [CUBE_NAME] = @CubeName'  # need to specify only fields for our cube for all query types

    def internal_func_dict(self):
        return {
            self.__class__.type: (lambda x: 'Calculated' if x == '9' else 'Aggregate'),
            self.__class__.data_type: (lambda x: DBDataType(int(x)))
            }


class Level(DMVColumnBaseClass):
    """An enum to represent the metadata of a level object for use in dmv queries.
    description: the description field
    name: the name field
    caption: the caption field
    visible: the visible field
    type: the type field
    dimension: the dimension field
    hierarchy: the hierarchy field
    level_number: the level_number field 
    """
    _settings_ = NoAlias  # necessary for different fields with the same value but different func

    description = 'DESCRIPTION'
    name = 'LEVEL_NAME'
    caption = 'LEVEL_CAPTION'
    visible = 'LEVEL_IS_VISIBLE'
    type = 'LEVEL_TYPE'
    dimension = 'HIERARCHY_UNIQUE_NAME'
    hierarchy = 'HIERARCHY_UNIQUE_NAME'
    level_number = 'LEVEL_NUMBER'
    data_type = 'LEVEL_DBTYPE'

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
            self.__class__.type: (lambda x: LevelType(int(x)).name),
            self.__class__.data_type: (lambda x: DBDataType(int(x)))
        }


class DBDataType(Enum):

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'

    EMPTY = 0  # Indicates that no value was specified.
    INT1 = 16  # Indicates a one-byte signed integer.
    INT2 = 2  # Indicates a two-byte signed integer.
    INT4 = 3  # Indicates a four-byte signed integer.
    INT8 = 20  # Indicates an eight-byte signed integer.
    INT_UNSIGNED1 = 17  # Indicates a one-byte unsigned integer.
    INT_UNSIGNED2 = 18  # Indicates a two-byte unsigned integer.
    INT_UNSIGNED4 = 19  # Indicates a four-byte unsigned integer.
    INT_UNSIGNED8 = 21  # Indicates an eight-byte unsigned integer.
    FLOAT32 = 4  # Indicates a single-precision floating-point value.
    FLOAT64 = 5  # Indicates a double-precision floating-point value.
    CURRENCY = 6  # Indicates a currency value. Currency is a fixed-point number with four digits to the right of the decimal point and is stored in an eight-byte signed integer scaled by 10,000.
    DATE_DOUBLE = 7  # Indicates a date value. Date values are stored as Double, the whole part of which is the number of days since December 30, 1899, and the fractional part of which is the fraction of a day.
    BSTR = 8  # A pointer to a BSTR, which is a null-terminated character string in which the string length is stored with the string.
    IDISPATCH = 9  # Indicates a pointer to an IDispatch interface on an OLE object.
    ERROR_CODE = 10  # Indicates a 32-bit error code.
    BOOL = 11  # Indicates a Boolean value.
    VARIANT = 12  # Indicates an Automation variant.
    IUNKNOWN = 13  # Indicates a pointer to an IUnknown interface on an OLE object.
    DECIMAL = 14  # Indicates an exact numeric value with a fixed precision and scale. The scale is between 0 and 28.
    GUID = 72  # Indicates a GUID.
    BYTES = 128  # Indicates a binary value.
    STRING = 129  # Indicates a string value.
    WSTR = 130  # Indicates a null-terminated Unicode character string.
    NUMERIC = 131  # Indicates an exact numeric value with a fixed precision and scale. The scale is between 0 and 38.
    UDT = 132  # Indicates a user-defined variable.
    DATE = 133  # Indicates a date value (yyyymmdd).
    TIME = 134  # Indicates a time value (hhmmss).
    DATETIME = 135  # Indicates a date-time stamp (yyyymmddhhmmss plus a fraction in billionths).
    HCHAPTER = 136  # Indicates a four-byte chapter value used to identify rows in a child rowset.


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
    """Breaks down the various time levels supported in both atscale and ansi sql
    """
    _init_ = 'index, atscale_type, val, steps, sql_name'

    def get_sql_expression(self, col, platform_type):
        if self.sql_name == 'day' or self.sql_name == 'hour' or self.sql_name == 'minute' or self.sql_name == 'second':
            if platform_type == PlatformType.IRIS:
                return f'DATE({col})'
            elif platform_type == PlatformType.SYNAPSE or platform_type == PlatformType.MSSQL:
                return f'DATETRUNC({self.sql_name}, {col})'
            elif platform_type == PlatformType.DATABRICKS:
                return f'date_trunc("{self.sql_name}", {col})'
            elif platform_type == PlatformType.GBQ:
                return f'date_trunc( {col}, {self.sql_name})'
            else:
                return f'date_trunc({self.sql_name}, {col})'
        else:
            if platform_type == PlatformType.IRIS or platform_type == PlatformType.SYNAPSE or platform_type == PlatformType.MSSQL:
                return f'DATEPART({self.sql_name}, {col})'
            elif platform_type == PlatformType.DATABRICKS:
                return f'date_part("{self.sql_name}", {col})'
            elif platform_type == PlatformType.GBQ:
                return f'EXTRACT({self.sql_name} from {col})'
            else:
                return f'date_part({self.sql_name}, {col})'
                
    # Only handling AtScale time levels that are also in ANSI SQL and are date_trunc 
    # compatible right now; trying to be as generic as possible.
    Year = 0, 'TimeYears',20, [1, 2], 'year'
    Quarter = 1, 'TimeQuarters', 68, [1, 4], 'quarter'
    Month = 2, 'TimeMonths', 132, [1, 3, 6, 12], 'month'
    Week = 3, 'TimeWeeks', 260, [1, 4], 'week' #this one acts weird with date_trunc, so using date_part
    Day = 4, 'TimeDays', 516, [1, 7, 28], 'day'
    Hour = 5, 'TimeHours', 772, [1, 12, 24], 'hour'
    Minute = 6, 'TimeMinutes', 1028, [1, 60], 'minute'
    Second = 7, 'TimeSeconds', 2052, [1, 60], 'second'


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
    
    def __new__(cls, value, dict_expression):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.dict_expression = dict_expression
        return obj
    
    SUM = ('SUM', False)
    AVG = ('AVG', False)
    MAX = ('MAX', False)
    MIN = ('MIN', False)
    DISTINCT_COUNT = ('DC', True)
    DISTINCT_COUNT_ESTIMATE = ('DCE', True)
    NON_DISTINCT_COUNT = ('NDC', True)
    STDDEV_SAMP = ('STDDEV_SAMP', False)
    STDDEV_POP = ('STDDEV_POP', False)
    VAR_SAMP = ('VAR_SAMP', False)
    VAR_POP = ('VAR_POP', False)

    def get_dict_expression(self, id):
        if self.name == 'DISTINCT_COUNT':
            return {
                'count-distinct': {
                    'key-ref': {'id': id},
                    'approximate': False
                    }
                }
        elif self.name == 'DISTINCT_COUNT_ESTIMATE':
            return {
                'count-distinct': {
                    'key-ref': {'id': id},
                    'approximate': True
                    }
                }
        elif self.name == 'NON_DISTINCT_COUNT':
            return {
                'count-nonnull': {
                    'key-ref': {'id': id},
                    'approximate': False
                    }
                }
        else:
            return {}


class MDXAggs(Enum):
    """Holds constant string representations for the supported MDX aggregation methods
     SUM: Addition
     STANDARD_DEVIATION: standard deviation of the sample
     MEAN: Average
     MAX: Maximum
     MIN: Mininum
     """
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
    GBQ = 'bigquery'
    DATABRICKS = 'databrickssql'
    IRIS = 'iris'
    SYNAPSE = 'azuresqldw'
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
    def __new__(cls, value, name_val):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.name_val = name_val
        return obj
    
    ALL = (0, 'All')
    NUMERIC = (1, 'Numeric') 
    CATEGORICAL = (2, 'Categorical')

class RequestType(Enum):
    """Used for specifying type of http request"""
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class MappedColumnFieldTerminator(Enum):
    """ Used for specifying mapped column field delimiters"""
    comma = ','
    semicolon = ';'
    pipe = '|'


class MappedColumnKeyTerminator(Enum):
    """ Used for specifying mapped column key delimiters"""
    equals = '='
    colon = ':'
    caret = '^'

class MappedColumnDataTypes(Enum):
    """Used for specifying data type of mapped column"""
    Int = 'Int'
    Long = 'Long', 
    Boolean = 'Boolean'
    String = 'String'
    Float = 'Float'
    Double = 'Double'
    Decimal = 'Decimal'
    Datetime = 'DateTime'
    Date = 'Date'

class ScikitLearnModelType(Enum):
    """ Used for specifying type of model being written to AtScale """
    LINEARREGRESSION = 'LinearRegression'
    LOGISTICREGRESSION = 'LogisticRegression'
