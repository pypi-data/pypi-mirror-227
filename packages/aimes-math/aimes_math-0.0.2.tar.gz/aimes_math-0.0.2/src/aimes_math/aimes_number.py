from .aimes_table import AIMESTable


class AIMESNumber(float):
    def __lt__(self, other):
        if isinstance(other, AIMESTable):
            for k, v in other.items():
                if not super().__lt__(v):
                    return False
        elif isinstance(other, AIMESNumber):
            return super().__lt__(other)
        else:
            return False
        return True

    def __le__(self, other):
        if isinstance(other, AIMESTable):
            for k, v in other.items():
                if not super().__le__(v):
                    return False
        elif isinstance(other, AIMESNumber):
            return super().__le__(other)
        else:
            return False
        return True

    def __gt__(self, other):
        if isinstance(other, AIMESTable):
            for k, v in other.items():
                if not super().__gt__(v):
                    return False
        elif isinstance(other, AIMESNumber):
            return super().__gt__(other)
        else:
            return False
        return True

    def __ge__(self, other):
        if isinstance(other, AIMESTable):
            for k, v in other.items():
                if not super().__ge__(v):
                    return False
        elif isinstance(other, AIMESNumber):
            return super().__ge__(other)
        else:
            return False
        return True

    def __add__(self, other):
        self.__check_other(other)
        if isinstance(other, AIMESTable):
            result = AIMESTable()
            for elem, count in other.items():
                new_count = self + other[elem]
                result[elem] = new_count
            return result
        return super().__add__(other)

    def __sub__(self, other):
        self.__check_other(other)
        if isinstance(other, AIMESTable):
            result = AIMESTable()
            for elem, count in other.items():
                new_count = self * other[elem]
                result[elem] = new_count
            return result
        return super().__sub__(other)

    def __mul__(self, other):
        self.__check_other(other)
        if isinstance(other, AIMESTable):
            result = AIMESTable()
            for elem, count in other.items():
                new_count = self * other[elem]
                result[elem] = new_count
            return result
        return super().__mul__(other)

    def __truediv__(self, other):
        self.__check_other(other)
        if isinstance(other, AIMESTable):
            result = AIMESTable()
            for elem, count in other.items():
                new_count = self / other[elem]
                result[elem] = new_count
            return result
        return super().__truediv__(other)

    def __pow__(self, other):
        self.__check_other(other)
        if isinstance(other, AIMESTable):
            result = AIMESTable()
            for elem, count in other.items():
                new_count = self ** other[elem]
                result[elem] = new_count
            return result
        return super().__pow__(other)

    def __iadd__(self, other):
        if isinstance(other, AIMESTable):
            for elem, count in other.items():
                self[elem] += self
        else:
            for elem, count in self.items():
                self[elem] += other
        return self

    def __isub__(self, other):
        if isinstance(other, AIMESTable):
            for elem, count in other.items():
                self[elem] -= self
        else:
            for elem, count in self.items():
                self[elem] -= other
        return self

    def __imul__(self, other):
        if isinstance(other, AIMESTable):
            for elem, count in other.items():
                self[elem] *= self
        else:
            for elem, count in self.items():
                self[elem] *= other
        return self

    def __itruediv__(self, other):
        if isinstance(other, AIMESTable):
            for elem, count in other.items():
                self[elem] /= self
        else:
            for elem, count in self.items():
                self[elem] /= other
        return self

    def __ipow__(self, other):
        if isinstance(other, AIMESTable):
            for elem, count in other.items():
                self[elem] **= self
        else:
            for elem, count in self.items():
                self[elem] **= other
        return self

    def __check_other(self, other):
        if not isinstance(other, AIMESTable | int | float):
            raise TypeError(f"Object is not a number, it is {type(other)}")
