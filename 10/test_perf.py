#! /usr/bin/env python3

import json
import time

import ujson

import cjson


def generate_json_str():
    "Generates json string with 1000 keys and 1000 values"

    json_str = "{"

    for i in range(1, 1001):
        if i % 2:
            json_str += f'"key{i}": "value{i}", '
        else:
            json_str += f'"key{i}": {i}, '
    json_str = json_str[:-2]
    json_str += "}"

    return json_str


def main():
    json_str = generate_json_str()

    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)

    start = time.perf_counter()
    for _ in range(1000):
        json.loads(json_str)
    end = time.perf_counter()
    print(f"json.loads: {end - start :.3f}s")

    start = time.perf_counter()
    for _ in range(1000):
        ujson.loads(json_str)
    end = time.perf_counter()
    print(f"ujson.loads: {end - start :.3f}s")

    start = time.perf_counter()
    for i in range(1000):
        cjson.loads(json_str)
    end = time.perf_counter()
    print(f"cjson.loads: {end - start :.3f}s")

    start = time.perf_counter()
    for _ in range(1000):
        json.dumps(json_doc)
    end = time.perf_counter()
    print(f"json.dumps: {end - start :.3f}s")

    start = time.perf_counter()
    for _ in range(1000):
        ujson.dumps(ujson_doc)
    end = time.perf_counter()
    print(f"ujson.dumps: {end - start :.3f}s")

    start = time.perf_counter()
    for _ in range(1000):
        cjson.dumps(cjson_doc)
    end = time.perf_counter()
    print(f"cjson.dumps: {end - start :.3f}s")


if __name__ == "__main__":
    main()
