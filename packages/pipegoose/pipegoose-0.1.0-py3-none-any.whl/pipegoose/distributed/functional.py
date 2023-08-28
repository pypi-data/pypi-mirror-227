from typing import Any, Optional

import torch
import torch.distributed as dist
from torch.distributed import ReduceOp

from pipegoose.distributed._p2p import _P2P
from pipegoose.distributed.parallel_context import ParallelContext
from pipegoose.distributed.parallel_mode import ParallelMode


def scatter(
    tensor: torch.Tensor,
    dim: int,
    parallel_context: Optional[ParallelContext] = None,
    parallel_mode: Optional[ParallelMode] = None,
) -> torch.Tensor:
    world_size = parallel_context.get_world_size(parallel_mode)
    rank = parallel_context.get_local_rank(parallel_mode)

    if world_size == 1:
        return tensor

    assert tensor.size(dim) % world_size == 0

    tensor_list = torch.chunk(tensor, world_size, dim=dim)
    return tensor_list[rank]


def reduce(
    tensor: torch.Tensor,
    dst: int,
    op: ReduceOp = ReduceOp.SUM,
    async_op: bool = False,
    parallel_context: Optional[ParallelContext] = None,
    parallel_mode: Optional[ParallelContext] = None,
) -> torch.Tensor:
    world_size = parallel_context.get_world_size(parallel_mode)

    if world_size == 1:
        return tensor

    group = parallel_context.get_group(parallel_mode)
    work = dist.reduce(tensor, dst=dst, op=op, group=group)

    if async_op:
        return tensor, work
    else:
        return tensor


def broadcast(
    tensor: torch.Tensor,
    src: int,
    async_op: bool = False,
    parallel_context: Optional[ParallelContext] = None,
    parallel_mode: Optional[ParallelMode] = None,
) -> torch.Tensor:
    world_size = parallel_context.get_world_size(parallel_mode)

    if world_size == 1:
        return tensor

    group = parallel_context.get_group(parallel_mode)
    work = dist.broadcast(tensor, src=src, group=group, async_op=async_op)

    if async_op:
        return tensor, work
    else:
        return tensor


def all_gather(
    tensor: torch.Tensor,
    dim: int = 0,
    async_op: bool = False,
    parallel_context: Optional[ParallelContext] = None,
    parallel_mode: Optional[ParallelMode] = None,
) -> torch.Tensor:
    """All gather tensors from all processes in parallel group.

    Args:
        input (torch.Tensor): The tensor you want to gather.
        dim (int, optional): The dimension along which to gather the tensor.. Defaults to 0.
        async_op (bool, optional): _description_. Defaults to False.
        parallel_context (Optional[ParallelContext], optional): _description_. Defaults to None.
        parallel_mode (Optional[ParallelMode], optional): _description_. Defaults to None.

    Returns:
        torch.Tensor: _description_
    """
    world_size = parallel_context.get_world_size(parallel_mode)
    group = parallel_context.get_group(parallel_mode)

    if world_size == 1:
        return tensor

    tensor_list = [torch.empty_like(tensor) for _ in range(world_size)]
    work = dist.all_gather(tensor_list=tensor_list, tensor=tensor, async_op=async_op, group=group)

    if tensor.dim() == 0:
        tensor_list = [tensor.unsqueeze(dim=0) for tensor in tensor_list]

    tensor_list = torch.cat(tensor_list, dim=dim)

    if async_op:
        return tensor_list, work
    else:
        return tensor_list


def all_reduce(
    tensor: torch.Tensor,
    op: ReduceOp = ReduceOp.SUM,
    async_op: bool = False,
    parallel_context: Optional[ParallelContext] = None,
    parallel_mode: Optional[ParallelMode] = None,
) -> torch.Tensor:
    world_size = parallel_context.get_world_size(parallel_mode)

    if world_size == 1:
        return tensor

    group = parallel_context.get_group(parallel_mode)
    work = dist.all_reduce(tensor, op=op, group=group, async_op=async_op)

    if async_op:
        return tensor, work
    else:
        return tensor


def reduce_scatter():
    pass


def send(
    data: Any,
    src: int,
    dst: int,
    parallel_context: ParallelContext,
    parallel_mode: ParallelMode = ParallelMode.PIPELINE,
):
    if src == parallel_context.get_local_rank(parallel_mode):
        _P2P().send(data, dst, parallel_context, parallel_mode)


def recv(
    src: int, dst: int, parallel_context: ParallelContext, parallel_mode: ParallelMode = ParallelMode.PIPELINE
) -> Optional[Any]:
    if dst == parallel_context.get_local_rank(parallel_mode):
        return _P2P().recv(src, parallel_context, parallel_mode)
