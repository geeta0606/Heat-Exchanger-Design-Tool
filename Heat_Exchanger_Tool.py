#Python-Based Heat Exchanger Design and Performance Analysis Tool
import math
import matplotlib.pyplot as plt

def heat_duty(T_in, T_out, Cp, m):
    Q = m*Cp*(T_out-T_in)
    return Q

def lmtd(Th_in, Th_out, Tc_in, Tc_out):
    delta_T1 = Th_in - Tc_out
    delta_T2 = Th_out - Tc_in
    if delta_T1 <= 0 or delta_T2 <= 0:
        raise ValueError("Invalid temperature inputs for LMTD calculation.")
    if math.isclose(delta_T1, delta_T2):
        return delta_T1
    else:
        return (delta_T1-delta_T2)/math.log(delta_T1/delta_T2)
    
def heat_exchanger_area(Q, U, LMTD):
    A = Q/(U*LMTD)
    return A

def effectiveness_counterflow(NTU, capacity_ratio):
    if capacity_ratio == 1:
        return NTU/(1+NTU)
    else:
        return (1-math.exp(-NTU*(1-capacity_ratio)))/(1-capacity_ratio*math.exp(-NTU*(1-capacity_ratio)))

def error_percentage(Qh, Qc):
    return (abs(Qh-Qc)/max(abs(Qh), abs(Qc)))*100

def capacity_ratio(Ch, Cc):
    return min(Ch, Cc)/max(Ch, Cc)

def capacity_rate(m, Cp):
    return m*Cp



####Taking user inputs for hot and cold fluid properties
Th_in = float(input("Enter the hot fluid inlet temperature (K): "))
Th_out = float(input("Enter the hot fluid outlet temperature (K): "))
Tc_in = float(input("Enter the cold fluid inlet temperature (K): "))
Tc_out = float(input("Enter the cold fluid outlet temperature (K): "))

Cp_h = float(input("Enter the specific heat capacity of the hot fluid (kJ/kgK): "))
Cp_c = float(input("Enter the specific heat capacity of the cold fluid (kJ/kgK): "))
m_h = float(input("Enter the mass flow rate of the hot fluid (kg/s): "))
m_c = float(input("Enter the mass flow rate of the cold fluid (kg/s): "))
U_input = float(input("Enter the overall heat transfer coefficient (W/m²K): "))


U= U_input/1000  #Converting W/m²K to kW/m²K

#Calculating heat duties, LMTD, heat exchanger area, error percentage, capacity rates, capacity ratio, maximum possible heat transfer, and effectiveness
Qh = heat_duty(Th_in, Th_out, Cp_h, m_h)

Qc = heat_duty(Tc_in, Tc_out, Cp_c, m_c)

delta_Tlm = lmtd(Th_in, Th_out, Tc_in, Tc_out)

area = heat_exchanger_area(abs(Qh), U, delta_Tlm)

error = error_percentage(Qh, Qc)

Ch= capacity_rate(m_h, Cp_h)

Cc= capacity_rate(m_c, Cp_c)

Cr = capacity_ratio(Ch, Cc)

#Qmax is the maximum possible heat transfer that can occur in the heat exchanger
#It is calculated using the minimum heat capacity rate and the temperature difference between the hot and cold fluids at their respective inlets.
Qmax=min(Ch, Cc)*(Th_in-Tc_in)

effectiveness = abs(Qc)/Qmax

NTU = U * area / min(Ch, Cc)




#analyzing the effectiveness of the heat exchanger and providing recommendations based on its value
if effectiveness < 0.5:
    print("The heat exchanger is not very effective. Consider redesigning or optimizing the system.")
elif math.isclose(effectiveness, 1):
    print("The heat exchanger is ideal.")
elif effectiveness > 0.5 and effectiveness < 1:
    print("The heat exchanger is moderately effective. There may be room for improvement.")
elif effectiveness > 1:
    print("Warning: Effectiveness exceeds 1. Check inputs.")
print("Area that can be used for heat transfer: {:.4f} m²".format(area))



### Displaying input parameters and results in a formatted manner
plt.figure(figsize=(12,7))
plt.axis('off')

# Left side - Input Parameters
inputs = f"""
INPUT PARAMETERS

Hot Fluid
------------
Inlet Temperature : {Th_in:.4f} K
Outlet Temperature: {Th_out:.4f} K
Cp               : {Cp_h:.4f} kJ/kgK
Mass Flow Rate   : {m_h:.4f} kg/s

Cold Fluid
------------
Inlet Temperature : {Tc_in:.4f} K
Outlet Temperature: {Tc_out:.4f} K
Cp               : {Cp_c:.4f} kJ/kgK
Mass Flow Rate   : {m_c:.4f} kg/s

Overall U
------------
{U_input:.4f} W/m²K
"""

