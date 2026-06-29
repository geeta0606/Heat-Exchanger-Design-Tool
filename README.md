# Heat-Exchanger-Design-Tool
## Overview

A Python-based tool developed to perform thermal analysis of a double-pipe heat exchanger using the Log Mean Temperature Difference (LMTD) and NTU-Effectiveness methods. The program calculates important design parameters and generates plots to study the effect of operating variables on heat exchanger performance.



## Features

- Calculates heat duty of hot and cold fluids
- Calculates Log Mean Temperature Difference (LMTD)
- Determines required heat transfer area
- Calculates heat capacity rates and capacity ratio
- Computes maximum possible heat transfer
- Calculates heat exchanger effectiveness
- Evaluates energy balance error
- Generates engineering performance plots
- Compares parallel-flow and counterflow heat exchangers


## Methods Used
- LMTD Method
- NTU-Effectiveness Method
- Energy Balance

## Project Structure
Heat-Exchanger-Design-Tool/
│
├── Heat_Exchanger_Tool.py
├── Heat_Exchanger_Report.pdf
├── README.md
└── plots/

![Area vs U](plots/area_vs_u.png)

![Effectiveness Comparison](plots/parallel_vs_counterflow.png)

![Heat Duty vs Flow Rate](plots/heat_duty_vs_hot_flow_rate.png)

## Technologies Used
- Python 3
- Matplotlib
- Math module
