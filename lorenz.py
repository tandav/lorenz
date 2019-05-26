import numpy as np
import numba


# @numba.jit(nopython=True, parallel=True, fastmath = True, nogil=True)
# def lorenz(p, s, r, b, steps, dt):
#     # print(p.max(), p.mean())
#     if np.abs(p.max()) > 1.7976931348623157e+50 or np.abs(p.min()) < 1.7976931348623157e-50:
#         p[...] = 0
#         # print(p.mean())
#     else:
#         print('hahah')
#         # p[...] = np.random.random(p.shape)
#         for i in numba.prange(1, steps):
#             p[i, 0] = p[i - 1, 0] + s * (p[i - 1, 1] - p[i - 1, 0]) * dt
#             p[i, 1] = p[i - 1, 1] + (r * p[i - 1, 0] - p[i - 1, 1] - p[i - 1, 0] * p[i - 1, 2]) * dt
#             p[i, 2] = p[i - 1, 2] + (p[i - 1, 0] * p[i - 1, 1] - b * p[i - 1, 2]) * dt
#
#     # for i in numba.prange(1, steps):
#     #
#     #     _0 = p[i - 1, 0] + s * (p[i - 1, 1] - p[i - 1, 0]) * dt
#     #     _1 = p[i - 1, 1] + (r * p[i - 1, 0] - p[i - 1, 1] - p[i - 1, 0] * p[i - 1, 2]) * dt
#     #     _2 = p[i - 1, 2] + (p[i - 1, 0] * p[i - 1, 1] - b * p[i - 1, 2]) * dt
#     #
#     #     p[i, 0] = _0 if not np.isinf(_0) and not np.isinf(_0) else 0
#     #     p[i, 1] = _1 if not np.isinf(_1) and not np.isinf(_1) else 0
#     #     p[i, 2] = _1 if not np.isinf(_2) and not np.isinf(_2) else 0
#     # p[np.isnan(p)] = 0

@numba.jit(nopython=True, parallel=True, fastmath = True, nogil=True)
def lorenz(p, s, r, b, steps, dt):
    for i in numba.prange(1, steps):
        p[i, 0] = p[i - 1, 0] + s * (p[i - 1, 1] - p[i - 1, 0]) * dt
        p[i, 1] = p[i - 1, 1] + (r * p[i - 1, 0] - p[i - 1, 1] - p[i - 1, 0] * p[i - 1, 2]) * dt
        p[i, 2] = p[i - 1, 2] + (p[i - 1, 0] * p[i - 1, 1] - b * p[i - 1, 2]) * dt
