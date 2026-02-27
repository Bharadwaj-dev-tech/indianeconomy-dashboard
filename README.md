# 📊 Indian Economic Growth Dashboard (1990–2023)

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31011/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.24-3f4f75.svg)](https://plotly.com/)
[![Open Source](https://img.shields.io/badge/Open%20Source-❤️-brightgreen.svg)]()

A premium, interactive dashboard that visualises **Indian economic indicators** from 1990 to 2023.  
Built with **Streamlit** and **Plotly**, it delivers a sleek black‑glossy interface with neon‑accented charts – perfect for fintech enthusiasts and economic analysts.

> ⚡ *Synthetic data mimics real economic events: liberalisation (1991), financial crisis (2008), and COVID‑19 shock (2020).*

---

## ✨ Key Features

- 🎯 **Live KPI Cards** – GDP Growth, Inflation, Fiscal Deficit, FDI, Forex Reserves
- 🗓️ **Year‑Range Slider** – filter data from 1990 to 2023 dynamically
- 📈 **Six Themed Tabs**:
  - *Overview* – GDP vs Inflation, Growth trend, Credit Growth
  - *Public Sector* – Fiscal Deficit, Public Debt, Fiscal indicators
  - *Private Sector* – GFCF, IIP, FDI
  - *External Sector* – Exports/Imports, Trade Balance, Forex Reserves
  - *3D Analytics* – Interactive 3D scatter & line plots
  - *Global GDP* – Choropleth map with country‑wise GDP classification
- 🌑 **Dark‑mode UI** with custom neon colour palette (`#00f5ff`, `#39ff14`, …)
- 🔍 **Hover tooltips** & smooth transitions
- 🗺️ **Global Comparison** – 30+ countries categorised by GDP level (High / Medium / Low)

---

## 🖼️ Dashboard Preview

*(Add a screenshot of your dashboard here)*  
![Dashboard Screenshot](https://via.placeholder.com/1200x600.png?text=Indian+Economic+Dashboard+Preview)

---

## 🛠️ Built With

- [Python 3.10.11](https://www.python.org/) – core language
- [Streamlit](https://streamlit.io/) – rapid web app framework
- [Plotly](https://plotly.com/python/) – interactive charting
- [Pandas](https://pandas.pydata.org/) – data wrangling
- [NumPy](https://numpy.org/) – numerical simulation

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10.11 (other 3.10+ versions may work, but 3.10.11 is tested)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bharadwaj-dev-tech/indian-economic-dashboard.git
   cd indian-economic-dashboard
   ```

2. **Create and activate a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open your browser at `http://localhost:8501`

---

## 📁 Repository Structure

```
.
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── (no external data)    # All data is generated on‑the‑fly
```

---

## 📊 Data Generation

All economic indicators are **synthetically generated** using NumPy and Pandas to reflect realistic Indian trends.  
No external files or API keys are needed – the app runs completely standalone.

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to open an **issue** or submit a **pull request** for improvements or additional features.

---

## 📄 License

This project is open source – you are free to use, modify, and distribute it as you wish.  
*(No formal license included – use under the terms of your choice.)*

---

**Made with ❤️ using Streamlit & Plotly**  
```
