# Signals Lab

An interactive playground for signals & systems concepts, built with Streamlit.

## Features

| Tab | What it teaches |
|---|---|
| Signal Generator | Build sine waves, mix signals, add noise |
| FFT Analyzer | See the frequency content of any generated signal |
| Convolution Demo | Watch kernels transform signals visually |
| Filter Demo | Apply low-pass, high-pass, and band-pass filters |
| Notes | Analogies and key term definitions |

## Install & run

Recommended on this machine, using `uv`:

```bash
cd /home/waldemar/signals-lab
uv run --with streamlit --with numpy --with scipy --with plotly streamlit run app.py
```

Normal Python/pip method, if `python3-venv` is installed:

```bash
cd /home/waldemar/signals-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at **http://localhost:8501** by default.

## Dependencies

- [Streamlit](https://streamlit.io) — interactive UI
- [NumPy](https://numpy.org) — signal arrays and FFT
- [SciPy](https://scipy.org) — convolution and filter design
- [Plotly](https://plotly.com/python/) — interactive charts

## Project structure

```
app.py          Main Streamlit app and UI layout
signals.py      Signal generation and processing (numpy/scipy)
plots.py        Plotly figure builders
requirements.txt
```

## Out of scope (v1)

Circuit simulators, Laplace transforms, audio input, and file upload are planned for a later version.
