from typing import Any, TypeAlias

import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.api.types import (
    is_bool_dtype,
    is_numeric_dtype,
    is_object_dtype,
    is_string_dtype,
)
from selectolax.parser import HTMLParser

Dtype: TypeAlias = np.dtype | pd.api.extensions.ExtensionDtype | type
DtypeIndices: TypeAlias = dict[str, list[int]]


def get_dtype_category(dtype: Dtype) -> str:
    """Get the data type category for `dtype`.

    Parameters
    ----------
    dtype : Dtype
        Object whose data type category is to be determined.

    Returns
    -------
    str
        Data type category.
    """
    # Columns inferred as "object" type will be treated as strings.
    if is_object_dtype(dtype) or is_string_dtype(dtype):
        return "string"
    elif is_bool_dtype(dtype):
        return "boolean"
    elif is_numeric_dtype(dtype):
        return "numeric"
    else:
        return "other"


def get_dtype_indices(dtypes: list[Dtype]) -> DtypeIndices:
    """Build dict of type category and indices where that type occurs in a DataFrame.

    Parameters
    ----------
    dtypes : list[Dtype]
        List containing data types of an index (row or column).

    Returns
    -------
    DtypeIndices
        Indices for each data type category with the categories as keys.
    """
    dtype_indices = {
        "string": [],
        "boolean": [],
        "numeric": [],
    }

    for index, dtype in enumerate(dtypes):
        dtype_category = get_dtype_category(dtype=dtype)
        if dtype_category in dtype_indices:
            dtype_indices[dtype_category].append(index)

    return dtype_indices


def combine_indices(
    index_indices: list[int], column_indices: list[int], index_levels: int
) -> list[int]:
    """Combine data type indices for the index and columns of a DataFrame into one list.

    The row index of an html table is being treated as another column or set of columns
    (if hierarchical) in addition to the normal columns. Therefore, data type indices
    for the row index (`index_indices`) need to be combined with the ones from the
    normal columns (`column_indices`). `index_levels` is used to shift the
    `column_indices` values to account for this new indexing (row index plus normal
    columns) prior to doing the combination.

    Note: Every index value (range(len(`index_indices`) + len(`column_indices`))) does
    not need to be present in the arguments or in the return value of this function. A
    given index value is only present if the corresponding "column" is of the given data
    type category currently being processed (see the calling function for the current
    data type category being processed).

    Parameters
    ----------
    index_indices : list[int]
        Indices of the row index.
    column_indices : list[int]
        Indices of the columns.
    index_levels : int
        Number of levels of the row index.

    Returns
    -------
    list[int]
        Combined indices.
    """
    combined_indices = index_indices.copy()
    # The list comprehension shifts the values of `column_indices` so that there is no
    # overlap in the values coming from `index_indices` with the values from
    # `column_indices` in the combination.
    combined_indices.extend([index + index_levels for index in column_indices])

    return combined_indices


def get_full_table_dtype_indices(df: DataFrame, index: bool) -> DtypeIndices:
    """Retrieve combined data type indices for the index and columns of `df`.

    Parameters
    ----------
    df : DataFrame
        DataFrame an html table will be created from.
    index : bool
        Boolean indicating whether or not to include the row index indices in the return
        value.

    Returns
    -------
    DtypeIndices
        Data categories and their indices within `df` (index and column indices
        combined).
    """
    index_dtypes: list[Dtype]

    if index is False:
        # If DataFrame has column names.
        if any(name is not None for name in df.columns.names):
            index_dtypes = [pd.Series(df.columns.names).dtype]
            # Column names take up an extra column to the left of the data columns,
            # therefore `index_levels` is set to 1 to account for this.
            index_levels = 1
        # If DataFrame does not have column names.
        else:
            index_dtypes = []
            index_levels = 0
    else:
        # Row index dtypes are accessed differently based on whether it is a MultiIndex
        # or not.
        if isinstance(df.index, pd.MultiIndex):
            index_dtypes = df.index.dtypes.to_list()
        else:
            index_dtypes = [df.index.dtype]

        index_levels = df.index.nlevels

    index_dtype_indices = get_dtype_indices(dtypes=index_dtypes)
    column_dtype_indices = get_dtype_indices(dtypes=df.dtypes)

    # The data structures are zipped in order to pass the data corresponding to the same
    # data type category to `combine_indices()`.
    zip_indices = zip(
        index_dtype_indices.keys(),
        index_dtype_indices.values(),
        column_dtype_indices.values(),
    )

    indices = {}

    for category, index_indices, column_indices in zip_indices:
        indices[category] = combine_indices(
            index_indices=index_indices,
            column_indices=column_indices,
            index_levels=index_levels,
        )

    return indices


