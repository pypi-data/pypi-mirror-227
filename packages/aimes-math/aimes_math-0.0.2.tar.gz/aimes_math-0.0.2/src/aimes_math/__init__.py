from types import NoneType
from typing import Literal


from .aimes_table import AIMESTable
from .aimes_number import AIMESNumber
from .operations import TableOperation


class AIMESObject:
    def __init__(
        self,
        obj: object,
        current_time: int,
        settings: dict = None,  # rows_settings:dict = { 0: ["x", "xx"] }
        aggregation_func: Literal["SUM", "COUNT", "MIN", "MAX"] = None,
    ) -> None:
        self.obj = obj
        self.current_time = current_time
        self.table_type: Literal["Matrix", "Vector"] = None
        self.obj_type = self.__get_obj_type()
        rows = None
        if settings:
            rows = settings.get("selected_rows")
        if rows and self.obj_type == dict:
            self.rows_settings = self.__parse_rows_settings(rows)
            self.__apply_time_offset()
            self.__apply_settings()
            self.aggregation_func: Literal[
                "SUM", "COUNT", "MIN", "MAX"
            ] = aggregation_func
            if aggregation_func:
                self.__apply_aggregation_func()
        elif not rows and self.obj_type == dict:
            try:
                self.obj = self.obj[self.current_time]
            except KeyError:
                self.obj = self.obj

    def __apply_settings(self):
        self.table_type = self.__get_table_type()
        match self.table_type:
            case "Matrix":
                self.__parse_matrix_with_time()
            case "Vector":
                self.__parse_matrix_without_time()

    def __apply_time_offset(self):
        settings = self.rows_settings
        TIME = self.current_time
        result_settings = {}
        for key, values in settings.items():
            key_ = TIME + key
            result_settings[key_] = settings[key]
        self.rows_settings = result_settings

    def __get_obj_type(self) -> float | int | dict:
        type_ = type(self.obj)
        if type_ == dict:
            if isinstance(
                self.obj.get(list(self.obj.keys())[0]), int | float | NoneType
            ):
                try:
                    type_ = float
                    result = self.obj[self.current_time]
                except KeyError:
                    type_ = dict
                    result = self.obj
                self.obj = result
        return type_

    def __get_table_type(self) -> Literal["Matrix", "Vector"]:
        settings: dict = self.rows_settings
        values = []
        for _, titles in settings.items():
            for title in titles:
                if title in values:
                    return "Matrix"
                values.append(title)
        return "Vector"

    def __parse_matrix_with_time(self):
        settings: dict = self.rows_settings
        table = self.obj
        result = {}
        for time, values in settings.items():
            temp_row = {}
            for value in values:
                temp_row[value] = table[time][value]
            result[time] = temp_row
        self.obj = result

    def __parse_matrix_without_time(self):
        settings: dict = self.rows_settings
        table = self.obj
        result = {}
        for time, values in settings.items():
            for value in values:
                result[value] = table[time][value]
        self.obj = result

    def __parse_rows_settings(self, rows_settings: dict):
        result = {}
        for title, value in rows_settings.items():
            if not value.get("selected"):
                continue
            for time in value.get("time"):
                if not result.get(time):
                    result[time] = []
                result[time].append(title)
        return result

    def __apply_aggregation_func(self):
        function = self.aggregation_func
        match function:
            case "SUM":
                self.get_sum()
            case "COUNT":
                self.get_number_of_rows()
            case "MAX":
                self.get_max()
            case "MIN":
                self.get_min()

    def get_sum(self):
        if not self.obj_type == dict:
            raise TypeError(f"Not a table.")
        match self.table_type:
            case "Matrix":
                self.obj = TableOperation.sum(self.obj)
            case "Vector":
                # self.obj = TableOperation.sum({self.current_time: self.obj})
                self.obj = TableOperation.sum(self.obj)

    def get_number_of_rows(self) -> int:
        if not self.obj_type == dict:
            raise TypeError(f"Not a table.")
        counter = 0
        for i in self.obj.values():
            if i:
                counter += 1
        self.obj = counter

    def get_min(self) -> float:
        if not self.obj_type == dict:
            raise TypeError(f"Not a table.")
        self.obj = min(self.obj.values())

    def get_max(self) -> float:
        if not self.obj_type == dict:
            raise TypeError(f"Not a table.")
        self.obj = max(self.obj.values())

    def get(self):
        if isinstance(self.obj, int | float):
            return AIMESNumber(self.obj)
        elif isinstance(self.obj, dict) and self.table_type == "Vector":
            return AIMESTable(self.obj)
        elif isinstance(self.obj, dict) and self.table_type == "Matrix":
            return self.obj
        elif isinstance(self.obj, dict) and not self.table_type:
            return AIMESTable(self.obj)
        else:
            return self.obj
