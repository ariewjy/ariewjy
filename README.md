## Hi there 👋 I am Arie!

> I am currently working as geoscientist, with expertise in petrophysics. Been working for more than 9 years in the energy industry, and is looking to learn more about data analytics/science and/or machine learning applications for energy industry as a whole.

- 🔭 I’m currently working on plotpetrophysics [![Plotpetrophysics](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://plotpetrophysics.streamlit.app/). An online geoscience tool to plot your well log data into a triple combo plot, to formation evaluation plot. 
- 🌱 I’m currently learning Python for Data Science/ Machine Learning, and keen to implement it to the energy industry. 
- 👯 I’m looking to collaborate on geoscience and/or data science
- 🤔 I’m looking for help with implementing a better code (refactoring) for the plotpetrophysics.com, you can find the source code here: https://github.com/ariewjy/triple_combo_web_plotter
- 💬 Ask me about geosciences in general, and petrophysical analysis
- 📫 How to reach me: www.linkedin.com/in/adityaariewijaya or twitter @adtarie


## Sonic-based water saturation examples

### 1) Python example script (calibration + inversion)

`sonic_sw_gassmann_example.py` demonstrates estimating water saturation from DTC/DTS with rock physics (Gassmann + Wood mixing), calibrated using a known water-bearing zone.

Run:

```bash
python3 sonic_sw_gassmann_example.py
```

### 2) Interactive synthetic well-log playground (HTML)

`sonic_sw_playground.html` provides a no-dependency interface to:

- generate synthetic well-log-like data (Depth, DTC, DTS, PHI, VSH),
- define water and hydrocarbon intervals,
- run a Gassmann-based Sw estimate from sonic,
- compare `Sw_true` vs `Sw_est` and visualize log tracks.

Run locally:

```bash
python3 -m http.server 8000
```

Then open:

- http://localhost:8000/sonic_sw_playground.html
