import itertools

import tensorflow as tf

from zfit.core.basefunc import BaseFunc
from zfit.util.container import convert_to_container


class SimpleFunction(BaseFunc):

    def __init__(self, func, name="Function", n_dims=1, **parameters):
        super().__init__(name=name, **parameters)
        self._value_func = self._check_input_x_function(func)
        self._user_n_dims = n_dims

    def _value(self, x):
        return self._value_func(x)

    @property
    def _n_dims(self):
        return self._user_n_dims


class BaseFunctorFunc(BaseFunc):
    def __init__(self, funcs, name="BaseFunctorFunc", **kwargs):
        funcs = convert_to_container(funcs)
        params = {}
        for func in funcs:
            params.update(func.parameters)
        kwargs.update(params)
        super().__init__(name=name, **kwargs)
        self.funcs = funcs

    def _get_dependents(self):  # TODO: change recursive to `only_floating`?
        dependents = super()._get_dependents()  # get the own parameter dependents
        func_dependents = self._extract_dependents(self.funcs)  # flatten
        return dependents.union(func_dependents)


class SumFunc(BaseFunctorFunc):
    def __init__(self, funcs, dims=None, name="SumFunc", **kwargs):
        super().__init__(funcs=funcs, name=name, **kwargs)
        self.dims = dims

    def _value(self, x):
        # sum_funcs = tf.add_n([func.value(x) for func in self.funcs])
        funcs = [func.value(x) for func in self.funcs]
        sum_funcs = tf.accumulate_n(funcs)
        return sum_funcs

    @property
    def _n_dims(self):
        return 1  # TODO(mayou36): properly implement dimensions


class ProdFunc(BaseFunctorFunc):
    def __init__(self, funcs, dims=None, name="SumFunc", **kwargs):
        super().__init__(funcs=funcs, name=name, **kwargs)
        self.dims = dims

    def _value(self, x):
        value = self.funcs[0].value(x)
        for func in self.funcs[1:]:
            value *= func.value(x)
        return value

    @property
    def _n_dims(self):
        return 1  # TODO(mayou36): properly implement dimensions
