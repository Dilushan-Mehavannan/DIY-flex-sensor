# LM324N Pinout & Hardware Interconnect Guide

This document specifies the pinout configuration for the **LM324N Quad Operational Amplifier IC** as utilized in the High-Impedance DIY Flex Sensor Signal Conditioning circuit.

---

## LM324N IC Overview (DIP-14)

```
                     +---V---+
      OUTPUT 1 (1)  -| 1  14 |-  (14) OUTPUT 4
     INPUT 1-  (2)  -| 2  13 |-  (13) INPUT 4-
     INPUT 1+  (3)  -| 3  12 |-  (12) INPUT 4+
          VCC+ (4)  -| 4  11 |-  (11) GND / VCC-
     INPUT 2+  (5)  -| 5  10 |-  (10) INPUT 3+
     INPUT 2-  (6)  -| 6   9 |-  (9)  INPUT 3-
      OUTPUT 2 (7)  -| 7   8 |-  (8)  OUTPUT 3
                     +-------+
```

---

## Detailed Pin Utilization in This Project

| Pin Number | IC Function | Project Net / Signal Name | Connected Hardware Component | Functional Description |
|:---:|:---:|:---:|:---:|:---|
| **Pin 1** | Output 1 | `V_BUF_OUT` | RV1 (Potentiometer wiper/terminal) & Pin 9 (Input 3-) | Output of Op-Amp Stage 1 (Buffered / Conditioned sensor signal). |
| **Pin 2** | Input 1- | `V_BUF_FB` | RV1 (10 kΩ Potentiometer terminal) | Inverting input for Op-Amp Stage 1 feedback calibration. |
| **Pin 3** | Input 1+ | `V_SENSE_FILT` | Junction of R1 (1 MΩ pull-up), C1 (100 nF), & Flex Sensor | High-input-impedance non-inverting terminal receiving the filtered sensor divider voltage. |
| **Pin 4** | $V_{CC}$ | `+8.0V` | Power Supply Positive Rail (+8V DC) | Positive supply rail powering all internal op-amp stages. |
| **Pin 5** | Input 2+ | `NC / UNUSED` | Not connected (or tied to GND via high resistance) | Unused amplifier stage (Op-Amp 2). |
| **Pin 6** | Input 2- | `NC / UNUSED` | Not connected | Unused amplifier stage (Op-Amp 2). |
| **Pin 7** | Output 2 | `NC / UNUSED` | Not connected | Unused amplifier stage (Op-Amp 2). |
| **Pin 8** | Output 3 | `V_LOGIC_OUT` | Resistor R4 (330 Ω) -> Anode of Red LED | Output of Op-Amp Stage 3 (Analog Inverter / Comparator) delivering binary logic signal. |
| **Pin 9** | Input 3- | `V_COMP_IN` | Pin 1 (`V_BUF_OUT`) | Inverting input of comparator receiving conditioned sensor signal. |
| **Pin 10** | Input 3+ | `V_REF_4V` | Junction of R2 (10 kΩ) & R3 (10 kΩ) divider | Non-inverting input held at constant reference threshold ($+4.0\text{ V}$). |
| **Pin 11** | GND | `0V / GND` | Power Supply Common Ground (0V) | Negative supply / circuit ground reference. |
| **Pin 12** | Input 4+ | `NC / UNUSED` | Not connected | Unused amplifier stage (Op-Amp 4). |
| **Pin 13** | Input 4- | `NC / UNUSED` | Not connected | Unused amplifier stage (Op-Amp 4). |
| **Pin 14** | Output 4 | `NC / UNUSED` | Not connected | Unused amplifier stage (Op-Amp 4). |

---

## Test Points (TP) for Lab Oscilloscope & Multimeter Verification

| Test Point | Location | Expected Quiescent State (Flat) | Expected Actuated State (90° Bend) | Measurement Tool |
|:---:|:---|:---:|:---:|:---:|
| **TP1** | Pin 3 (`V_SENSE_FILT`) | High DC Voltage (~4.0V - 5.5V) with < 10 mV ripple | Drops significantly towards GND | Oscilloscope CH1 (DC Coupling) |
| **TP2** | Pin 10 (`V_REF_4V`) | Stable $4.00\text{ V} \pm 0.05\text{ V}$ DC | Stable $4.00\text{ V} \pm 0.05\text{ V}$ DC | DMM (DC Volts mode) |
| **TP3** | Pin 1 (`V_BUF_OUT`) | Conditioned voltage $> 4.0\text{ V}$ | Conditioned voltage $< 4.0\text{ V}$ | Oscilloscope CH1 |
| **TP4** | Pin 8 (`V_LOGIC_OUT`) | $0.0\text{ V}$ (Logic LOW, LED OFF) | $\approx 6.5\text{ V} - 7.2\text{ V}$ (Logic HIGH, LED ON) | DMM / Oscilloscope |
