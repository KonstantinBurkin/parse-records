import polars as pl
from polars import col as c
import re


def regex_search(
    regex_string: str,
    column: str,
    dataframe: pl.DataFrame,
) -> pl.DataFrame:

    def search_condition(x):
        try:
            found = re.search(regex_string, x).group(1)
        except AttributeError:
            # match not found in the original string
            found = ""  # apply your error handling
        return found

    new_column = dataframe.with_columns(
        c(column)
        .map_elements(
            search_condition,
            return_dtype=str,
        )
        .alias("new_column")
    )["new_column"]

    return new_column
