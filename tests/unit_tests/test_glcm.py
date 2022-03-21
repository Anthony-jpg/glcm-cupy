import cupy as cp
import numpy as np
import pytest

from glcm_cuda import GLCM
from tests.unit_tests import glcm_expected


@pytest.mark.parametrize(
    "i",
    [
        np.asarray([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8),
        np.asarray([1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=np.uint8),
        np.asarray([127, ] * 9, dtype=np.uint8),
        np.asarray([128, ] * 9, dtype=np.uint8),
        np.asarray([255, 255, 255, 255, 255, 255, 255, 255, 255],
                   dtype=np.uint8),
        # np.asarray([0, 1, 254, 255, 255, 255, 255, 255, 255], dtype=np.uint8),
    ]
)
@pytest.mark.parametrize(
    "j",
    [
        # np.asarray([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8),
        np.asarray([0, ] * 9, dtype=np.uint8),
        np.asarray([1, ] * 9, dtype=np.uint8),
        np.asarray([2, ] * 9, dtype=np.uint8),
        np.asarray([254, ] * 9, dtype=np.uint8),
        np.asarray([255, ] * 9, dtype=np.uint8),
        # np.asarray([255, 255, 255, 255, 255, 255, 255, 255, 255], dtype=np.uint8),
        np.asarray([0, 1, 254, 255, 255, 255, 255, 255, 255], dtype=np.uint8),
    ]
)
def test_glcm(i, j):
    windows = 2
    g = GLCM(radius=1)._from_partitioned_windows(
        cp.asarray(np.tile(i, (windows, 1))),
        cp.asarray(np.tile(j, (windows, 1)))
    )
    actual = dict(
        homogeneity=float(g[..., GLCM.HOMOGENEITY].sum() / windows),
        contrast=float(g[..., GLCM.CONTRAST].sum() / windows),
        asm=float(g[..., GLCM.ASM].sum() / windows),
        mean_i=float(g[..., GLCM.MEAN_I].sum() / windows),
        mean_j=float(g[..., GLCM.MEAN_J].sum() / windows),
        var_i=float(g[..., GLCM.VAR_I].sum() / windows),
        var_j=float(g[..., GLCM.VAR_J].sum() / windows),
        correlation=float(g[..., GLCM.CORRELATION].sum()/ windows)
    )

    expected = glcm_expected(i, j)
    assert actual == pytest.approx(expected, abs=1e-2)
