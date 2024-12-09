#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to parse a JSON string and return a Python dictionary (loads)
static PyObject* custom_json_loads(PyObject* self, PyObject* args) {
    const char* json_str;
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        PyErr_SetString(PyExc_TypeError, "Expected a JSON string");
        return NULL;
    }

    if (json_str[0] != '{' || json_str[strlen(json_str) - 1] != '}') {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }

    PyObject* dict = PyDict_New();
    if (!dict) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to create dictionary");
        return NULL;
    }

    const char* ptr = json_str + 1;  // Skip the opening brace
    while (*ptr) {
        while (*ptr == ' ' || *ptr == '\n' || *ptr == ',') ptr++;  // Skip spaces and commas
        if (*ptr == '}') break;  // End of JSON object

        // Parse key
        if (*ptr != '\"') {
            Py_DECREF(dict);
            PyErr_Format(PyExc_TypeError, "Invalid JSON key");
            return NULL;
        }
        const char* key_start = ++ptr;
        while (*ptr && *ptr != '\"') ptr++;
        if (!*ptr) {
            Py_DECREF(dict);
            PyErr_Format(PyExc_TypeError, "Unterminated JSON key");
            return NULL;
        }
        PyObject* key = PyUnicode_FromStringAndSize(key_start, ptr - key_start);
        ptr++;  // Skip closing quote

        // Skip colon
        while (*ptr == ' ') ptr++;
        if (*ptr != ':') {
            Py_DECREF(dict);
            Py_DECREF(key);
            PyErr_Format(PyExc_TypeError, "Expected ':' after key");
            return NULL;
        }
        ptr++;

        // Parse value
        while (*ptr == ' ') ptr++;
        PyObject* value = NULL;
        if (*ptr == '\"') {
            const char* value_start = ++ptr;
            while (*ptr && *ptr != '\"') ptr++;
            if (!*ptr) {
                Py_DECREF(dict);
                Py_DECREF(key);
                PyErr_Format(PyExc_TypeError, "Unterminated JSON value");
                return NULL;
            }
            value = PyUnicode_FromStringAndSize(value_start, ptr - value_start);
            ptr++;  // Skip closing quote
        } else if (*ptr == '-' || (*ptr >= '0' && *ptr <= '9')) {
            char* end_ptr;
            long num = strtol(ptr, &end_ptr, 10);  // Support negative numbers
            value = PyLong_FromLong(num);
            ptr = end_ptr;
        } else {
            Py_DECREF(dict);
            Py_DECREF(key);
            PyErr_Format(PyExc_TypeError, "Invalid JSON value");
            return NULL;
        }

        if (PyDict_SetItem(dict, key, value) < 0) {
            Py_DECREF(dict);
            Py_DECREF(key);
            Py_DECREF(value);
            return NULL;
        }
        Py_DECREF(key);
        Py_DECREF(value);
    }

    return dict;
}

static PyObject* custom_json_dumps(PyObject* self, PyObject* args) {
    PyObject* dict;
    if (!PyArg_ParseTuple(args, "O", &dict)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary");
        return NULL;
    }

    if (!PyDict_Check(dict)) {
        PyErr_SetString(PyExc_TypeError, "Argument must be a dictionary");
        return NULL;
    }

    PyObject* keys = PyDict_Keys(dict);
    PyObject* values = PyDict_Values(dict);
    if (!keys || !values) {
        Py_XDECREF(keys);
        Py_XDECREF(values);
        PyErr_SetString(PyExc_RuntimeError, "Failed to retrieve dictionary items");
        return NULL;
    }

    PyObject* result = PyUnicode_FromString("{");
    Py_ssize_t size = PyList_Size(keys);

    for (Py_ssize_t i = 0; i < size; i++) {
        PyObject* key = PyList_GetItem(keys, i);
        PyObject* value = PyList_GetItem(values, i);

        if (!PyUnicode_Check(key)) {
            Py_DECREF(keys);
            Py_DECREF(values);
            Py_DECREF(result);
            PyErr_SetString(PyExc_TypeError, "Dictionary keys must be strings");
            return NULL;
        }
        PyObject* key_str = PyUnicode_FromFormat("\"%U\"", key);

        PyObject* value_str = NULL;
        if (PyUnicode_Check(value)) {
            value_str = PyUnicode_FromFormat("\"%U\"", value);
        } else if (PyLong_Check(value)) {
            value_str = PyObject_Str(value);
        } else {
            Py_DECREF(keys);
            Py_DECREF(values);
            Py_DECREF(result);
            Py_DECREF(key_str);
            PyErr_SetString(PyExc_TypeError, "Unsupported value type");
            return NULL;
        }

        PyUnicode_AppendAndDel(&result, key_str);
        PyUnicode_AppendAndDel(&result, PyUnicode_FromString(": "));
        PyUnicode_AppendAndDel(&result, value_str);

        if (i < size - 1) {
            PyUnicode_AppendAndDel(&result, PyUnicode_FromString(", "));
        }
    }

    PyUnicode_AppendAndDel(&result, PyUnicode_FromString("}"));
    Py_DECREF(keys);
    Py_DECREF(values);

    return result;
}

// Module method definitions
static PyMethodDef CustomJsonMethods[] = {
    {"loads", custom_json_loads, METH_VARARGS, "Parse JSON string into a Python dictionary"},
    {"dumps", custom_json_dumps, METH_VARARGS, "Serialize a Python dictionary into a JSON string"},
    {NULL, NULL, 0, NULL}  // Sentinel
};

// Module definition
static struct PyModuleDef custom_json_module = {
    PyModuleDef_HEAD_INIT,
    "custom_json",
    "Custom JSON parser and serializer",
    -1,
    CustomJsonMethods
};

// Module initialization
PyMODINIT_FUNC PyInit_custom_json(void) {
    return PyModule_Create(&custom_json_module);
}