def align_table_columns_horizontally(
    table_html: str, dtype_indices: DtypeIndices
) -> str:
    """Align columns horizontally with Bootstrap classes based on data type of column.

    Parameters
    ----------
    table_html : str
        Html string representing the table.
    dtype_indices : DtypeIndices
        Data type categories and the indices where they occur in the table.

    Returns
    -------
    str
        Updated table html string.
    """
    parser = HTMLParser(table_html)
    # Find all table rows including the header row(s).
    table_rows = parser.css("tr")

    rowspan_shift_remaining = 0

    for table_row in table_rows:
        # The amount of index shift that a row index node with a rowspan attribute
        # creates is 1 for each row (it is constant per row). The total number of index
        # shifts (i.e. total number of rows affected) is the value of the rowspan
        # attribute minus 1. The shift does not affect the row in which the rowspan
        # attribute is encountered, it affects only subsequent rows. As each row shift
        # is completed, `rowspan_shift_remaining` is decremented until 0 is reached.
        if rowspan_shift_remaining > 0:
            rowspan_shift_remaining -= 1
            rowspan_shift = 1
        else:
            rowspan_shift = 0
        # `colspan_shift` is reset for each row since column index nodes with a colspan
        # attribute only affect the row in which they show up.
        colspan_shift = 0

        for col, child_node in enumerate(table_row.iter()):
            if "colspan" in child_node.attributes:
                # Index shift of a colspan node is the colspan value minus 1. The +=
                # operator is used because if multiple colspan nodes are encountered
                # while still on the same row, index shift will stack for all nodes
                # remaining in that row.
                colspan_shift += int(child_node.attrs["colspan"]) - 1
                # Column index nodes with a colspan attribute are centered horizontally.
                child_node.attrs["class"] = "text-center"
                # Remove deprecated html attribute "halign".
                try:
                    del child_node.attrs["halign"]
                except KeyError:
                    print("The attribute 'halign' was not found within this node.")
            elif "rowspan" in child_node.attributes:
                # Index shift of rowspan node is the rowspan value minus 1.
                rowspan_shift_remaining = int(child_node.attrs["rowspan"]) - 1
                # Row index nodes with a colspan attribute are centered vertically.
                child_node.attrs["class"] = "align-middle"
                # Remove deprecated html attribute "valign".
                try:
                    del child_node.attrs["valign"]
                except KeyError:
                    print("The attribute 'valign' was not found within this node.")
            else:
                # Adjust the index by any shifts due to rowspan/colspan nodes.
                index = col + rowspan_shift + colspan_shift

                if index in dtype_indices["string"]:
                    # Left align strings.
                    child_node.attrs["class"] = "text-start"
                elif index in dtype_indices["boolean"]:
                    # Center align booleans.
                    child_node.attrs["class"] = "text-center"
                elif index in dtype_indices["numeric"]:
                    # Right align numerics.
                    child_node.attrs["class"] = "text-end"

    return parser.css_first("table").html


def convert_frame_to_html(df: DataFrame, **to_html_kwargs: Any) -> str:
    """Convert DataFrame to html table, include bootstrap classes for text alignment.

    Parameters
    ----------
    df : DataFrame
        DataFrame to be converted to an html table.
    **to_html_kwargs : Any
        Keyword arguments passed directly to `df.to_html()`.

    Returns
    -------
    str
        Html table string.
    """
    # Starting html table string.
    table_html = df.to_html(**to_html_kwargs)

    index = to_html_kwargs.get("index", True)
    if not isinstance(index, bool):
        raise TypeError("`index` must be of type `bool`.")

    dtype_indices = get_full_table_dtype_indices(df, index=index)

    updated_table_html = align_table_columns_horizontally(
        table_html=table_html, dtype_indices=dtype_indices
    )

    return updated_table_html
