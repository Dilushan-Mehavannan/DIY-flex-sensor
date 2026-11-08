# Hardware Setup, Calibration & Troubleshooting Guide

This guide details the step-by-step procedure to assemble, calibrate, and verify the High-Impedance Flex Sensor signal conditioning testbench.

---

## 1. Safety & Required Equipment

### Instruments Required
1. Regulated DC Power Supply (set to $+8.0\text{ V}$, current limit set to $100\text{ mA}$).
2. Dual-Channel Digital Storage Oscilloscope (DSO) or Analog Oscilloscope (e.g., Twintex TOS-2020CF).
3. 10x Oscilloscope Probes ($10\text{ M}\Omega$ input impedance recommended).
4. Digital Multimeter (DMM).
5. Solderless breadboard and jumper wires.

---

## 2. Step-by-Step Assembly Procedure

1. **Power Rails:**
   - Connect the $+8.0\text{ V}$ terminal of the bench supply to the red power rail of the breadboard.
   - Connect the power supply ground ($0\text{ V}$) to the blue/black ground rail of the breadboard.
2. **IC Placement:**
   - Insert the **LM324N** across the central trough of the breadboard.
   - Connect **Pin 4** to $+8.0\text{ V}$.
   - Connect **Pin 11** to **GND**.
3. **Reference Voltage Divider ($V_{ref} = 4.0\text{ V}$):**
   - Connect one $10\text{ k}\Omega$ resistor ($R_2$) between $+8.0\text{ V}$ and Pin 10.
   - Connect a second $10\text{ k}\Omega$ resistor ($R_3$) between Pin 10 and GND.
   - Verify with DMM: Pin 10 should read exactly $4.00\text{ V} \pm 0.05\text{ V}$.
4. **Sensor Divider & Low-Pass Filter:**
   - Connect a $1.00\text{ M}\Omega$ resistor ($R_1$) between $+8.0\text{ V}$ and Pin 3.
   - Connect the DIY flex sensor between Pin 3 and GND.
   - Connect the $0.1\,\mu\text{F}$ ($100\text{ nF}$) ceramic capacitor ($C_1$) in parallel across Pin 3 and GND.
5. **Buffer Stage & Feedback Potentiometer:**
   - Connect the $10\text{ k}\Omega$ potentiometer ($RV_1$) between Pin 1 (Output 1) and Pin 2 (Inverting Input 1).
   - Route Pin 1 to Pin 9 (Inverting input of Op-Amp 3).
6. **Output Indicator Stage:**
   - Connect a $330\,\Omega$ resistor ($R_4$) from Pin 8 (Output 3) to the Anode (longer leg) of the Red LED.
   - Connect the Cathode (shorter leg / flat rim) of the LED to GND.

---

## 3. Calibration Procedure

```
[Power On (+8V)] ---> [Probe Pin 10 (Verify 4.0V)] ---> [Keep Sensor Flat] ---> [Adjust RV1 until LED turns OFF] ---> [Bend Sensor to 90°: Verify LED turns ON]
```

1. **Baseline State (Flat):**
   - Place the DIY flex sensor completely flat on a non-conductive surface.
   - Connect Oscilloscope Channel 1 to **Pin 1**.
   - Slowly rotate potentiometer $RV_1$ until the DC voltage at Pin 1 sits slightly above the reference threshold (around $4.5\text{ V} - 5.0\text{ V}$).
   - Verify that the LED at Pin 8 is **completely extinguished** ($0\text{ V}$).
2. **Actuation State (Bent):**
   - Manually deflect the flex sensor to an angle between 45° and 90°.
   - Observe that the voltage at Pin 1 drops below $4.0\text{ V}$.
   - Observe that the LED at Pin 8 immediately **illuminates brightly** (output transitions to $\approx 6.5\text{ V} - 8.0\text{ V}$).
3. **Sensitivity Fine-Tuning:**
   - If the LED turns on too easily (excessive sensitivity): Turn $RV_1$ slightly clockwise to raise the quiescent baseline voltage.
   - If the sensor requires excessive bending force to trigger: Turn $RV_1$ counter-clockwise closer to the $4.0\text{ V}$ threshold.

---

## 4. Troubleshooting Matrix

| Symptom | Probable Cause | Diagnostic & Corrective Action |
|:---|:---|:---|
| **LED always ON regardless of bend** | Quiescent voltage at Pin 9 is $< 4.0\text{ V}$ or sensor disconnected | Check sensor connection; verify $R_1$ ($1\text{ M}\Omega$) pull-up; rotate $RV_1$ clockwise to increase Pin 1 voltage. |
| **LED never turns ON upon bending** | Pin 1 voltage stays $> 4.0\text{ V}$ or LED reversed | Check LED polarity (Anode to $330\,\Omega$, Cathode to GND); inspect carbon track conductivity during bending. |
| **Oscilloscope shows 50Hz sine wave ripple** | $C_1$ ($100\text{ nF}$) filter capacitor missing or loose | Ensure $C_1$ is firmly seated between Pin 3 and GND; check earth ground of bench supply. |
| **Circuit behaves erratically when touched** | High-impedance node floating | Verify DIY flex sensor ground connection; ensure all breadboard contacts are snug. |
