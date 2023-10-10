import torch
from .mel_extractor import Wav2Mel
from .models import CFNaiveMelPE


class DotDict(dict):
    """
    DotDict, used for config

    Example:
        # >>> config = DotDict({'a': 1, 'b': {'c': 2}}})
        # >>> config.a
        # 1
        # >>> config.b.c
        # 2
    """

    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def spawn_model(args: DotDict) -> CFNaiveMelPE:
    """Spawn conformer naive model"""
    if args.model.type == 'CFNaiveMelPE':
        pe_model = CFNaiveMelPE(
            input_channels=catch_none_args_must(
                args.mel.num_mels,
                func_name='torchfcpe.tools.spawn_cf_naive_mel_pe',
                warning_str='args.mel.num_mels is None',
            ),
            out_dims=catch_none_args_must(
                args.model.out_dims,
                func_name='torchfcpe.tools.spawn_cf_naive_mel_pe',
                warning_str='args.model.out_dims is None',
            ),
            hidden_dims=catch_none_args_must(
                args.model.hidden_dims,
                func_name='torchfcpe.tools.spawn_cf_naive_mel_pe',
                warning_str='args.model.hidden_dims is None',
            ),
            n_layers=catch_none_args_must(
                args.model.n_layers,
                func_name='torchfcpe.tools.spawn_cf_naive_mel_pe',
                warning_str='args.model.n_layers is None',
            ),
            n_heads=catch_none_args_must(
                args.model.n_heads,
                func_name='torchfcpe.tools.spawn_cf_naive_mel_pe',
                warning_str='args.model.n_heads is None',
            ),
            f0_max=catch_none_args_must(
                args.model.f0_max,
                func_name='torchfcpe.tools.spawn_cf_naive_mel_pe',
                warning_str='args.model.f0_max is None',
            ),
            f0_min=catch_none_args_must(
                args.model.f0_min,
                func_name='torchfcpe.tools.spawn_cf_naive_mel_pe',
                warning_str='args.model.f0_min is None',
            ),
            use_fa_norm=catch_none_args_must(
                args.model.use_fa_norm,
                func_name='torchfcpe.tools.spawn_cf_naive_mel_pe',
                warning_str='args.model.use_fa_norm is None',
            ),
            residual_dropout=catch_none_args_must(
                args.model.residual_dropout,
                func_name='torchfcpe.tools.spawn_cf_naive_mel_pe',
                warning_str='args.model.residual_dropout is None',
            ),
            attention_dropout=catch_none_args_must(
                args.model.attention_dropout,
                func_name='torchfcpe.tools.spawn_cf_naive_mel_pe',
                warning_str='args.model.attention_dropout is None',
            ),
        )
    else:
        raise ValueError(f'  [ERROR] args.model.type is {args.model.type}, but only support CFNaiveMelPE')
    return pe_model


def spawn_wav2mel(args: DotDict, device: str = None) -> Wav2Mel:
    """Spawn wav2mel"""
    wav2mel = Wav2Mel(
        sr=catch_none_args_opti(
            args.mel.sr,
            default=16000,
            func_name='torchfcpe.tools.spawn_wav2mel',
            warning_str='args.mel.sr is None',
        ),
        n_mels=catch_none_args_opti(
            args.mel.num_mels,
            default=128,
            func_name='torchfcpe.tools.spawn_wav2mel',
            warning_str='args.mel.num_mels is None',
        ),
        n_fft=catch_none_args_opti(
            args.mel.n_fft,
            default=1024,
            func_name='torchfcpe.tools.spawn_wav2mel',
            warning_str='args.mel.n_fft is None',
        ),
        win_size=catch_none_args_opti(
            args.mel.win_size,
            default=1024,
            func_name='torchfcpe.tools.spawn_wav2mel',
            warning_str='args.mel.win_size is None',
        ),
        hop_length=catch_none_args_opti(
            args.mel.hop_size,
            default=160,
            func_name='torchfcpe.tools.spawn_wav2mel',
            warning_str='args.mel.hop_size is None',
        ),
        fmin=catch_none_args_opti(
            args.mel.fmin,
            default=0,
            func_name='torchfcpe.tools.spawn_wav2mel',
            warning_str='args.mel.fmin is None',
        ),
        fmax=catch_none_args_opti(
            args.mel.fmax,
            default=8000,
            func_name='torchfcpe.tools.spawn_wav2mel',
            warning_str='args.mel.fmax is None',
        ),
        clip_val=catch_none_args_opti(
            args.mel.clip_val,
            default=1e-5,
            func_name='torchfcpe.tools.spawn_wav2mel',
            warning_str='args.mel.clip_val is None',
        ),
        device=catch_none_args_opti(
            device,
            default='cpu',
            func_name='torchfcpe.tools.spawn_wav2mel',
            warning_str='.device is None',
        ),
    )
    return wav2mel


def catch_none_args_opti(x, default, func_name, warning_str=None, level='WARN'):
    """Catch None, optional"""
    if x is None:
        if warning_str is not None:
            print(f'  [{level}] {warning_str}; use default {default}')
            print(f'  [{level}]    > call by:{func_name}')
        return default
    else:
        return x


def catch_none_args_must(x, func_name, warning_str):
    """Catch None, must"""
    level = "ERROR"
    if x is None:
        print(f'  [{level}] {warning_str}')
        print(f'  [{level}]    > call by:{func_name}')
        raise ValueError(f'  [{level}] {warning_str}')
    else:
        return x


def get_device(device: str, func_name: str) -> str:
    """Get device"""
    if device is None:
        print(f'  [INFO] torchcrepe.tools.get_device: device is None, use auto choice.')
        if torch.cuda.is_available():
            device = 'cuda'
            print(f'  [INFO] torchcrepe.tools.get_device: cuda is available, use cuda.')
            print(f'  [INFO]    > call by:{func_name}')
        else:
            device = 'cpu'
            print(f'  [INFO] torchcrepe.tools.get_device: cuda is not available, use cpu.')
            print(f'  [INFO]    > call by:{func_name}')
    else:
        print(f'  [INFO] torchcrepe.tools.get_device: device is not None, use {device}')
        print(f'  [INFO]    > call by:{func_name}')
        device = device
    return device