# Right side - Results
results = f"""
CALCULATED RESULTS

Heat Duty (Hot)      : {Qh:.4f} kW
Heat Duty (Cold)     : {Qc:.4f} kW

LMTD                 : {delta_Tlm:.4f} K
NTU                  : {NTU:.4f}
Required Area        : {area:.4f} m²

Percentage Error     : {error:.4f} %

Capacity Rate (Hot)  : {Ch:.4f} kW/K
Capacity Rate (Cold) : {Cc:.4f} kW/K

Cmin                 : {min(Ch,Cc):.4f} kW/K
Capacity Ratio (Cr)  : {Cr:.4f}

Qmax                 : {Qmax:.4f} kW
Effectiveness        : {effectiveness:.4f}
"""

# Left column
plt.text(
    0.05, 0.95,
    inputs,
    fontsize=11,
    family='monospace',
    verticalalignment='top',
    bbox=dict(facecolor='lightyellow', edgecolor='black')
)

# Right column
plt.text(
    0.55, 0.95,
    results,
    fontsize=11,
    family='monospace',
    verticalalignment='top',
    bbox=dict(facecolor='lightcyan', edgecolor='black')
)

plt.title("--------------------------------------------------------------\nHEAT EXCHANGER DESIGN AND PERFORMANCE REPORT\n--------------------------------------------------------------", fontsize=14)
plt.show()




# Plotting the temperature profiles of hot and cold fluids

## A v/s U plot
U_values =[]
A_values =[]

for U_W in range(100, 2100, 100):
    U_values.append(U_W)
    U_kW = U_W / 1000
    A_values.append(heat_exchanger_area(abs(Qh), U_kW, delta_Tlm))

plt.plot(U_values, A_values, marker='o', color='orange')
plt.xlabel("Overall Heat Transfer Coefficient (W/m²K)")
plt.ylabel('Required Heat Exchanger Area (m²)')
plt.title('Heat Exchanger Design Analysis')
plt.grid(True)
plt.show()

## A v/s heat fluid flow rate plot
m_h_values =[]
A_values_mh =[]
for mh in range(1, 21):
    m_h_values.append(mh)
    Qh_temp = heat_duty(Th_in, Th_out, Cp_h, mh)
    A_values_mh.append(heat_exchanger_area(abs(Qh_temp), U, delta_Tlm))

plt.plot(m_h_values, A_values_mh, marker='o', color='red')
plt.xlabel('Hot Fluid Mass Flow Rate (kg/s)')
plt.ylabel('Required Heat Exchanger Area (m²)')
plt.title('Heat Exchanger Area vs Hot Fluid Mass Flow Rate')
plt.grid(True)
plt.show()

## A v/s cold fluid flow rate plot
m_c_values =[]
A_values_mc =[]
for mc in range(1, 21):
    m_c_values.append(mc)
    Qc_temp = heat_duty(Tc_in, Tc_out, Cp_c, mc)
    A_values_mc.append(heat_exchanger_area(abs(Qc_temp), U, delta_Tlm))


plt.plot(m_c_values, A_values_mc, marker='o', color='blue')
plt.xlabel('Cold Fluid Mass Flow Rate (kg/s)')
plt.ylabel('Required Heat Exchanger Area (m²)')
plt.title('Heat Exchanger Area vs Cold Fluid Mass Flow Rate')
plt.grid(True)
plt.show()


## effectiveness v/s U
U_values_eff =[]
effectiveness_values =[]
fixed_area = area

for U_W in range(100,2100,100):
    U_values_eff.append(U_W)

    U_kW = U_W / 1000

    NTU = U_kW * fixed_area / min(Ch,Cc)

    effectiveness_values.append(effectiveness_counterflow(NTU, Cr))

plt.plot(U_values_eff, effectiveness_values, marker='o', color='purple')
plt.xlabel('Overall Heat Transfer Coefficient (W/m²K)')
plt.ylabel('Effectiveness')
plt.title('Effectiveness vs Overall Heat Transfer Coefficient')
plt.grid(True)
plt.show()

## parallel v/s counter flow effectiveness comparison
effectiveness_parallel = []
effectiveness_counter = []
NTU_values = list(range(1, 21))
for NTU_temp in range(1, 21):
    effectiveness_parallel.append((1 - math.exp(-NTU_temp * (1 + Cr))) / (1 + Cr))
    effectiveness_counter.append(effectiveness_counterflow(NTU_temp, Cr))
plt.plot(NTU_values, effectiveness_parallel, label='Parallel Flow')
plt.plot(NTU_values, effectiveness_counter, label='Counter Flow')
plt.xlabel('NTU')
plt.ylabel('Effectiveness')
plt.title('Effectiveness Comparison: Parallel vs Counter Flow')
plt.grid(True)
plt.legend()
plt.show()
