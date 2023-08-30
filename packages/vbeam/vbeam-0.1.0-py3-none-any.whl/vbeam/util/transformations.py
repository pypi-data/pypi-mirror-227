import spekk.transformations
import spekk.transformations.common
import spekk.util
from spekk import Spec
from spekk.transformations import *

from vbeam.fastmath import numpy as np


def iterative_vmap(f, in_axes):
    if isinstance(in_axes, int):
        in_axes = [in_axes]

    def wrapped(*args):
        sizes = [
            spekk.util.shape(arg)[a] for arg, a in zip(args, in_axes) if a is not None
        ]
        size = sizes[0]
        if not all(s == size for s in sizes):
            raise ValueError(
                f"Cannot apply python_vmap to arguments with different sizes over the \
in_axes: {sizes=}, {in_axes=}"
            )

        def scan_f(_, i):
            return None, f(
                *spekk.transformations.common.get_args_for_index(args, in_axes, i)
            )

        return np.scan(scan_f, None, np.arange(size))[1]

    return wrapped


class ForAll(spekk.transformations.ForAll):
    def __init__(
        self,
        *dimensions: str,
        parallel: bool = True,
        vmap_impl=None,
    ):
        if vmap_impl is None:
            from spekk.transformations.for_all import python_vmap
            vmap_impl = np.vmap if parallel else iterative_vmap
        super().__init__(*dimensions, vmap_impl=vmap_impl)


class Reduce(spekk.transformations.Reduce):
    def __post_init__(self):
        self.reduce_impl = np.reduce
        super().__post_init__()


__all__ = spekk.transformations.__all__
