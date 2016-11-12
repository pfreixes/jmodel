import timeit
import ujson
import _json

from jmodel.model import Model
from json.decoder import JSONObject, JSONArray
from json.scanner import py_make_scanner


class _ParserPython:
    object_hook = None
    object_pairs_hook = None
    parse_string = _json.scanstring
    parse_float = float
    parse_int = int
    parse_constant = None
    strict = True
    parse_object = JSONObject
    parse_array = JSONArray
    memo = {}


class _Parser:
    object_hook = None
    object_pairs_hook = None
    parse_float = float
    parse_int = int
    parse_constant = None
    strict = True


def pyjson_loads_lines(lines):
    scanner = py_make_scanner(_ParserPython)
    for line in lines:
        scanner(line, 0)


def json_loads_lines(lines):
    scanner = _json.make_scanner(_Parser)
    for line in lines:
        scanner(line, 0)


def jmodel_loads_lines(lines):
    for line in lines:
        Model.loads(line)


def ujson_loads_lines(lines):
    for line in lines:
        ujson.loads(line)


def json_loads(s):
    scanner = _json.make_scanner(_Parser)
    scanner(s, 0)


def jmodel_loads(s):
    Model.loads(s)


def ujson_loads(s):
    ujson.loads(s)


def pyjson_loads(s):
    scanner = py_make_scanner(_ParserPython)
    scanner(s, 0)


if __name__ == '__main__':
    with open('./benchmark/data/one-json-per-line.txt') as fd:
        lines = fd.readlines()

    print("Parsing many lines (lines %d) (Repeated 10 times)" % len(lines))
    print("------------------------------------------------")
    print("Time took Python json (Python version): {}".format(
        timeit.timeit("pyjson_loads_lines(lines)",
                      number=10,
                      setup="from __main__ import Model, lines, pyjson_loads_lines")
    ))
    print("Time took cythonized Python json: {}".format(
        timeit.timeit("jmodel_loads_lines(lines)",
                      number=10,
                      setup="from __main__ import Model, lines, jmodel_loads_lines")
    ))
    print("Time took Python json (C version) : {}".format(
        timeit.timeit("json_loads_lines(lines)",
                      number=10,
                      setup="from __main__ import lines, _json, json_loads_lines")
    ))
    print("Time took ujson: {}".format(
        timeit.timeit("ujson_loads_lines(lines)",
                      number=10,
                      setup="from __main__ import ujson, lines, ujson_loads_lines")
    ))

    print("")

    with open('./benchmark/data/huge-text.json') as fd:
        s = fd.read()

    print("Parsing huge-text file (size %d)" % len(s))
    print("------------------------------")
    print("Time took Python json (Python version): {}".format(
        timeit.timeit("pyjson_loads(s)", number=2, setup="from __main__ import Model, s, pyjson_loads")
    ))
    print("Time took cythonized Python json: {}".format(
        timeit.timeit("jmodel_loads(s)", number=2, setup="from __main__ import Model, s, jmodel_loads")
    ))
    print("Time took Python json (C version) : {}".format(
        timeit.timeit("json_loads(s)", number=2, setup="from __main__ import s, _json, json_loads")
    ))
    print("Time took ujson: {}".format(
        timeit.timeit("ujson_loads(s)", number=2, setup="from __main__ import ujson, s, ujson_loads")
    ))

    print("")

    with open('./benchmark/data/medium.json') as fd:
        s = fd.read()

    print("Parsing medium file (size %d)" % len(s))
    print("------------------------------")
    print("Time took Python json (Python version): {}".format(
        timeit.timeit("pyjson_loads(s)", number=5, setup="from __main__ import Model, s, pyjson_loads")
    ))
    print("Time took cythonized Python json: {}".format(
        timeit.timeit("jmodel_loads(s)", number=5, setup="from __main__ import Model, s, jmodel_loads")
    ))
    print("Time took Python json (C version) : {}".format(
        timeit.timeit("json_loads(s)", number=5, setup="from __main__ import s, _json, json_loads")
    ))
    print("Time took ujson: {}".format(
        timeit.timeit("ujson_loads(s)", number=5, setup="from __main__ import ujson, s, ujson_loads")
    ))

    with open('./benchmark/data/countries.json') as fd:
        s = fd.read()

    print("Parsing 243 countries file ")
    print("----------------------------")
    print("Time took Python json (Python version): {}".format(
        timeit.timeit("pyjson_loads(s)", number=5, setup="from __main__ import Model, s, pyjson_loads")
    ))
    print("Time took cythonized Python json: {}".format(
        timeit.timeit("jmodel_loads(s)", number=5, setup="from __main__ import Model, s, jmodel_loads")
    ))
    print("Time took Python json (C version) : {}".format(
        timeit.timeit("json_loads(s)", number=5, setup="from __main__ import s, _json, json_loads")
    ))
    print("Time took ujson: {}".format(
        timeit.timeit("ujson_loads(s)", number=5, setup="from __main__ import ujson, s, ujson_loads")
    ))
