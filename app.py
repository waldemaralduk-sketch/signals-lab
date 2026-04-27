"""Signals Lab — interactive signals & systems visualizer."""

import numpy as np
from scipy.signal import convolve
import streamlit as st

import signals as sg
import plots as pl

st.set_page_config(page_title="Signals Lab", layout="wide", page_icon="〜")

st.title("Signals Lab")
st.caption("An interactive playground for signals & systems concepts.")

tabs = st.tabs([
    "Signal Generator",
    "FFT Analyzer",
    "Convolution Demo",
    "Filter Demo",
    "Notes",
])


# ---------------------------------------------------------------------------
# Shared state: generated signal passes from Signal Generator to FFT Analyzer
# ---------------------------------------------------------------------------
def _build_signal(sample_rate, duration, f1, amp1, phase1, use2, f2, amp2, phase2, noise_amp):
    t = sg.time_axis(duration, sample_rate)
    sig = sg.sine_wave(t, f1, amp1, phase1)
    if use2:
        sig = sig + sg.sine_wave(t, f2, amp2, phase2)
    if noise_amp > 0:
        sig = sig + sg.white_noise(t, noise_amp)
    return t, sig


# ---------------------------------------------------------------------------
# Tab 1 — Signal Generator
# ---------------------------------------------------------------------------
with tabs[0]:
    st.subheader("Signal Generator")
    st.markdown(
        "Build a signal from one or two sine waves and optional noise. "
        "Adjust the sliders and watch the wave update instantly."
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Sine wave 1**")
        sr = st.select_slider("Sample rate (Hz)", options=[1000, 2000, 4000, 8000, 16000], value=4000)
        dur = st.slider("Duration (s)", 0.5, 5.0, 1.0, 0.5)
        f1 = st.slider("Frequency 1 (Hz)", 1, sr // 4, 5)
        amp1 = st.slider("Amplitude 1", 0.1, 5.0, 1.0, 0.1)
        phase1 = st.slider("Phase 1 (deg)", -180, 180, 0, 5)

    with c2:
        st.markdown("**Optional second sine wave**")
        use2 = st.checkbox("Add second sine wave", value=False)
        f2 = st.slider("Frequency 2 (Hz)", 1, sr // 4, 20, disabled=not use2)
        amp2 = st.slider("Amplitude 2", 0.1, 5.0, 0.5, 0.1, disabled=not use2)
        phase2 = st.slider("Phase 2 (deg)", -180, 180, 0, 5, disabled=not use2)
        st.markdown("**Noise**")
        noise_amp = st.slider("Noise amplitude", 0.0, 2.0, 0.0, 0.05)

    t, combined = _build_signal(sr, dur, f1, amp1, phase1, use2, f2, amp2, phase2, noise_amp)

    traces = [("Sine 1", sg.sine_wave(t, f1, amp1, phase1))]
    if use2:
        traces.append(("Sine 2", sg.sine_wave(t, f2, amp2, phase2)))
    if noise_amp > 0 or use2:
        traces.append(("Combined", combined))

    st.plotly_chart(pl.time_domain_plot(t, traces), use_container_width=True)

    # Stash in session state so FFT tab can read it
    st.session_state["gen_t"] = t
    st.session_state["gen_sig"] = combined
    st.session_state["gen_sr"] = sr


# ---------------------------------------------------------------------------
# Tab 2 — FFT Analyzer
# ---------------------------------------------------------------------------
with tabs[1]:
    st.subheader("FFT Analyzer")
    st.markdown(
        "The **frequency domain** shows what ingredients are inside a signal — "
        "just like separating a smoothie back into its fruits. "
        "Each spike corresponds to one sine wave frequency."
    )

    if "gen_sig" in st.session_state:
        sig_fft = st.session_state["gen_sig"]
        sr_fft = st.session_state["gen_sr"]
        t_fft = st.session_state["gen_t"]

        st.markdown("**Time domain** (same signal from Signal Generator)")
        st.plotly_chart(
            pl.time_domain_plot(t_fft, [("Signal", sig_fft)]),
            use_container_width=True,
        )

        freqs, mags = sg.compute_fft(sig_fft, sr_fft)
        max_display_hz = st.slider(
            "Show frequencies up to (Hz)",
            10, sr_fft // 2, min(200, sr_fft // 2),
        )
        mask = freqs <= max_display_hz
        st.plotly_chart(pl.fft_plot(freqs[mask], mags[mask]), use_container_width=True)

        st.info(
            "**Time domain** = the signal over time (the wave shape).  \n"
            "**Frequency domain** = the frequencies inside the signal (the recipe).  \n"
            "A pure sine wave shows one spike. Two sines show two spikes. Noise spreads energy everywhere."
        )
    else:
        st.info("Generate a signal in the **Signal Generator** tab first.")


# ---------------------------------------------------------------------------
# Tab 3 — Convolution Demo
# ---------------------------------------------------------------------------
with tabs[2]:
    st.subheader("Convolution Demo")
    st.markdown(
        "Convolution slides a **kernel** (system response) over an **input signal** "
        "to produce an output. It answers: *what comes out of this system when this signal goes in?*"
    )

    c1, c2 = st.columns(2)
    with c1:
        input_name = st.selectbox("Input signal", list(sg.CONV_INPUTS.keys()))
    with c2:
        kernel_name = st.selectbox("Kernel / system", list(sg.CONV_KERNELS.keys()))

    N = 200
    sig_in = sg.CONV_INPUTS[input_name](N)
    kernel = sg.CONV_KERNELS[kernel_name]()
    sig_out = convolve(sig_in, kernel, mode="full")[: N]

    t_in = np.arange(N)
    t_out = np.arange(N)
    k_idx = np.arange(len(kernel))

    st.plotly_chart(
        pl.conv_plot(t_in, sig_in, k_idx, kernel, t_out, sig_out),
        use_container_width=True,
    )

    descriptions = {
        "Smoothing": "Averages neighboring samples — blurs sharp edges, reduces noise.",
        "Echo / delay": "Adds a delayed, quieter copy of the signal — like a room echo.",
        "Edge-like": "Highlights rapid changes — output is large where the signal changes fast.",
    }
    st.info(f"**{kernel_name} kernel:** {descriptions[kernel_name]}")


# ---------------------------------------------------------------------------
# Tab 4 — Filter Demo
# ---------------------------------------------------------------------------
with tabs[3]:
    st.subheader("Filter Demo")
    st.markdown(
        "A filter is like a **sieve for frequencies** — it lets some through and blocks others. "
        "Watch how the FFT spectrum changes after filtering."
    )

    sr_f = 4000

    st.markdown("**Build a noisy multi-tone signal**")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        filt_f1 = st.slider("Component 1 (Hz)", 5, 500, 20)
        filt_a1 = st.slider("Amplitude 1 ", 0.1, 3.0, 1.0, 0.1)
    with fc2:
        filt_f2 = st.slider("Component 2 (Hz)", 5, 500, 120)
        filt_a2 = st.slider("Amplitude 2 ", 0.1, 3.0, 1.0, 0.1)
    with fc3:
        filt_noise = st.slider("Noise amplitude ", 0.0, 2.0, 0.3, 0.05)

    t_f = sg.time_axis(1.0, sr_f)
    raw = (
        sg.sine_wave(t_f, filt_f1, filt_a1, 0)
        + sg.sine_wave(t_f, filt_f2, filt_a2, 0)
        + sg.white_noise(t_f, filt_noise, seed=7)
    )

    st.markdown("**Filter settings**")
    fc1b, fc2b, fc3b = st.columns(3)
    with fc1b:
        filt_type = st.radio("Filter type", ["Low-pass", "High-pass", "Band-pass"])
    with fc2b:
        nyq = sr_f // 2
        if filt_type == "Band-pass":
            bp_low = st.slider("Band low (Hz)", 5, nyq - 10, 50)
            bp_high = st.slider("Band high (Hz)", bp_low + 5, nyq - 1, 200)
        else:
            cutoff = st.slider("Cutoff frequency (Hz)", 5, nyq - 1, 80)
    with fc3b:
        filt_order = st.slider("Filter order", 1, 8, 4)

    try:
        if filt_type == "Low-pass":
            sos = sg.design_lowpass(cutoff, sr_f, filt_order)
        elif filt_type == "High-pass":
            sos = sg.design_highpass(cutoff, sr_f, filt_order)
        else:
            sos = sg.design_bandpass(bp_low, bp_high, sr_f, filt_order)

        filtered = sg.apply_filter(sos, raw)
        filter_error = None
    except Exception as e:
        filtered = raw.copy()
        filter_error = str(e)

    if filter_error:
        st.error(f"Filter design error: {filter_error}. Try adjusting the cutoff or order.")

    st.markdown("**Time domain: before vs after**")
    st.plotly_chart(
        pl.time_domain_plot(t_f, [("Original", raw), ("Filtered", filtered)]),
        use_container_width=True,
    )

    freqs_raw, mags_raw = sg.compute_fft(raw, sr_f)
    freqs_filt, mags_filt = sg.compute_fft(filtered, sr_f)
    max_hz = st.slider("Show spectrum up to (Hz) ", 10, nyq, min(400, nyq))
    mask = freqs_raw <= max_hz
    st.markdown("**FFT: before (left) vs after (right)**")
    st.plotly_chart(
        pl.dual_fft_plot(
            freqs_raw[mask], mags_raw[mask],
            freqs_filt[mask], mags_filt[mask],
            label_a="Original", label_b="Filtered",
        ),
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# Tab 5 — Notes
# ---------------------------------------------------------------------------
with tabs[4]:
    st.subheader("Concepts & Analogies")

    st.markdown("""
### What is a signal?
A signal is a quantity that varies over time — like sound pressure, voltage, or sensor readings.
In this app, signals are arrays of numbers sampled at a fixed **sample rate** (samples per second).

---

### Time domain vs frequency domain
| View | What it shows | Analogy |
|---|---|---|
| Time domain | The wave shape over time | A recording of a song |
| Frequency domain (FFT) | The frequencies present in the signal | The chord chart of that song |

**FFT (Fast Fourier Transform)** decomposes a signal into its frequency ingredients — like separating
a smoothie back into its fruits. A pure 10 Hz sine wave produces exactly one spike at 10 Hz in the FFT.

---

### Convolution
Convolution slides one signal over another sample by sample, multiplying and summing as it goes.
In systems theory, it tells you: *given this input and this system's impulse response, what does the output look like?*

- **Smoothing kernel** → blurs the signal (running average)
- **Echo kernel** → adds a delayed copy (reverb/echo effect)
- **Edge kernel** → highlights abrupt changes

---

### Filters
A filter passes some frequencies and blocks others — like a sieve.

| Filter | Passes | Blocks |
|---|---|---|
| Low-pass | Low frequencies | High frequencies & noise |
| High-pass | High frequencies | Low frequencies (e.g., DC drift) |
| Band-pass | A range of frequencies | Everything outside that range |

**Cutoff frequency** sets the boundary. **Filter order** controls how sharp the cutoff is —
higher order = steeper slope but can ring or become unstable.

---

### Key terms
- **Amplitude** — how tall the wave is (volume / intensity)
- **Frequency** — how many cycles per second (pitch)
- **Phase** — where in its cycle the wave starts
- **Sample rate** — how many samples per second (must be > 2× the highest frequency present — Nyquist theorem)
- **Nyquist limit** — highest frequency that can be represented = sample rate ÷ 2

---

*Signals Lab v1 — built with Streamlit, NumPy, SciPy, and Plotly.*
""")
