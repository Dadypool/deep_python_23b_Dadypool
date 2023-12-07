#include <Python.h>


static PyObject *cjson_loads(PyObject *self, PyObject *args) {
    const char *json_str;

    // Парсим аргументы
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        PyErr_SetString(PyExc_TypeError, "Expected object or value");
        return NULL;
    }

    json_str = strdup(json_str);

    // Разделители
    const char *delimiter = ": ,\"{}";

    // Создаем новый словарь
    PyObject *dict = PyDict_New();
    if (dict == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create dictionary");
        return NULL;
    }
    
    char *key = NULL;
    char *value = NULL;
    char *token = strtok((char *)json_str, delimiter);

    while (token != NULL) {
        if(key == NULL) {
            key = strdup(token);
        } else if (value == NULL) {
            value = strdup(token);
        } else {
            PyErr_SetString(PyExc_RuntimeError, "Failed parsing json string");
            return NULL;
        }

        // Следующий токен
        token = strtok(NULL, delimiter);

        // Завершение элемента, если найдены ключ и значение
        if (key != NULL && value != NULL) {
            // Преобразование значения в PyObject
            PyObject *py_key;
            PyObject *py_value;
            
            if (!(py_key = Py_BuildValue("s", key))) {
                PyErr_SetString(PyExc_RuntimeError, "Failed to build string key");
                return NULL;
            }

            // Если значение - число
            if (isdigit(value[0]) || (value[0] == '-' && isdigit(value[1]))) {
                if (!(py_value = Py_BuildValue("i", atoi(value)))) {
                    PyErr_SetString(PyExc_RuntimeError, "Failed to build int value");
                    return NULL;
                }
            // Иначе, значение - строка
            } else {
                if (!(py_value = Py_BuildValue("s", value))) {
                    PyErr_SetString(PyExc_RuntimeError, "Failed to build string value");
                    return NULL;
                }
            }

            // Установка значения в словаре
            if (PyDict_SetItem(dict, py_key, py_value) < 0) {
                PyErr_SetString(PyExc_RuntimeError, "Failed to set item");
                return NULL;
            }

            // Освобождение памяти
            free(key);
            free(value);
            Py_DECREF(py_key);
            Py_DECREF(py_value);

            // Сброс указателей
            key = NULL;
            value = NULL;
        }
    }

    return dict;
}

static PyObject *cjson_dumps(PyObject *self, PyObject *args) {
    PyObject *pyDict;

    // Парсинг аргументов
    if (!PyArg_ParseTuple(args, "O", &pyDict)) {
        PyErr_SetString(PyExc_TypeError, "Expected python dictionary");
        return NULL;
    }

    PyObject *jsonStr = PyUnicode_FromString("{");

    PyObject *key, *value;
    Py_ssize_t pos = 0;

    // Перебираем все элементы словаря
    while (PyDict_Next(pyDict, &pos, &key, &value)) {
        // Объединяем JSON-представление ключа
        PyObject *keyStr = PyUnicode_FromFormat("\"%s\": ", PyUnicode_AsUTF8(PyObject_Str(key)));
        PyObject *valueStr = PyObject_Str(value);

        // Если значение - строка, добавляем его с двойными кавычками
        if (PyUnicode_Check(value)) {
            valueStr = PyUnicode_FromFormat("\"%s\"", PyUnicode_AsUTF8(valueStr));
        }

        // Объединяем JSON-представление ключа и значения
        jsonStr = PyUnicode_Concat(jsonStr, keyStr); 
        jsonStr = PyUnicode_Concat(jsonStr, valueStr); 
        jsonStr = PyUnicode_Concat(jsonStr, PyUnicode_FromString(", "));

        Py_XDECREF(keyStr);
        Py_XDECREF(valueStr);
    }

    // Удаляем последнюю запятую и добавляем закрывающую фигурную скобку
    jsonStr = PyUnicode_Substring(jsonStr, 0, PyUnicode_GetLength(jsonStr) - 2);
    jsonStr = PyUnicode_FromFormat("%s}", PyUnicode_AsUTF8(jsonStr));

    return jsonStr;
}


static PyMethodDef methods[] = {
    {"loads", cjson_loads, METH_VARARGS, "Parse JSON string to dictionary"},
    {"dumps", cjson_dumps, METH_VARARGS, "Dump dictionary to JSON string"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef cjson = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    NULL,
    -1,
    methods};

PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&cjson);
}
