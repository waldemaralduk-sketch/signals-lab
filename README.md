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

First, clone the project:

```bash
git clone https://github.com/waldemaralduk-sketch/signals-lab.git
cd signals-lab
```

### Windows

Open **PowerShell** in the `signals-lab` folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run this once in the same PowerShell window:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try the activation command again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Alternative Windows Command Prompt activation:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Using uv

If you already use `uv`, you can run it without manually creating a virtual environment:

```bash
uv run --with streamlit --with numpy --with scipy --with plotly streamlit run app.py
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
