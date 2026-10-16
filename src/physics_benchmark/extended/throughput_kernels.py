"""Device controller for the throughput experiment (Warp is an optional dependency)."""

import warp as wp


@wp.kernel
def control(
    index: wp.array(dtype=wp.int32),
    q: wp.array2d(dtype=float),
    v: wp.array2d(dtype=float),
    qr: wp.array2d(dtype=float),
    vr: wp.array2d(dtype=float),
    ff: wp.array2d(dtype=float),
    kp: wp.array(dtype=float),
    kd: wp.array(dtype=float),
    limits: wp.array(dtype=float),
    force: wp.array2d(dtype=float),
):
    world, j = wp.tid()
    i = wp.min(index[0], 2499)
    force[world, j] = wp.clamp(
        ff[i, j] + kp[j] * (qr[i, j] - q[world, j]) + kd[j] * (vr[i, j] - v[world, j]),
        -limits[j],
        limits[j],
    )


@wp.kernel
def advance(index: wp.array(dtype=wp.int32)):
    index[0] += 1
