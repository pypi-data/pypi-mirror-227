XMOS_AITOOLSLIB_DEFINITIONS = \
-DTF_LITE_STATIC_MEMORY \
-DTF_LITE_STRIP_ERROR_STRINGS \
-DXCORE \
-DNO_INTERPRETER

XMOS_AITOOLSLIB_LIBRARIES = $(XMOS_AITOOLSLIB_PATH)/lib/libxtflitemicro.a
XMOS_AITOOLSLIB_INCLUDES = -I$(XMOS_AITOOLSLIB_PATH)/include
