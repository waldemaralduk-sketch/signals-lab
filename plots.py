"""Reusable Plotly figure builders."""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


_COLORS = ["#4C9BE8", "#F4845F", "#5ECA89", "#C97EE0", "#F2C94C"]


def _base_layout(fig: go.Figure, **kwargs) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="#FAFAFA", size=13),
        margin=dict(l=20, r=20, t=40, b=20),
        **kwargs,
    )
    return fig


def time_domain_plot(t: np.ndarray, signals: list[tuple[str, np.ndarray]]) -> go.Figure:
    """Multiple named signals on a single time-domain axes."""
    fig = go.Figure()
    for i, (name, sig) in enumerate(signals):
        fig.add_trace(go.Scatter(
            x=t, y=sig,
            mode="lines",
            name=name,
            line=dict(color=_COLORS[i % len(_COLORS)], width=1.5),
        ))
    _base_layout(fig, xaxis_title="Time (s)", yaxis_title="Amplitude", height=300)
    return fig


def fft_plot(freqs: np.ndarray, mags: np.ndarray, title: str = "Frequency Spectrum") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=freqs, y=mags,
        mode="lines",
        fill="tozeroy",
        fillcolor="rgba(76,155,232,0.25)",
        line=dict(color=_COLORS[0], width=1.5),
        name="Magnitude",
    ))
    _base_layout(fig, title=title, xaxis_title="Frequency (Hz)", yaxis_title="Magnitude", height=280)
    return fig


def dual_fft_plot(
    freqs_a: np.ndarray, mags_a: np.ndarray,
    freqs_b: np.ndarray, mags_b: np.ndarray,
    label_a: str = "Before", label_b: str = "After",
) -> go.Figure:
    fig = make_subplots(rows=1, cols=2, subplot_titles=(label_a, label_b))
    fig.add_trace(go.Scatter(
        x=freqs_a, y=mags_a, mode="lines", fill="tozeroy",
        fillcolor="rgba(76,155,232,0.25)",
        line=dict(color=_COLORS[0], width=1.5), name=label_a,
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=freqs_b, y=mags_b, mode="lines", fill="tozeroy",
        fillcolor="rgba(94,202,137,0.25)",
        line=dict(color=_COLORS[2], width=1.5), name=label_b,
    ), row=1, col=2)
    _base_layout(fig, height=280)
    fig.update_xaxes(title_text="Hz")
    fig.update_yaxes(title_text="Magnitude")
    return fig


def conv_plot(
    t_in: np.ndarray, sig_in: np.ndarray,
    k_idx: np.ndarray, kernel: np.ndarray,
    t_out: np.ndarray, sig_out: np.ndarray,
) -> go.Figure:
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=("Input signal", "Kernel / system response", "Convolution output"),
        vertical_spacing=0.12,
    )
    fig.add_trace(go.Scatter(x=t_in, y=sig_in, mode="lines",
                             line=dict(color=_COLORS[0], width=1.5), name="Input"), row=1, col=1)
    fig.add_trace(go.Scatter(x=k_idx, y=kernel, mode="lines+markers",
                             line=dict(color=_COLORS[1], width=1.5), name="Kernel"), row=2, col=1)
    fig.add_trace(go.Scatter(x=t_out, y=sig_out, mode="lines",
                             line=dict(color=_COLORS[2], width=1.5), name="Output"), row=3, col=1)
    _base_layout(fig, height=550)
    return fig
