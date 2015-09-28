import json
from pawavip.success.store import Store
from unittest import TestCase
from .core import fixture_file_path
from nose.tools import *

class StoreTests(TestCase):
    # : :type: Store
    store = None

    def setUp(self):
        self.store = Store()

    def test_number(self):
        path = fixture_file_path('store.json')
        self.store.restore_from(path)

        self.store.add('hoge', 2)

        eq_(self.store.get_value('hoge'), 2)

        self.store.sub('hoge', 1)
        eq_(self.store.get_value('hoge'), 1)

        self.store.set_value('hoge', 70)

        eq_(self.store.get_value('hoge'), 70)

        ok_(self.store.le('hoge', 71))
        ok_(self.store.le('hoge', 70))
        ok_(not self.store.le('hoge', 69))

        ok_(self.store.ge('hoge', 69))
        ok_(self.store.ge('hoge', 70))
        ok_(not self.store.ge('hoge', 71))

    def test_switch(self):
        path = fixture_file_path('store.json')
        self.store.restore_from(path)
        ok_(not self.store.on('fuga'))

        self.store.set_on('fuga')

        ok_(self.store.on('fuga'))

        self.store.set_off('fuga')

        ok_(not self.store.on('fuga'))

    def test_list(self):
        path = fixture_file_path('store.json')
        self.store.restore_from(path)

        self.store.append('foo', 'aaa')

        eq_(tuple(self.store.get_value('foo')), ('aaa', ))

        self.store.append('foo', 'bbb')
        eq_(tuple(self.store.get_value('foo')), ('aaa', 'bbb'))

        self.store.extend('foo', ('ccc', 'ddd'))
        eq_(tuple(self.store.get_value('foo')), ('aaa', 'bbb', 'ccc', 'ddd'))

        self.store.remove('foo', 'ccc')
        eq_(tuple(self.store.get_value('foo')), ('aaa', 'bbb', 'ddd'))

        self.store.remove('foo', 'ccc')
