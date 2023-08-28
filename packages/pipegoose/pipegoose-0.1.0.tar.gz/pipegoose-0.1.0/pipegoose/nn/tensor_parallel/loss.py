from typing import Any

import torch
from einops import rearrange
from torch import nn
from torchtyping import TensorType

from pipegoose.distributed.functional import all_reduce
from pipegoose.distributed.parallel_context import ParallelContext
from pipegoose.distributed.parallel_mode import ParallelMode
from pipegoose.nn.tensor_parallel._utils import get_vocab_range_idx


class _VocabParallelCrossEntropy(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx: Any,
        parallel_logits: TensorType["batch_size", "n_samples", "vocab_size"],
        targets: TensorType["batch_size", "n_samples"],
        parallel_context: ParallelContext,
    ) -> torch.Tensor:
        def normalize_logits(parallel_logits):
            logit_max = torch.max(parallel_logits, dim=-1)[0]
            logit_max = all_reduce(
                logit_max,
                op=torch.distributed.ReduceOp.MAX,
                parallel_context=parallel_context,
                parallel_mode=ParallelMode.TENSOR,
            )
            normalized_parallel_logits = parallel_logits - logit_max.unsqueeze(-1)
            return normalized_parallel_logits

        def get_predicted_logits(parallel_logits, targets):
            rank = parallel_context.get_local_rank(ParallelMode.TENSOR)
            partition_size = parallel_logits.shape[-1]
            vocab_start_idx, vocab_end_idx = get_vocab_range_idx(partition_size, rank)

            target_mask = (targets < vocab_start_idx) | (targets >= vocab_end_idx)
            masked_targets = targets.clone() - vocab_start_idx
            masked_targets[target_mask] = 0

            parallel_logits = rearrange(parallel_logits, "batch_size seq_len vocab_size -> (batch_size seq_len) vocab_size")
            masked_targets_1d = rearrange(masked_targets, "batch_size seq_len -> (batch_size seq_len)")
            predicted_logits = parallel_logits[torch.arange(masked_targets_1d.size(0)), masked_targets_1d]
            predicted_logits = torch.where(
                rearrange(target_mask, "batch_size seq_len -> (batch_size seq_len)") == False, predicted_logits, 0.0
            )
            predicted_logits = all_reduce(
                predicted_logits, parallel_context=parallel_context, parallel_mode=ParallelMode.TENSOR
            )
            return predicted_logits

        # NOTE: parallel cross entropy still works without normalizing logits
        parallel_logits = normalize_logits(parallel_logits)
        predicted_logits = get_predicted_logits(parallel_logits, targets)

        exp_logits = torch.exp(parallel_logits)
        sum_exp_logits = exp_logits.sum(dim=-1)
        sum_exp_logits = all_reduce(sum_exp_logits, parallel_context=parallel_context, parallel_mode=ParallelMode.TENSOR)

        loss = torch.log(sum_exp_logits) - predicted_logits

        return loss

    @staticmethod
    def backward(ctx):
        pass


class VocabParallelCrossEntropy(nn.Module):
    def __init__(self, parallel_context: ParallelContext):
        super().__init__()
        # TODO: support reduce_mean, ignore_index
        self.parallel_context = parallel_context

    def forward(
        self, logits: TensorType["batch_size", "n_samples", "vocab_size"], targets: TensorType["batch_size", "n_samples"]
    ) -> torch.Tensor:
        loss = _VocabParallelCrossEntropy.apply(logits, targets, self.parallel_context)
        loss = loss.mean() / len(targets)
        return loss
