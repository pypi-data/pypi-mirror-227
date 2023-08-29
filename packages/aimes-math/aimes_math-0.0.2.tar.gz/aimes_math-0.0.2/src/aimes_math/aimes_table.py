class AIMESTable(dict):
    def __eq__(self, other):
        if isinstance(other, float | int):
            for key, item in self.items():
                if item != other:
                    return False

        elif isinstance(other, AIMESTable):
            for key, item in self.items():
                if other[key] != item:
                    return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, float | int):
            for key, item in self.items():
                if float(item) <= float(other):
                    return False

        elif isinstance(other, AIMESTable):
            for key, item in self.items():
                if float(item) <= float(other[key]):
                    return False

        return True

    def __ge__(self, other):
        if isinstance(other, float | int):
            for key, item in self.items():
                if float(item) < float(other):
                    return False

        elif isinstance(other, AIMESTable):
            for key, item in self.items():
                if float(item) < float(other[key]):
                    return False

        return True

    def __lt__(self, other):
        if isinstance(other, float | int):
            for key, item in self.items():
                if float(item) >= float(other):
                    return False

        elif isinstance(other, AIMESTable):
            for key, item in self.items():
                if float(item) >= float(other[key]):
                    return False

        return True

    def __le__(self, other):
        if isinstance(other, float | int):
            for key, item in self.items():
                if float(item) > float(other):
                    return False

        elif isinstance(other, AIMESTable):
            for key, item in self.items():
                if float(item) > float(other[key]):
                    return False

        return True

    def __add__(self, other):
        self.__check_other(other)
        result = AIMESTable()
        if isinstance(other, AIMESTable) and isinstance(self, AIMESTable):
            if len(list(other.keys())) > len(list(self.keys())):
                self, other = other, self
        for elem, count in self.items():
            if isinstance(other, AIMESTable):
                if not other.get(elem):
                    new_count = count
                else:
                    new_count = count + other[elem]
            else:
                new_count = count + other
            result[elem] = new_count
        return result

    def __sub__(self, other):
        self.__check_other(other)
        result = AIMESTable()
        if isinstance(other, AIMESTable) and isinstance(self, AIMESTable):
            if len(list(other.keys())) > len(list(self.keys())):
                self, other = other, self
        for elem, count in self.items():
            if isinstance(other, AIMESTable):
                if not other.get(elem):
                    new_count = count
                else:
                    new_count = count - other[elem]
            else:
                new_count = count - other
            result[elem] = new_count
        return result

    def __mul__(self, other):
        self.__check_other(other)
        result = AIMESTable()
        if isinstance(other, AIMESTable) and isinstance(self, AIMESTable):
            if len(list(other.keys())) > len(list(self.keys())):
                self, other = other, self
        for elem, count in self.items():
            if isinstance(other, AIMESTable):
                if not other.get(elem):
                    new_count = count
                else:
                    new_count = count * other[elem]
            else:
                new_count = count * other
            result[elem] = new_count
        return result

    def __truediv__(self, other):
        self.__check_other(other)
        result = AIMESTable()
        if isinstance(other, AIMESTable) and isinstance(self, AIMESTable):
            if len(list(other.keys())) > len(list(self.keys())):
                self, other = other, self
        for elem, count in self.items():
            if isinstance(other, AIMESTable):
                if not other.get(elem):
                    new_count = count
                else:
                    new_count = count / other[elem]
            else:
                new_count = count / other
            result[elem] = new_count
        return result

    def __pow__(self, other):
        self.__check_other(other)
        result = AIMESTable()
        if isinstance(other, AIMESTable) and isinstance(self, AIMESTable):
            if len(list(other.keys())) > len(list(self.keys())):
                self, other = other, self
        for elem, count in self.items():
            if isinstance(other, AIMESTable):
                if not other.get(elem):
                    new_count = count
                else:
                    new_count = count ** other[elem]
            else:
                new_count = count**other
            result[elem] = new_count
        return result

    def __iadd__(self, other):
        if isinstance(other, AIMESTable):
            for elem, count in other.items():
                self[elem] += count
        else:
            for elem, count in self.items():
                self[elem] += other
        return self

    def __isub__(self, other):
        if isinstance(other, AIMESTable):
            for elem, count in other.items():
                self[elem] -= count
        else:
            for elem, count in self.items():
                self[elem] -= other
        return self

    def __imul__(self, other):
        if isinstance(other, AIMESTable):
            for elem, count in other.items():
                self[elem] *= count
        else:
            for elem, count in self.items():
                self[elem] *= other
        return self

    def __itruediv__(self, other):
        if isinstance(other, AIMESTable):
            for elem, count in other.items():
                self[elem] /= count
        else:
            for elem, count in self.items():
                self[elem] /= other
        return self

    def __ipow__(self, other):
        if isinstance(other, AIMESTable):
            for elem, count in other.items():
                self[elem] **= count
        else:
            for elem, count in self.items():
                self[elem] **= other
        return self

    def __check_other(self, other):
        if not isinstance(other, AIMESTable | int | float):
            raise TypeError(f"Object is not a number, {type(other)} was given.")
