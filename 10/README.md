# Домашняя работа №10

### 1. Реализовал модуль cjson с помощью C API - [cjson.c](https://github.com/Dadypool/deep_python_23b_Dadypool/blob/main/11/cjson.c)
### 2. Написал Makefile - [Makefile](https://github.com/Dadypool/deep_python_23b_Dadypool/blob/main/11/Makefile)
### 3. Написал тесты для модуля - [test_cjson.py](https://github.com/Dadypool/deep_python_23b_Dadypool/blob/main/11/test_cjson.py)
### 4. Написал тест производительности - [test_perf.py](https://github.com/Dadypool/deep_python_23b_Dadypool/blob/main/11/test_perf.py)

## Полученные результаты:
    json.loads: 0.174s
    ujson.loads: 0.153s
    cjson.loads: 0.440s

    json.dumps: 0.163s
    ujson.dumps: 0.129s
    cjson.dumps: 14.145s
### Итог: проигрывает по скорости обоим модулям. С dumps вообще всё плохо, скорее всего, связано с конкатенацией и форматированием - происходят через питоновские функции PyUnicode_Concat и PyUnicode_FromFormat