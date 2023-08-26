from enum import Enum


class LevelType(Enum):
    """Translates the numeric level indicator from the model json into a string form
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

   
class TimeSteps (Enum): 
    """Translates the time levels into usable step sizes.
    """
    TimeSeconds = [1, 60]
    TimeMinutes = [1, 60]
    TimeHours = [1, 12, 24]
    TimeDays = [1, 7, 28]
    TimeWeeks = [1, 4]
    TimeMonths = [1, 3, 6, 12]
    TimeQuarters =  [1, 4]
    TimeTrimesters = [1, 3]
    TimeHalfYears = [1, 2]
    TimeYears = [1, 2]


class Aggs(Enum):
    """Holds constant string representations for the supported aggregation methods of numerical features
    as of Jan 28, 2022 ... DC = distinct count (excluding duplicates) DCE = distinct count estimate
    NDC = Non-Distinct Count ..."""
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