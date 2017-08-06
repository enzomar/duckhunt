#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from duckhunt import duckhunt
from datetime import datetime
import pickle
import json


@duckhunt
class Passenger(object):
    a_str = str
    a_int = int
    a_list = list
    a_dict = dict
    a_tuple = tuple
    a_object = datetime


@duckhunt
class Bom(object):
    a_str = str
    a_int = int
    a_list = list
    a_dict = dict
    a_tuple = tuple
    a_object = datetime
    a_duckhunt = Passenger


class DuckhuntTest(unittest.TestCase):
    def setUp(self):
        self.bom = Bom()
        self.bom_populated = self.populate_bom()

    def populate_bom(self):
        b = Bom()
        p = Passenger()
        p.a_str = 'Pax Thomaç'

        b.a_str = '2344-cece-455'
        b.a_list = ['abc', 123, p]
        b.a_dict = dict()
        b.a_dict['key'] = 'value'
        b.a_tuple = (1, 2)
        b.a_object = datetime(1982, 1, 30  , 8, 30)
        b.a_duckhunt = p

        return b

    def test_not_set_attr(self):
        self.assertEqual(self.bom.a_str, None)
        self.assertEqual(self.bom.a_int, None)
        self.assertEqual(self.bom.a_list, None)
        self.assertEqual(self.bom.a_dict, None)
        self.assertEqual(self.bom.a_tuple, None)
        self.assertEqual(self.bom.a_object, None)
        self.assertEqual(self.bom.a_duckhunt, None)

    def test_wrong_types(self):
        with self.assertRaises(TypeError):
            self.bom.a_str = 0
        with self.assertRaises(TypeError):
            self.bom.a_int = ''
        with self.assertRaises(TypeError):
            self.bom.a_list = dict
        with self.assertRaises(TypeError):
            self.bom.a_dict = list()
        with self.assertRaises(TypeError):
            self.bom.a_tuple = 0
        with self.assertRaises(TypeError):
            self.bom.a_object = 0
        with self.assertRaises(TypeError):
            self.bom.a_duckhunt = 0

    def test_attribute_name_get(self):
        with self.assertRaises(AttributeError):
            self.bom.xxx

    def test_attribute_name_set(self):
        with self.assertRaises(AttributeError):
            self.bom.xxx = 0

    def test_pickle(self):
        ser = pickle.dumps(self.bom_populated)
        des_bom = pickle.loads(ser)
        ser2 = pickle.dumps(des_bom)
        self.assertEqual(ser, ser2)

    def test_stringify(self):
        print(self.bom_populated)
        bom_str = str(self.bom_populated)
        self.assertTrue('a_object' in bom_str)
        json.loads(bom_str)


if __name__ == '__main__':
    unittest.main()
