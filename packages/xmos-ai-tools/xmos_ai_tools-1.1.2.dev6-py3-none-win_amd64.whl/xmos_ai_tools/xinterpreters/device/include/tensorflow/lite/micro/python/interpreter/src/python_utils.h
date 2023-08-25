/* Copyright 2022 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/
#ifndef TENSORFLOW_LITE_MICRO_TOOLS_PYTHON_INTERPRETER_PYTHON_UTILS_H_
#define TENSORFLOW_LITE_MICRO_TOOLS_PYTHON_INTERPRETER_PYTHON_UTILS_H_

#include <Python.h>

namespace tflite {

struct PyDecrefDeleter {
  void operator()(PyObject* p) const { Py_DECREF(p); }
};

int ConvertFromPyString(PyObject* obj, char** data, Py_ssize_t* length);
PyObject* ConvertToPyString(const char* data, size_t length);

}  // namespace tflite

#endif
