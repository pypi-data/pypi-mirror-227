/* Copyright 2020 The TensorFlow Authors. All Rights Reserved.

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

// This is a standard TensorFlow Lite FlatBuffer model file that has been
// converted into a C data array, so it can be easily compiled into a binary
// for devices that don't have a file system. It was created using the command:
// xxd -i model.tflite > model.cc

#ifndef TENSORFLOW_LITE_MICRO_EXAMPLES_MICRO_SPEECH_SIMPLE_FEATURES_MODEL_H_
#define TENSORFLOW_LITE_MICRO_EXAMPLES_MICRO_SPEECH_SIMPLE_FEATURES_MODEL_H_

extern const unsigned char g_model[];
extern const int g_model_len;

#endif  // TENSORFLOW_LITE_MICRO_EXAMPLES_MICRO_SPEECH_SIMPLE_FEATURES_MODEL_H_
