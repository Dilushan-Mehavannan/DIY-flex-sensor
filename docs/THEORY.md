# Theoretical Derivations & Analytical Foundations

This document provides the mathematical derivations, semiconductor physics, and electrical network equations governing the DIY Piezoresistive Flex Sensor and its analog signal conditioning circuitry.

---

## 1. Piezoresistive Transduction & Percolation Conduction

The sensor utilizes a flexible polymer substrate coated with a conductive carbon particulate composite. The electrical conductivity of carbon-polymer composites is governed by **Percolation Theory** and quantum tunneling:

$$\sigma \propto (\phi - \phi_c)^t \quad \text{for } \phi > \phi_c$$

Where:
- $\sigma$ is the bulk electrical conductivity.
- $\phi$ is the volume fraction of conductive carbon particles.
- $\phi_c$ is the percolation threshold (the critical volume fraction required to form continuous conductive chains).
- $t$ is the universal critical exponent (typically $1.6 - 2.0$ for three-dimensional networks).

### Mechanical Strain & Resistance Variation
When the sensor substrate of thickness $h$ is bent to a radius of curvature $\rho$ (or angle $\theta$), the mechanical strain $\epsilon$ along the convex outer surface is given by:

$$\epsilon = \frac{y}{\rho} = \frac{h / 2}{\rho}$$

