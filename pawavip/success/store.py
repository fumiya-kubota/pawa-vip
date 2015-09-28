import json
from numbers import Number


class Store(object):
    # type: :dict
    _data = None

    def save_to(self, file_name):
        with open(file_name, 'w') as fp:
            fp.write(json.dump(self._data))

    def restore_from(self, file_name):
        print file_name
        with open(file_name) as fp:
            self._data = json.load(fp)

    def get_value(self, key):
        return self._data.get(key)

    def set_value(self, key, value=None, value_func=None):
        if value_func is not None:
            self._data[key] = value_func(self._data.get(key))
        elif value is not None:
            self._data[key] = value

    def add(self, key, value):
        self.set_value(key, value_func=lambda v: v + value)

    def sub(self, key, value):
        self.set_value(key, value_func=lambda v: v - value)

    def append(self, key, value):
        val = self.get_value(key)
        if not isinstance(val, list):
            raise ValueError
        val.append(value)
        val.sort()

    def extend(self, key, values):
        val = self.get_value(key)
        if not isinstance(val, list):
            raise ValueError
        val.extend(values)
        val.sort()

    def remove(self, key, value):
        val = self.get_value(key)
        if not isinstance(val, list):
            raise ValueError
        if value in val:
            val.remove(value)
            val.sort()

    def set_on(self, key):
        self.set_value(key, value=True)

    def set_off(self, key):
        self.set_value(key, value=False)

    def on(self, key):
        return True if self.get_value(key) else False

    def le(self, key, value):
        val = self.get_value(key)
        if not isinstance(val, Number):
            raise ValueError
        return val <= value

    def ge(self, key, value):
        val = self.get_value(key)
        if not isinstance(val, Number):
            raise ValueError
        return val >= value
