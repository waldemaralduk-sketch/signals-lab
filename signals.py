"""Core signal generation and processing utilities."""

import numpy as np
from scipy import signal as sp_signal


def time_axis(duration: float, sample_rate: int) -> np.ndarray:
    return np.linspace(0, duration, int(duration * sample_rate), endpoint=False)


def sine_wave(t: np.ndarray, freq: float, amplitude: float, phase_deg: float) -> np.ndarray:
    return amplitude * np.sin(2 * np.pi * freq * t + np.deg2rad(phase_deg))


def white_noise(t: np.ndarray, amplitude: float, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return amplitude * rng.standard_normal(len(t))


def compute_fft(sig: np.ndarray, sample_rate: int):
    n = len(sig)
    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    magnitudes = np.abs(np.fft.rfft(sig)) * 2 / n
    return freqs, magnitudes


# --- Convolution inputs ---

def make_impulse(n: int) -> np.ndarray:
    x = np.zeros(n)
    x[n // 4] = 1.0
    return x


def make_square_pulse(n: int) -> np.ndarray:
    x = np.zeros(n)
    x[n // 4: n // 2] = 1.0
    return x


def make_sine_burst(n: int, cycles: int = 3) -> np.ndarray:
    t = np.linspace(0, cycles * 2 * np.pi, n)
    burst = np.sin(t)
    burst[: n // 4] = 0
    burst[n // 2:] = 0
    return burst


def make_step(n: int) -> np.ndarray:
    x = np.zeros(n)
    x[n // 4:] = 1.0
    return x


CONV_INPUTS = {
    "Impulse": make_impulse,
    "Square pulse": make_square_pulse,
    "Sine burst": make_sine_burst,
    "Step": make_step,
}


# --- Convolution kernels ---

def kernel_smooth(width: int = 15) -> np.ndarray:
    k = np.ones(width) / width
    return k


def kernel_echo(delay: int = 20, decay: float = 0.6) -> np.ndarray:
    k = np.zeros(delay + 1)
    k[0] = 1.0
    k[delay] = decay
    return k


def kernel_edge(width: int = 11) -> np.ndarray:
    k = np.zeros(width)
    mid = width // 2
    k[:mid] = -1.0 / mid
    k[mid + 1:] = 1.0 / (width - mid - 1)
    return k


CONV_KERNELS = {
    "Smoothing": kernel_smooth,
    "Echo / delay": kernel_echo,
    "Edge-like": kernel_edge,
}


# --- Filters ---

def design_lowpass(cutoff: float, sample_rate: int, order: int) -> tuple:
    nyq = sample_rate / 2
    return sp_signal.butter(order, cutoff / nyq, btype="low", output="sos")


def design_highpass(cutoff: float, sample_rate: int, order: int) -> tuple:
    nyq = sample_rate / 2
    return sp_signal.butter(order, cutoff / nyq, btype="high", output="sos")


def design_bandpass(low: float, high: float, sample_rate: int, order: int) -> tuple:
    nyq = sample_rate / 2
    return sp_signal.butter(order, [low / nyq, high / nyq], btype="band", output="sos")


def apply_filter(sos, sig: np.ndarray) -> np.ndarray:
    return sp_signal.sosfiltfilt(sos, sig)
