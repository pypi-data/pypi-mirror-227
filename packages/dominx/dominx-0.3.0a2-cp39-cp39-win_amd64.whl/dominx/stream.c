#include "stream.h"

static int
Stream_traverse(StreamObject *self, visitproc visit, void *arg)
{
    return 0;
}

static int
Stream_clear(StreamObject *self)
{
    return 0;
}

static void
Stream_dealloc(StreamObject *self)
{
    PyObject_GC_UnTrack(self);
    Stream_clear(self);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

PyMODINIT_FUNC
PyInit_stream(void)
{
    PyObject *m;

    if (PyType_Ready(&StreamType) < 0)
        return NULL;

    m = PyModule_Create(&stream_py);
    if (m == NULL)
        return NULL;

    Py_INCREF(&StreamType);
    if (PyModule_AddObject(m, "Stream", (PyObject *)&StreamType) < 0) {
        Py_DECREF(&StreamType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
