/*
 * This file was auto-generated with f2py (version:2_1330) and hand edited by
 * Pearu for testing purposes.  Do not edit this file unless you know what you
 * are doing!!!
 */

#ifdef __cplusplus
extern "C" {
#endif

/*********************** See f2py2e/cfuncs.py: includes
 * ***********************/

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "fortranobject.h"

#include <math.h>

static PyObject *wrap_error;
static PyObject *wrap_module;

/************************************ call
 * ************************************/
static char doc_f2py_rout_wrap_call[] =
        "\
Function signature:\n\
  arr = call(type_num,dims,intent,obj)\n\
Required arguments:\n"
        "  type_num : input int\n"
        "  dims : input int-sequence\n"
        "  intent : input int\n"
        "  obj : input python object\n"
        "Return objects:\n"
        "  arr : array";
static PyObject *
f2py_rout_wrap_call(PyObject *capi_self, PyObject *capi_args)
{
    PyObject *volatile capi_buildvalue = NULL;
    int type_num = 0;
    int elsize = 0;
    npy_intp *dims = NULL;
    PyObject *dims_capi = Py_None;
    int rank = 0;
    int intent = 0;
    PyArrayObject *capi_arr_tmp = NULL;
    PyObject *arr_capi = Py_None;
    int i;

    if (!PyArg_ParseTuple(capi_args, "iiOiO|:wrap.call", &type_num, &elsize,
                          &dims_capi, &intent, &arr_capi))
        return NULL;
    rank = PySequence_Length(dims_capi);
    dims = malloc(rank * sizeof(npy_intp));
    for (i = 0; i < rank; ++i) {
        PyObject *tmp;
        tmp = PySequence_GetItem(dims_capi, i);
        if (tmp == NULL) {
            goto fail;
        }
        dims[i] = (npy_intp)PyLong_AsLong(tmp);
        Py_DECREF(tmp);
        if (dims[i] == -1 && PyErr_Occurred()) {
            goto fail;
        }
    }
    capi_arr_tmp = ndarray_from_pyobj(type_num, elsize, dims, rank,
                                      intent | F2PY_INTENT_OUT, arr_capi,
                                      "wrap.call failed");
    if (capi_arr_tmp == NULL) {
        free(dims);
        return NULL;
    }
    capi_buildvalue = Py_BuildValue("N", capi_arr_tmp);
    free(dims);
    return capi_buildvalue;

fail:
    free(dims);
    return NULL;
}

static char doc_f2py_rout_wrap_attrs[] =
        "\
Function signature:\n\
  arr = array_attrs(arr)\n\
Required arguments:\n"
        "  arr : input array object\n"
        "Return objects:\n"
        "  data : data address in hex\n"
        "  nd : int\n"
        "  dimensions : tuple\n"
        "  strides : tuple\n"
        "  base : python object\n"
        "  (kind,type,type_num,elsize,alignment) : 4-tuple\n"
        "  flags : int\n"
        "  itemsize : int\n";
static PyObject *
f2py_rout_wrap_attrs(PyObject *capi_self, PyObject *capi_args)
{
    PyObject *arr_capi = Py_None;
    PyArrayObject *arr = NULL;
    PyObject *dimensions = NULL;
    PyObject *strides = NULL;
    char s[100];
    int i;
    memset(s, 0, 100);
    if (!PyArg_ParseTuple(capi_args, "O!|:wrap.attrs", &PyArray_Type,
                          &arr_capi))
        return NULL;
    arr = (PyArrayObject *)arr_capi;
    sprintf(s, "%p", PyArray_DATA(arr));
    dimensions = PyTuple_New(PyArray_NDIM(arr));
    strides = PyTuple_New(PyArray_NDIM(arr));
    for (i = 0; i < PyArray_NDIM(arr); ++i) {
        PyTuple_SetItem(dimensions, i, PyLong_FromLong(PyArray_DIM(arr, i)));
        PyTuple_SetItem(strides, i, PyLong_FromLong(PyArray_STRIDE(arr, i)));
    }
    return Py_BuildValue(
            "siNNO(cciii)ii", s, PyArray_NDIM(arr), dimensions, strides,
            (PyArray_BASE(arr) == NULL ? Py_None : PyArray_BASE(arr)),
            PyArray_DESCR(arr)->kind, PyArray_DESCR(arr)->type,
            PyArray_TYPE(arr), PyArray_ITEMSIZE(arr),
            PyArray_DESCR(arr)->alignment, PyArray_FLAGS(arr),
            PyArray_ITEMSIZE(arr));
}

static PyMethodDef f2py_module_methods[] = {

        {"call", f2py_rout_wrap_call, METH_VARARGS, doc_f2py_rout_wrap_call},
        {"array_attrs", f2py_rout_wrap_attrs, METH_VARARGS,
         doc_f2py_rout_wrap_attrs},
        {NULL, NULL}};

static struct PyModuleDef moduledef = {PyModuleDef_HEAD_INIT,
                                       "test_array_from_pyobj_ext",
                                       NULL,
                                       -1,
                                       f2py_module_methods,
                                       NULL,
                                       NULL,
                                       NULL,
                                       NULL};

PyMODINIT_FUNC
PyInit_test_array_from_pyobj_ext(void)
{
    PyObject *m, *d, *s;
    m = wrap_module = PyModule_Create(&moduledef);
    Py_SET_TYPE(&PyFortran_Type, &PyType_Type);
    import_array();
    if (PyErr_Occurred())
        Py_FatalError("can't initialize module wrap (failed to import numpy)");
    d = PyModule_GetDict(m);
    s = PyUnicode_FromString(
            "This module 'wrap' is auto-generated with f2py "
            "(version:2_1330).\nFunctions:\n"
            "  arr = call(type_num,dims,intent,obj)\n"
            ".");
    PyDict_SetItemString(d, "__doc__", s);
    wrap_error = PyErr_NewException("wrap.error", NULL, NULL);
    Py_DECREF(s);

#define ADDCONST(NAME, CONST)         \
    s = PyLong_FromLong(CONST);       \
    PyDict_SetItemString(d, NAME, s); \
    Py_DECREF(s)

    ADDCONST("F2PY_INTENT_IN", F2PY_INTENT_IN);
    ADDCONST("F2PY_INTENT_INOUT", F2PY_INTENT_INOUT);
    ADDCONST("F2PY_INTENT_OUT", F2PY_INTENT_OUT);
    ADDCONST("F2PY_INTENT_HIDE", F2PY_INTENT_HIDE);
    ADDCONST("F2PY_INTENT_CACHE", F2PY_INTENT_CACHE);
    ADDCONST("F2PY_INTENT_COPY", F2PY_INTENT_COPY);
    ADDCONST("F2PY_INTENT_C", F2PY_INTENT_C);
    ADDCONST("F2PY_OPTIONAL", F2PY_OPTIONAL);
    ADDCONST("F2PY_INTENT_INPLACE", F2PY_INTENT_INPLACE);
    ADDCONST("NPY_BOOL", NPY_BOOL);
    ADDCONST("NPY_BYTE", NPY_BYTE);
    ADDCONST("NPY_UBYTE", NPY_UBYTE);
    ADDCONST("NPY_SHORT", NPY_SHORT);
    ADDCONST("NPY_USHORT", NPY_USHORT);
    ADDCONST("NPY_INT", NPY_INT);
    ADDCONST("NPY_UINT", NPY_UINT);
    ADDCONST("NPY_INTP", NPY_INTP);
    ADDCONST("NPY_UINTP", NPY_UINTP);
    ADDCONST("NPY_LONG", NPY_LONG);
    ADDCONST("NPY_ULONG", NPY_ULONG);
    ADDCONST("NPY_LONGLONG", NPY_LONGLONG);
    ADDCONST("NPY_ULONGLONG", NPY_ULONGLONG);
    ADDCONST("NPY_FLOAT", NPY_FLOAT);
    ADDCONST("NPY_DOUBLE", NPY_DOUBLE);
    ADDCONST("NPY_LONGDOUBLE", NPY_LONGDOUBLE);
    ADDCONST("NPY_CFLOAT", NPY_CFLOAT);
    ADDCONST("NPY_CDOUBLE", NPY_CDOUBLE);
    ADDCONST("NPY_CLONGDOUBLE", NPY_CLONGDOUBLE);
    ADDCONST("NPY_OBJECT", NPY_OBJECT);
    ADDCONST("NPY_STRING", NPY_STRING);
    ADDCONST("NPY_UNICODE", NPY_UNICODE);
    ADDCONST("NPY_VOID", NPY_VOID);
    ADDCONST("NPY_NTYPES", NPY_NTYPES);
    ADDCONST("NPY_NOTYPE", NPY_NOTYPE);
    ADDCONST("NPY_USERDEF", NPY_USERDEF);

    ADDCONST("CONTIGUOUS", NPY_ARRAY_C_CONTIGUOUS);
    ADDCONST("FORTRAN", NPY_ARRAY_F_CONTIGUOUS);
    ADDCONST("OWNDATA", NPY_ARRAY_OWNDATA);
    ADDCONST("FORCECAST", NPY_ARRAY_FORCECAST);
    ADDCONST("ENSURECOPY", NPY_ARRAY_ENSURECOPY);
    ADDCONST("ENSUREARRAY", NPY_ARRAY_ENSUREARRAY);
    ADDCONST("ALIGNED", NPY_ARRAY_ALIGNED);
    ADDCONST("WRITEABLE", NPY_ARRAY_WRITEABLE);
    ADDCONST("WRITEBACKIFCOPY", NPY_ARRAY_WRITEBACKIFCOPY);

    ADDCONST("BEHAVED", NPY_ARRAY_BEHAVED);
    ADDCONST("BEHAVED_NS", NPY_ARRAY_BEHAVED_NS);
    ADDCONST("CARRAY", NPY_ARRAY_CARRAY);
    ADDCONST("FARRAY", NPY_ARRAY_FARRAY);
    ADDCONST("CARRAY_RO", NPY_ARRAY_CARRAY_RO);
    ADDCONST("FARRAY_RO", NPY_ARRAY_FARRAY_RO);
    ADDCONST("DEFAULT", NPY_ARRAY_DEFAULT);
    ADDCONST("UPDATE_ALL", NPY_ARRAY_UPDATE_ALL);

#undef ADDCONST(

    if (PyErr_Occurred())
        Py_FatalError("can't initialize module wrap");

#ifdef F2PY_REPORT_ATEXIT
    on_exit(f2py_report_on_exit, (void *)"array_from_pyobj.wrap.call");
#endif

    return m;
}
#ifdef __cplusplus
}
#endif
