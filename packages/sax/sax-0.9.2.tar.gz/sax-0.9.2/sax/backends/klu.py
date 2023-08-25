# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/08b_backends_klu.ipynb (unless otherwise specified).


from __future__ import annotations


__all__ = ['solve_klu', 'mul_coo', 'evaluate_circuit_klu']

# Cell
#nbdev_comment from __future__ import annotations

from typing import Dict


from ..typing_ import SDense, SDict, SType, scoo
from . import evaluate_circuit

try:
    import klujax
except ImportError:
    klujax = None

try:
    import jax
    import jax.numpy as jnp
    JAX_AVAILABLE = True
except ImportError:
    import numpy as jnp
    JAX_AVAILABLE = False

# Cell
solve_klu = None
if klujax is not None:
    solve_klu = jax.vmap(klujax.solve, (None, None, 0, None), 0)

# Internal Cell

# @jax.jit  # TODO: make this available to autograd
# def mul_coo(Ai, Aj, Ax, b):
#     result = jnp.zeros_like(b).at[..., Ai, :].add(Ax[..., :, None] * b[..., Aj, :])
#     return result

# Cell
mul_coo = None
if klujax is not None:
    mul_coo = jax.vmap(klujax.coo_mul_vec, (None, None, 0, 0), 0)

# Cell
def evaluate_circuit_klu(
    instances: Dict[str, SType],
    connections: Dict[str, str],
    ports: Dict[str, str],
):
    """evaluate a circuit using KLU for the given sdicts. """

    if klujax is None:
        raise ImportError(
            "Could not import 'klujax'. "
            "Please install it first before using backend method 'klu'"
        )

    assert solve_klu is not None
    assert mul_coo is not None

    connections = {**connections, **{v: k for k, v in connections.items()}}
    inverse_ports = {v: k for k, v in ports.items()}
    port_map = {k: i for i, k in enumerate(ports)}

    idx, Si, Sj, Sx, instance_ports = 0, [], [], [], {}
    batch_shape = ()
    for name, instance in instances.items():
        si, sj, sx, ports_map = scoo(instance)
        Si.append(si + idx)
        Sj.append(sj + idx)
        Sx.append(sx)
        if len(sx.shape[:-1]) > len(batch_shape):
            batch_shape = sx.shape[:-1]
        instance_ports.update({f"{name},{p}": i + idx for p, i in ports_map.items()})
        idx += len(ports_map)

    Si = jnp.concatenate(Si, -1)
    Sj = jnp.concatenate(Sj, -1)
    Sx = jnp.concatenate(
        [jnp.broadcast_to(sx, (*batch_shape, sx.shape[-1])) for sx in Sx], -1
    )

    n_col = idx
    n_rhs = len(port_map)

    Cmap = {
        int(instance_ports[k]): int(instance_ports[v]) for k, v in connections.items()
    }
    Ci = jnp.array(list(Cmap.keys()), dtype=jnp.int32)
    Cj = jnp.array(list(Cmap.values()), dtype=jnp.int32)

    Cextmap = {int(instance_ports[k]): int(port_map[v]) for k, v in inverse_ports.items()}
    Cexti = jnp.stack(list(Cextmap.keys()), 0)
    Cextj = jnp.stack(list(Cextmap.values()), 0)
    Cext = jnp.zeros((n_col, n_rhs), dtype=complex).at[Cexti, Cextj].set(1.0)

    # TODO: make this block jittable...
    Ix = jnp.ones((*batch_shape, n_col))
    Ii = Ij = jnp.arange(n_col)
    mask = Cj[None,:] == Si[:, None]
    CSi = jnp.broadcast_to(Ci[None, :], mask.shape)[mask]

    # CSi = jnp.where(Cj[None, :] == Si[:, None], Ci[None, :], 0).sum(1)
    mask = (Cj[:, None] == Si[None, :]).any(0)
    CSj = Sj[mask]

    if Sx.ndim > 1: # bug in JAX... see https://github.com/google/jax/issues/9050
        CSx = Sx[..., mask]
    else:
        CSx = Sx[mask]

    # CSj = jnp.where(mask, Sj, 0)
    # CSx = jnp.where(mask, Sx, 0.0)

    I_CSi = jnp.concatenate([CSi, Ii], -1)
    I_CSj = jnp.concatenate([CSj, Ij], -1)
    I_CSx = jnp.concatenate([-CSx, Ix], -1)

    n_col, n_rhs = Cext.shape
    n_lhs = jnp.prod(jnp.array(batch_shape, dtype=jnp.int32))
    Sx = Sx.reshape(n_lhs, -1)
    I_CSx = I_CSx.reshape(n_lhs, -1)

    inv_I_CS_Cext = solve_klu(I_CSi, I_CSj, I_CSx, Cext)
    S_inv_I_CS_Cext = mul_coo(Si, Sj, Sx, inv_I_CS_Cext)

    CextT_S_inv_I_CS_Cext = S_inv_I_CS_Cext[..., Cexti, :][..., :, Cextj]

    _, n, _ = CextT_S_inv_I_CS_Cext.shape
    S = CextT_S_inv_I_CS_Cext.reshape(*batch_shape, n, n)

    return S, port_map