As strain increases:
1. The average inter-particle separation distance $s$ between adjacent carbon micro-aggregates increases ($s' = s(1 + \epsilon)$).
2. Quantum tunneling transmission probability $T(s)$ decays exponentially with separation distance:
   $$T(s) \propto \exp\left(-2 \frac{\sqrt{2m(\Phi - E)}}{\hbar} \cdot s\right)$$
3. Percolation pathways are severed, resulting in a dramatic increase in bulk electrical resistance ($R_{flex}$).

---

## 2. Voltage Divider & Source Impedance Matching

Given that DIY carbon tracks produce an unbent baseline resistance $R_{flex} \approx 1\text{ M}\Omega$, standard voltage dividers using low resistors (e.g., $10\text{ k}\Omega$) yield severe attenuation:

$$V_{node} = V_{CC} \cdot \frac{R_{flex}}{R_{pullup} + R_{flex}}$$

If $R_{pullup} = 10\text{ k}\Omega$ and $R_{flex} = 1\text{ M}\Omega$:
$$V_{node} = 8.0\text{ V} \cdot \frac{10^6}{10^4 + 10^6} = 8.0 \cdot 0.990 = 7.92\text{ V}$$

When $R_{flex}$ varies by $100\text{ k}\Omega$, the node voltage changes by only $\approx 0.07\text{ V}$, resulting in poor sensitivity.

### Matched Impedance Design ($R_{pullup} = 1.00\text{ M}\Omega$)
By selecting $R_1 = 1.00\text{ M}\Omega \approx R_{flex, nominal}$:

$$\left.\frac{\partial V_{node}}{\partial R_{flex}}\right|_{R_{flex} = R_1} = \frac{V_{CC} \cdot R_1}{(R_1 + R_{flex})^2} = \frac{V_{CC}}{4 R_1}$$

This maximizes the small-signal sensitivity of the voltage divider network.

---

## 3. Passive RC Low-Pass Filter Frequency Response

A $0.1\,\mu\text{F}$ ($100\text{ nF}$) ceramic capacitor ($C_1$) is placed across the flex sensor node to ground.

### Equivalent Thevenin Impedance
Looking into the divider node, the Thevenin equivalent resistance $R_{th}$ is the parallel combination of the pull-up resistor and sensor resistance:

$$R_{th} = R_1 \parallel R_{flex} = \frac{R_1 \cdot R_{flex}}{R_1 + R_{flex}}$$

At nominal flat condition ($R_1 = 1\text{ M}\Omega$, $R_{flex} \approx 1\text{ M}\Omega$):

$$R_{th} = \frac{1\text{ M}\Omega \cdot 1\text{ M}\Omega}{1\text{ M}\Omega + 1\text{ M}\Omega} = 500\text{ k}\Omega$$

### Cutoff Frequency ($f_c$)
The $-3\text{ dB}$ corner frequency of the first-order low-pass filter is:

$$f_c = \frac{1}{2\pi \cdot R_{th} \cdot C_1} = \frac{1}{2\pi \cdot (500 \times 10^3\,\Omega) \cdot (100 \times 10^{-9}\,\text{F})}$$

$$f_c = \frac{1}{2\pi \times 0.05} = \frac{1}{0.31416} \approx 3.183\text{ Hz}$$

### Attenuation at $50\text{ Hz}$ AC Mains Hum
The transfer function of the low-pass filter is:

$$|H(j\omega)| = \frac{1}{\sqrt{1 + \left(\frac{f}{f_c}\right)^2}}$$

At $f = 50\text{ Hz}$:

$$|H(j 50)| = \frac{1}{\sqrt{1 + \left(\frac{50}{3.183}\right)^2}} = \frac{1}{\sqrt{1 + (15.7)^{2}}} \approx \frac{1}{15.74} \approx 0.0635$$

In decibels:

$$\text{Attenuation} = 20 \log_{10}(0.0635) \approx -23.94\text{ dB}$$

The filter provides approximately **$24\text{ dB}$ of attenuation** against $50\text{ Hz}$ mains electromagnetic hum, while easily passing typical human flexure dynamics ($0 - 2\text{ Hz}$).

---

## 4. Buffer Amplifier Loading & Input Bias Current

The LM324N operational amplifier utilizes a Darlington PNP input differential pair.
- Input Bias Current ($I_B$): $\approx 20\text{ nA}$ typical (maximum $100\text{ nF}$ over temperature).
- Input Resistance ($R_{in}$): $> 1\text{ M}\Omega$ (open loop), and dynamically exceeds $> 100\text{ M}\Omega$ under non-inverting closed-loop feedback.

The maximum voltage offset drop caused by input bias current through the $500\text{ k}\Omega$ Thevenin source is:

$$\Delta V_{offset} = I_B \cdot R_{th} \approx 20\text{ nA} \times 500\text{ k}\Omega = 10\text{ mV}$$

A $10\text{ mV}$ offset is completely negligible compared to the multi-volt dynamic range of the sensor, validating the LM324N as a cost-effective single-supply buffer.

---

## 5. Comparator Reference & LED Driver Calculation

### Reference Threshold Generation
A voltage divider formed by two identical $10.0\text{ k}\Omega$ resistors ($R_2, R_3$) generates the switching threshold:

$$V_{ref} = V_{CC} \cdot \frac{R_3}{R_2 + R_3} = 8.0\text{ V} \cdot \frac{10\text{ k}\Omega}{20\text{ k}\Omega} = 4.00\text{ V}$$

### Comparator Output States (LM324N Pin 8)
- **Quiescent (Unbent):**
  $$V_{Pin9} > 4.0\text{ V} \implies V_{Pin8} = V_{OL} \approx 0.02\text{ V} \implies \text{LED OFF}$$
- **Bent (Actuated):**
  $$V_{Pin9} < 4.0\text{ V} \implies V_{Pin8} = V_{OH} \approx V_{CC} - 1.5\text{ V} \approx 6.5\text{ V} \implies \text{LED ON}$$

### LED Current Limiting Resistor ($R_4 = 330\,\Omega$)
For a standard $5\text{ mm}$ Red LED with forward voltage $V_F \approx 2.0\text{ V}$:

$$I_D = \frac{V_{OH} - V_F}{R_4} = \frac{6.5\text{ V} - 2.0\text{ V}}{330\,\Omega} = \frac{4.5\text{ V}}{330\,\Omega} \approx 13.64\text{ mA}$$

The calculated current of $13.6\text{ mA}$ is well within the LM324N output source capability (typically $20 - 40\text{ mA}$) and safe LED ratings ($20\text{ mA}$ max continuous).
