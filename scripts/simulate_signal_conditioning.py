#!/usr/bin/env python3
"""
DIY Flex Sensor Signal Conditioning Circuit Simulator
Author: M. Dilushan (Reg No: 2021/PS/42)
Project: High-Impedance Piezoresistive Flex Sensor Design

This script simulates:
1. Piezoresistive resistance response of DIY carbon flex sensor under bending.
2. 50Hz AC mains electromagnetic noise pickup.
3. First-order RC low-pass filtering.
4. LM324 op-amp non-inverting buffer stage with potentiometer calibration.
5. Inverting comparator (NOT gate) threshold switching with LED actuation.
"""

import math
import os
import sys

def simulate_signal_conditioning():
    # Circuit Parameters
    VCC = 8.0               # Volts
    R_pullup = 1.0e6        # 1.00 MOhm
    C_filter = 100.0e-9     # 100 nF (0.1 uF)
    V_ref = 4.0             # 4.0V Comparator Threshold
    
    # Simulation Time Domain
    t_start = 0.0
    t_end = 4.0             # 4 seconds
    fs = 2000               # 2000 Hz sampling rate
    dt = 1.0 / fs
    total_steps = int((t_end - t_start) * fs)
    
    # Time array
    time_pts = [i * dt for i in range(total_steps)]
    
    # Resistance Profile:
    # 0.0s - 1.0s: Flat state (R_flex ~ 1.5 MOhm)
    # 1.0s - 1.5s: Bending motion towards 90 deg (R_flex drops as carbon clusters compress/shift to ~ 400 kOhm)
    # 1.5s - 2.8s: Held bent at 90 deg (R_flex ~ 400 kOhm)
    # 2.8s - 3.4s: Release motion back to flat (R_flex recovers to ~ 1.5 MOhm)
    # 3.4s - 4.0s: Quiescent flat state
    
    r_flex = []
    v_raw = []
    v_filt = []
    v_buf = []
    v_comp = []
    led_state = []
    
    # 50 Hz Mains Noise Amplitude
    v_noise_amp = 0.25      # 250 mV peak-to-peak 50 Hz mains hum
    
    # Filter state variable
    v_c = (VCC * 1.5e6) / (R_pullup + 1.5e6)  # Initial DC voltage across capacitor
    
    for t in time_pts:
        # 1. Calculate Sensor Resistance R_flex(t)
        if t < 1.0:
            r = 1.5e6
        elif 1.0 <= t < 1.5:
            # Smooth transition from 1.5M to 400k
            progress = (t - 1.0) / 0.5
            r = 1.5e6 - (1.1e6 * 0.5 * (1 - math.cos(math.pi * progress)))
        elif 1.5 <= t < 2.8:
            r = 4.0e5
        elif 2.8 <= t < 3.4:
            # Smooth transition back to 1.5M
            progress = (t - 2.8) / 0.6
            r = 4.0e5 + (1.1e6 * 0.5 * (1 - math.cos(math.pi * progress)))
        else:
            r = 1.5e6
        r_flex.append(r)
        
        # 2. Theoretical Divider Node Voltage with 50Hz AC Mains Noise
        v_dc = VCC * (r / (R_pullup + r))
        noise = v_noise_amp * math.sin(2.0 * math.pi * 50.0 * t)
        v_in = max(0.0, min(VCC, v_dc + noise))
        v_raw.append(v_in)
        
        # 3. RC Low-Pass Filter Simulation (Forward Euler discretization)
        # R_th = R_pullup || R_flex
        r_th = (R_pullup * r) / (R_pullup + r)
        tau = r_th * C_filter
        alpha = dt / (tau + dt)
        v_c = v_c + alpha * (v_in - v_c)
        v_filt.append(v_c)
        
        # 4. Op-Amp Buffer Stage (Unity-gain buffer tuned by potentiometer)
        # Saturated between 0.05V and (VCC - 1.4V) for LM324
        v_b = max(0.05, min(VCC - 1.4, v_c))
        v_buf.append(v_b)
        
        # 5. Inverting Comparator Stage (NOT Gate)
        # Inverting terminal (Pin 9) receives v_buf; Non-inverting (Pin 10) is V_ref (4.0V)
        # If v_buf < V_ref -> Output is HIGH (approx VCC - 1.5V = 6.5V)
        # If v_buf >= V_ref -> Output is LOW (approx 0.02V)
        if v_b < V_ref:
            v_out = VCC - 1.5   # ~6.5V
            state = 1           # LED ON
        else:
            v_out = 0.02        # ~0.02V
            state = 0           # LED OFF
            
        v_comp.append(v_out)
        led_state.append(state)
        
    print("=" * 60)
    print("DIY FLEX SENSOR SIGNAL CONDITIONING SIMULATION RESULTS")
    print("Author: M. Dilushan (Reg No: 2021/PS/42)")
    print("=" * 60)
    print(f"Sampling frequency: {fs} Hz | Total duration: {t_end} s")
    print(f"R_pullup: {R_pullup/1e6:.2f} MOhm | C_filter: {C_filter*1e9:.0f} nF")
    print(f"Theoretical Cutoff Frequency fc: {1.0 / (2.0 * math.pi * ((R_pullup * 1.5e6) / (R_pullup + 1.5e6)) * C_filter):.2f} Hz")
    print("-" * 60)
    print("Condition        | Sensor R (MOhm) | Raw V_node (V) | Filtered V (V) | Comp Out (V) | LED State")
    print("-" * 60)
    
    sample_indices = [
        (int(0.5 * fs), "Flat (Resting)"),
        (int(1.25 * fs), "Transitioning "),
        (int(2.0 * fs), "Bent (90 deg)  "),
        (int(3.1 * fs), "Returning     "),
        (int(3.8 * fs), "Flat Recovered")
    ]
    
    for idx, label in sample_indices:
        print(f"{label} |      {r_flex[idx]/1e6:4.2f}       |     {v_raw[idx]:4.2f}     |     {v_filt[idx]:4.2f}     |    {v_comp[idx]:4.2f}      |   {'ON' if led_state[idx] else 'OFF'}")
        
    print("=" * 60)
    
    # Export simulation data to CSV
    csv_dir = os.path.join(os.path.dirname(__file__), "..", "hardware")
    os.makedirs(csv_dir, exist_ok=True)
    csv_path = os.path.join(csv_dir, "simulation_data.csv")
    with open(csv_path, "w") as f:
        f.write("Time_s,R_flex_Ohm,V_raw_V,V_filtered_V,V_comparator_V,LED_State\n")
        # Subsample for CSV size efficiency (every 10th sample)
        for i in range(0, total_steps, 10):
            f.write(f"{time_pts[i]:.4f},{r_flex[i]:.1f},{v_raw[i]:.3f},{v_filt[i]:.3f},{v_comp[i]:.3f},{led_state[i]}\n")
    print(f"[OK] Simulation dataset exported to: {os.path.abspath(csv_path)}")

if __name__ == "__main__":
    simulate_signal_conditioning()
