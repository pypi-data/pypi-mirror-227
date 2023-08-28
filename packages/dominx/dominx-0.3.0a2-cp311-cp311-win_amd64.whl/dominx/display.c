#include "display.h"

PyMODINIT_FUNC
PyInit_display(void)
{
    PyObject *m = PyModule_Create(&display_py);
    return m;
}
