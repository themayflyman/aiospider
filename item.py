#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pformat


class Field:
    """Container of field metadata"""

    def __init__(self, default=None):
        self.default = default


class ItemMeta(type):

    def __new__(cls, name, bases, attrs):
        tmp_class = type.__new__(cls, name, bases, attrs)
        fields = getattr(tmp_class, 'fields', {})
        _default_values = getattr(tmp_class, '_default_values', {})
        for k, v in attrs.items():
            if isinstance(v, Field):
                fields[k] = v
                if v.default != None:
                    _default_values[k] = v.default

        attrs['fields'] = fields
        attrs['_default_values'] = _default_values

        return type.__new__(cls, name, bases, attrs)  


class Item(metaclass=ItemMeta):

    fields = {}
    _default_values = {}

    def __init__(self, *args, **kwargs):
        self._values = self._default_values.copy()
        if args or kwargs:
            for k, v in dict(*args, **kwargs).items():
                self._values[k] = v

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        if key in self.fields:
            self._values[key] = value
        else:
            raise KeyError('{} has no field: {}'.format(
                           self.__class__.__name__, key))

    def __delitem__(self, key):
        del self._values[key]

    def __getattr__(self, name):
        if name in self.fields:
            raise AttributeError('Use {}[{}] to get field value'.format(
                                 self.__class__.__name__, name))
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            raise AttributeError('Use {}[{}] = {} to set field value'.format(
                                 self.__class__.__name__, name, value))
        super(Item, self).__setattr__(name, value)

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def keys(self):
        return self._values.keys()

    def __repr__(self):
        return pformat(dict(self))

    def get(self, key):
        return self._values.get(key)


class Node(Item):
    """
    Node object for Spider to crawl.
    """
    id = Field()
    url = Field()
    method = Field()
    params = Field()
    json = Field()
    proxy_type = Field(default='http')
    retry = Field(default=0)



if __name__ == '__main__':
    n = Node(url='')
