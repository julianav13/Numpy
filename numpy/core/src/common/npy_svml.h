#if NPY_SIMD && defined(NPY_HAVE_AVX512_SKX) && defined(NPY_CAN_LINK_SVML)
extern __m512 __svml_expf16(__m512 x);
extern __m512 __svml_exp2f16(__m512 x);
extern __m512 __svml_logf16(__m512 x);
extern __m512 __svml_log2f16(__m512 x);
extern __m512 __svml_log10f16(__m512 x);
extern __m512 __svml_expm1f16(__m512 x);
extern __m512 __svml_log1pf16(__m512 x);
extern __m512 __svml_cbrtf16(__m512 x);
extern __m512 __svml_sinf16(__m512 x);
extern __m512 __svml_cosf16(__m512 x);
extern __m512 __svml_tanf16(__m512 x);
extern __m512 __svml_asinf16(__m512 x);
extern __m512 __svml_acosf16(__m512 x);
extern __m512 __svml_atanf16(__m512 x);
extern __m512 __svml_atan2f16(__m512 x);
extern __m512 __svml_sinhf16(__m512 x);
extern __m512 __svml_coshf16(__m512 x);
extern __m512 __svml_tanhf16(__m512 x);
extern __m512 __svml_asinhf16(__m512 x);
extern __m512 __svml_acoshf16(__m512 x);
extern __m512 __svml_atanhf16(__m512 x);

extern __m512d __svml_exp8(__m512d x);
extern __m512d __svml_exp28(__m512d x);
extern __m512d __svml_log8(__m512d x);
extern __m512d __svml_log28(__m512d x);
extern __m512d __svml_log108(__m512d x);
extern __m512d __svml_expm18(__m512d x);
extern __m512d __svml_log1p8(__m512d x);
extern __m512d __svml_cbrt8(__m512d x);
extern __m512d __svml_sin8(__m512d x);
extern __m512d __svml_cos8(__m512d x);
extern __m512d __svml_tan8(__m512d x);
extern __m512d __svml_asin8(__m512d x);
extern __m512d __svml_acos8(__m512d x);
extern __m512d __svml_atan8(__m512d x);
extern __m512d __svml_atan28(__m512d x);
extern __m512d __svml_sinh8(__m512d x);
extern __m512d __svml_cosh8(__m512d x);
extern __m512d __svml_tanh8(__m512d x);
extern __m512d __svml_asinh8(__m512d x);
extern __m512d __svml_acosh8(__m512d x);
extern __m512d __svml_atanh8(__m512d x);
#endif
