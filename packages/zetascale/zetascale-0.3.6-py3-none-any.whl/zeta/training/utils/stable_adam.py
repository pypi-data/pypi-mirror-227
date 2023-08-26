import math
from typing import List, Optional, Tuple, Union

import torch
import torch.nn as nn


class StableAdamWUnfused(torch.optim.Optimizer):
    def __init__(
        self,
        params,
        lr=0.002,
        weight_decay=0.2,
        betas=(0.9, 0.99),
        eps=1e-8,
        clip_thresh=1.0,
        precision="amp_bfloat16",
        custom_scalar=65536,
    ):
        beta1, beta2 = betas[0], betas[1]
        defaults = dict(lr=lr, weight_decay=weight_decay, beta1=beta1, beta2=beta2)
        super(StableAdamWUnfused, self).__init__(params, defaults)

        self.eps = eps
        self.d = clip_thresh

        # Set precision to "custom_fp16" if you want to use a fixed loss scalar, custom_scalar, which is divided out in the update step.
        # If you do this, call (custom_scalar * loss).backward() instead of loss.backward().
        self.precision = precision
        self.custom_scaler = custom_scalar

        for group in self.param_groups:
            group["step"] = 1.0

        print("Using StableAdamWUnfused-v1")

    def __setstate__(self, state):
        super(StableAdamWUnfused, self).__setstate__(state)

    def step(self, closure=None):
        if closure is not None:
            closure()

        for group in self.param_groups:
            lr = group["lr"]
            weight_decay = group["weight_decay"]
            beta1 = group["beta1"]
            beta2 = group["beta2"]
            step = group["step"]

            for p in group["params"]:
                if p.grad is None:
                    continue
                theta = p.data
                param_state = self.state[p]

                if self.precision == "custom_fp16":
                    g = p.grad.data / self.custom_scaler
                    if torch.any(torch.isnan(g) | torch.isinf(g)):
                        continue
                else:
                    g = p.grad.data

                if "exp_avg" not in param_state:
                    v = param_state["exp_avg"] = torch.zeros_like(theta)
                    u = param_state["exp_avg_sq"] = torch.zeros_like(theta)
                else:
                    v = param_state["exp_avg"]
                    u = param_state["exp_avg_sq"]

                beta1hat = beta1 * (1 - beta1 ** (step - 1)) / (1 - beta1**step)
                beta2hat = beta2 * (1 - beta2 ** (step - 1)) / (1 - beta2**step)

                v = v.mul_(beta1hat).add_(g, alpha=1.0 - beta1hat)
                u = u.mul_(beta2hat).addcmul_(g, g, value=1.0 - beta2hat)

                denominator = u.sqrt().add_(self.eps)

                # StableAdamW = AdamW + update clipping (https://arxiv.org/abs/1804.04235) applied tensor-wise.
                rms = (
                    torch.div(
                        g.pow(2), torch.maximum(u, (self.eps**2) * torch.ones_like(u))
                    )
                    .mean()
                    .sqrt()
                    .item()
                )

                theta = theta.mul_(1.0 - lr * weight_decay).addcdiv_(
                    v, denominator, value=-lr * (1.0 / max(1.0, rms / self.d))
                )

                # save current params
                param_state["exp_avg"] = v
                param_state["exp_avg_sq"] = u

            group["step"] = step + 1





class RelativePositionBias(nn.Module):
    def __init__(
        self, bidirectional=True, num_buckets=32, max_distance=128, n_heads=12
    ):
        super().__init__()
        self.bidirectional = bidirectional
        self.num_buckets = num_buckets
        self.max_distance = max_distance
        self.n_heads = n_heads
        self.relative_attention_bias = nn.Embedding(self.num_buckets, self.n_heads)

    @staticmethod
    def _relative_position_bucket(
        relative_position, bidirectional=True, num_buckets=32, max_distance=128
    ):
        ret = 0
        n = -relative_position
        if bidirectional:
            num_buckets //= 2
            ret += (n < 0).to(torch.long) * num_buckets
            n = torch.abs(n)
        else:
            n = torch.max(n, torch.zeros_like(n))

        max_exact = num_buckets // 2
        is_small = n < max_exact

        val_if_large = max_exact + (
            torch.log(n.float() / max_exact)
            / math.log(max_distance / max_exact)
            * (num_buckets - max_exact)
        ).to(torch.long)
        val_if_large = torch.min(
            val_if_large, torch.full_like(val_if_large, num_buckets - 1)
        )

        ret += torch.where(is_small, n, val_if_large)
        return ret

    def compute_bias(self, qlen, klen, step=None):
        step = 0 if step is None else step
        context_position = torch.arange(
            step,
            step + qlen,
            dtype=torch.long,
            device=self.relative_attention_bias.weight.device,
        )[:, None]
        memory_position = torch.arange(
            klen, dtype=torch.long, device=self.relative_attention_bias.weight.device
        )[None, :]
        relative_position = memory_position - context_position  # shape (qlen, klen)

        rp_bucket = self._relative_position_bucket(
            relative_position,  # shape (qlen, klen)
            bidirectional=self.bidirectional,
            num_buckets=self.num_buckets,
            max_distance=self.max_distance,
        )
        rp_bucket = rp_bucket.to(self.relative_attention_bias.weight.device)
        values = self.relative_attention_bias(
            rp_bucket
        )  # shape (qlen, klen, num_heads)
        values = values.permute([2, 0, 1]).unsqueeze(
            0
        )  # shape (1, num_heads, qlen, klen)
        return values

    def forward(self, batch_size, qlen, klen, step=None):
        # shape (batch * num_heads, qlen, klen)
        return (
            self.compute_bias(qlen, klen, step)
            .repeat(batch_size, 1, 1, 1)
            .view(-1, qlen, klen)
        )

