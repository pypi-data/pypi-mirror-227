import math


class TableOperation:
    """

    This code defines a class called "TableOperation" with several methods for performing operations on tables.
    The class imports the "math" module and uses the "typing" module to specify a List data type.

    The methods included in the class are as follows:

        - row_sum(): takes table as a dictionary, a list of titles, and a list of dates,
          and returns a dictionary of sums of each title across all rows with the given dates.

        - time_sum(): takes table as a dictionary, a list of titles, and a list of dates,
          and returns a dictionary of sums of each date across all rows with the given titles.

        - row_mul(): takes table as a dictionary, a list of titles, and a list of dates,
          and returns a dictionary of products of each title across all rows with the given dates.

        - time_mul(): takes table as a dictionary, a list of titles, and a list of dates,
          and returns a dictionary of products of each date across all rows with the given titles.

        - ln(): takes table as a dictionary, a list of titles, and a list of dates,
          and returns a dictionary of natural logarithms of each value for each title and date in the table.

        - lg(): takes table as a dictionary, a list of titles, and a list of dates,
          and returns a dictionary of base-10 logarithms of each value for each title and date in the table.


    Each method takes in table as a dictionary,
    where each key represents a date and each value is a dictionary of titles and corresponding values.
    The methods then iterate through the rows specified by the given date or title lists,
    compute the desired operation, and return a dictionary with the resulting values.

    """

    ### -------------- SUM/MUL --------------

    def sum(table: dict) -> float:
        return TableOperation.sum_row(table)

    def sum_row(table: dict) -> float:  # {0: {"x": 1, "y": 2}, 1:{"x": 2}}
        if isinstance(table, int | float):
            raise TypeError("Number was given, must be Data-Node.")
        table_sum: float = 0.0

        for time, value in table.items():
            # for row in value.values():
            table_sum += value

        return table_sum

    def sum_time(table: dict) -> float:
        if isinstance(table, int | float):
            raise TypeError("Number was given, must be Data-Node.")
        result_table = {}
        for k, v in table.items():
            if isinstance(v, int | float):
                return table
            for k, value in v.items():
                if not result_table.get(k):
                    result_table[k] = 0
                result_table[k] += value
        return result_table

    def product(table: dict) -> float:
        table_product: float = 1

        for time, value in table.items():
            for row in value.values():
                table_product *= row

        return table_product

    def mul_row(table: dict) -> float:
        if isinstance(table, int | float):
            raise TypeError("Number was given, must be Data-Node.")
        table_product: float = 1

        for time, value in table.items():
            # for row in value.values():
            table_product *= value

        return table_product

    def mul_time(table: dict) -> dict:
        if isinstance(table, int | float):
            raise TypeError("Number was given, must be Data-Node.")
        result_table = {}
        for k, v in table.items():
            if isinstance(v, int | float):
                return table
            for k, value in v.items():
                if not result_table.get(k):
                    result_table[k] = 1
                result_table[k] *= value
        return result_table

    ### -------------- LN/LG --------------

    def ln(x: dict | float) -> dict | float:
        if isinstance(x, float | int):
            if x <= 0:
                raise ValueError(
                    f"Ln can be applied to number less more 0 or equaled 0. Table contains {x}."
                )
            return math.log(x, math.e)

        elif isinstance(x, dict):
            table_ln: dict = {key: None for key in x.keys()}

            for k, v in x.items():
                if v <= 0:
                    raise ValueError(
                        f"Ln can be applied to number more then 0 or equaled 0. Table contains {v}."
                    )
                table_ln[k] = math.log(v, math.e)
            return table_ln
        else:
            raise TypeError(f"Type {type(x)} is not supported.")

    def lg(x: dict | float) -> dict | float:
        if isinstance(x, float | int):
            if x <= 0:
                raise ValueError(
                    f"Lg can be applied to number more then 0 or equaled 0. Table contains {x}."
                )
            return math.log10(x)

        elif isinstance(x, dict):
            table_lg: dict = {key: None for key in x.keys()}
            for k, v in x.items():
                if v <= 0:
                    raise ValueError(
                        f"Lg can be applied to number more then 0 or equaled 0. Table contains {v}."
                    )
                table_lg[k] = math.log10(v)
            return table_lg
        else:
            raise TypeError(f"Type {type(x)} is not supported.")
