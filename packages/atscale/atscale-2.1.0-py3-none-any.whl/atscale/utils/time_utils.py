"""Module for handling SQL and AtScale Date and Time objects"""

from atscale.db.sql_connection import SQLConnection
from atscale.base.enums import TimeLevels

def determine_time_levels(dbconn: SQLConnection, table_name: str, column: str):
    # TODO
    # This is a direct connect to the database and querying it rather than through atscale which feels pretty dangerous.
    # I'd rather be doing this through atscale so there's a central point managing all the sql translation. So maybe use
    # jdbc for this in the future? Totally open, just speculating.

    # TimeLevels are numbered at 0 for Year and then go down from there. We'll set the top to year then
    # iterate through the options and query the db to figure out where the top and bottom levels are.
    top = None
    bottom = None
    num = len(TimeLevels)-1
    last_distinct = None  
    for level in TimeLevels:  # this starts at years and works down
        expression = level.get_sql_expression(column, dbconn.platform_type)
        query = f'SELECT count(distinct({expression})) FROM {table_name}'
        df = dbconn.submit_query(query)
        # Grab the one value from the df which is the count of distinct values at this aggregation level.
        distinct = df.iat[0, 0]
        if distinct > 1:
            if not top:  # if top is None, meaning we haven't found it yet
                # Then this is the first level where there is more than one unique value, which means the level
                # above this one is the top. The top will have only one unique value, and aggregate everything.
                #if we're at top, we can't go any higher so will just set that as top
                if level == TimeLevels.Year:
                    top = TimeLevels.Year
                else:
                    #otherwise, top is the level above the current level in this loop
                    top = [l for l in TimeLevels if l.index == (level.index-1)][0]
                if top.index == num: #if top is the penultimate item in the enum (currently minutes), then add the last one (currently seconds), which should be level in this loop (right after setting top in the last one)
                    bottom = level
                    break
            elif distinct == last_distinct:
                # If two consecutive values have the same distinct value (using date_trunc), then the last value we looked at was the bottom
                bottom = [l for l in TimeLevels if l.index == level.index-1][0] 
                break
        last_distinct = distinct

    # We should now have the top and bottom levels.
    # There should be  better way of doing this, but trying to go fast and being a bit sloppy
    levels = [level for level in TimeLevels if top.index <=
              level.index <= bottom.index]
    return levels
