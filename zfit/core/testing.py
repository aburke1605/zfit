"""
Module for testing of the zfit components. Contains a singleton instance to register new PDFs and let
them be tested.
"""
#  Copyright (c) 2020 zfit

from collections import OrderedDict
from typing import Callable, Tuple, List, Union, Iterable

import scipy.stats
import tensorflow as tf

from .interfaces import ZfitPDF
from .parameter import ZfitParameterMixin
from ..util.cache import clear_caches
from ..util.container import convert_to_container

__all__ = ["tester", "setup_function", "teardown_function"]


def setup_function():
    pass


def teardown_function():
    ZfitParameterMixin._existing_names.clear()

    clear_caches()
    # tf.compat.v1.reset_default_graph()


class BaseTester:
    pass


class AutoTester:

    def __init__(self):
        self.pdfs = []

    def register_pdf(self, pdf_class: ZfitPDF, params_factories: Union[Callable, Iterable[Callable]],
                     scipy_dist: scipy.stats.rv_continuous = None,
                     analytic_int_axes: Union[None, int, List[Tuple[int, ...]]] = None):
        # if not isinstance(pdf_class, ZfitPDF):
        #     raise TypeError(f"PDF {pdf_class} is not a ZfitPDF.")
        params_factories = convert_to_container(params_factories)

        if isinstance(analytic_int_axes, tuple):
            raise TypeError(f"`analytic_int_axes` is either a number or a list of tuples.")
        analytic_int_axes = convert_to_container(analytic_int_axes, non_containers=[tuple])
        if analytic_int_axes is not None:
            isinstance(analytic_int_axes)
        registration = OrderedDict((('pdf_class', pdf_class),
                                    ("params", params_factories),
                                    ("scipy_dist", scipy_dist)))
        self.pdfs.append(registration)

    def create_parameterized_pdfs(self):
        if len(self.pdfs) == 0:
            return [], []

        argnames = list(self.pdfs[0].keys())
        argvals = [[] * len(argnames)]

        for pdf in self.pdfs:
            for i, param in enumerate(pdf.values()):
                argvals[i].append(param)

        return argnames, argvals


tester = AutoTester()
