# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/09d_nn_io.ipynb (unless otherwise specified).


from __future__ import annotations


__all__ = ['load_nn_weights_json', 'save_nn_weights_json', 'get_available_sizes', 'get_dense_weights_path',
           'get_norm_path', 'load_nn_dense']

# Cell
#nbdev_comment from __future__ import annotations

import json
import os
import re
from typing import Callable, Dict, List, Optional, Tuple

import jax.numpy as jnp
from .core import dense, preprocess
from .utils import norm
from ..typing_ import ComplexFloat

# Cell

def load_nn_weights_json(path: str) -> Dict[str, ComplexFloat]:
    """Load json weights from given path"""
    path = os.path.abspath(os.path.expanduser(path))
    weights = {}
    if os.path.exists(path):
        with open(path, "r") as file:
            for k, v in json.load(file).items():
                _v = jnp.array(v, dtype=float)
                assert isinstance(_v, jnp.ndarray)
                weights[k] = _v
    return weights

# Cell
def save_nn_weights_json(weights: Dict[str, ComplexFloat], path: str):
    """Save json weights to given path"""
    path = os.path.abspath(os.path.expanduser(path))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
        _weights = {}
        for k, v in weights.items():
            v = jnp.atleast_1d(jnp.array(v))
            assert isinstance(v, jnp.ndarray)
            _weights[k] = v.tolist()
        json.dump(_weights, file)

# Cell
def get_available_sizes(
    dirpath: str,
    prefix: str,
    input_names: Tuple[str, ...],
    output_names: Tuple[str, ...],
) -> List[Tuple[int, ...]]:
    """Get all available json weight hidden sizes given filename parameters

    > Note: this function does NOT return the input size and the output size
      of the neural network. ONLY the hidden sizes are reported. The input
      and output sizes can easily be derived from `input_names` (after
      preprocessing) and `output_names`.
    """
    all_weightfiles = os.listdir(dirpath)
    possible_weightfiles = (
        s for s in all_weightfiles if s.endswith(f"-{'-'.join(output_names)}.json")
    )
    possible_weightfiles = (
        s
        for s in possible_weightfiles
        if s.startswith(f"{prefix}-{'-'.join(input_names)}")
    )
    possible_weightfiles = (re.sub("[^0-9x]", "", s) for s in possible_weightfiles)
    possible_weightfiles = (re.sub("^x*", "", s) for s in possible_weightfiles)
    possible_weightfiles = (re.sub("x[^0-9]*$", "", s) for s in possible_weightfiles)
    possible_hidden_sizes = (s.strip() for s in possible_weightfiles if s.strip())
    possible_hidden_sizes = (
        tuple(hs.strip() for hs in s.split("x") if hs.strip())
        for s in possible_hidden_sizes
    )
    possible_hidden_sizes = (
        tuple(int(hs) for hs in s[1:-1]) for s in possible_hidden_sizes if len(s) > 2
    )
    possible_hidden_sizes = sorted(
        possible_hidden_sizes, key=lambda hs: (len(hs), max(hs))
    )
    return possible_hidden_sizes

# Cell

def get_dense_weights_path(
    *sizes: int,
    input_names: Optional[Tuple[str, ...]] = None,
    output_names: Optional[Tuple[str, ...]] = None,
    dirpath: str = "weights",
    prefix: str = "dense",
    preprocess=preprocess,
):
    """Create the SAX conventional path for a given weight dictionary"""
    if input_names:
        num_inputs = preprocess(*jnp.ones(len(input_names))).shape[0]
        sizes = (num_inputs,) + sizes
    if output_names:
        sizes = sizes + (len(output_names),)
    path = os.path.abspath(os.path.join(dirpath, prefix))
    if input_names:
        path = f"{path}-{'-'.join(input_names)}"
    if sizes:
        path = f"{path}-{'x'.join(str(s) for s in sizes)}"
    if output_names:
        path = f"{path}-{'-'.join(output_names)}"
    return f"{path}.json"

# Cell

def get_norm_path(
    *shape: int,
    input_names: Optional[Tuple[str, ...]] = None,
    output_names: Optional[Tuple[str, ...]] = None,
    dirpath: str = "norms",
    prefix: str = "norm",
    preprocess=preprocess,
):
    """Create the SAX conventional path for the normalization constants"""
    if input_names and output_names:
        raise ValueError(
            "To get the norm name, one can only specify `input_names` OR `output_names`."
        )
    if input_names:
        num_inputs = preprocess(*jnp.ones(len(input_names))).shape[0]
        shape = (num_inputs,) + shape
    if output_names:
        shape = shape + (len(output_names),)
    path = os.path.abspath(os.path.join(dirpath, prefix))
    if input_names:
        path = f"{path}-{'-'.join(input_names)}"
    if shape:
        path = f"{path}-{'x'.join(str(s) for s in shape)}"
    if output_names:
        path = f"{path}-{'-'.join(output_names)}"
    return f"{path}.json"

# Internal Cell
class _PartialDense:
    def __init__(self, weights, x_norm, y_norm, input_names, output_names):
        self.weights = weights
        self.x_norm = x_norm
        self.y_norm = y_norm
        self.input_names = input_names
        self.output_names = output_names

    def __call__(self, *params: ComplexFloat) -> ComplexFloat:
        return dense(self.weights, *params, x_norm=self.x_norm, y_norm=self.y_norm)

    def __repr__(self):
        return f"{self.__class__.__name__}{repr(self.input_names)}->{repr(self.output_names)}"

# Cell
def load_nn_dense(
    *sizes: int,
    input_names: Optional[Tuple[str, ...]] = None,
    output_names: Optional[Tuple[str, ...]] = None,
    weightprefix="dense",
    weightdirpath="weights",
    normdirpath="norms",
    normprefix="norm",
    preprocess=preprocess,
) -> Callable:
    """Load a pre-trained dense model"""
    weights_path = get_dense_weights_path(
        *sizes,
        input_names=input_names,
        output_names=output_names,
        prefix=weightprefix,
        dirpath=weightdirpath,
        preprocess=preprocess,
    )
    if not os.path.exists(weights_path):
        raise ValueError("Cannot find weights path for given parameters")
    x_norm_path = get_norm_path(
        input_names=input_names,
        prefix=normprefix,
        dirpath=normdirpath,
        preprocess=preprocess,
    )
    if not os.path.exists(x_norm_path):
        raise ValueError("Cannot find normalization for input parameters")
    y_norm_path = get_norm_path(
        output_names=output_names,
        prefix=normprefix,
        dirpath=normdirpath,
        preprocess=preprocess,
    )
    if not os.path.exists(x_norm_path):
        raise ValueError("Cannot find normalization for output parameters")
    weights = load_nn_weights_json(weights_path)
    x_norm_dict = load_nn_weights_json(x_norm_path)
    y_norm_dict = load_nn_weights_json(y_norm_path)
    x_norm = norm(x_norm_dict["mean"], x_norm_dict["std"])
    y_norm = norm(y_norm_dict["mean"], y_norm_dict["std"])
    partial_dense = _PartialDense(weights, x_norm, y_norm, input_names, output_names)
    return partial_dense