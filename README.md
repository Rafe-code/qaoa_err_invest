# Investigating Angle-Dependent Errors in Rzz and Rx Gates on IBM Quantum Hardware

**Author:** Rafe Whitehead  
**Date:** April 2025

---

## 1. Overview

This project investigates how the error profiles of the IBM `Rzz` and `Rx` quantum gates vary as a function of rotation angle. These gates are significant sources of error in the implementations of near-term quantum algorithms, such as the Quantum Approximation Optimisation Algorithm (QAOA). If the `Rzz` and `Rx` gates have lower error rates at specific rotation angles, it is possible the error accumulation of the implemented circuits could be reduced by tuning the circuit such that the expected rotations of the `Rzz` and `Rx` gates lie within low error domains.

---

## 2. Background

The QAOA algorithm [\[1\]](#ref-1) holds potential within the Noisy Intermediate Scale Quantum (NISQ) era of quantum computers due to its low required circuit depth and application to combinatorial optimisation problems [\[2\]](#ref-2). This algorithm optimises gate parameters in the quantum circuit by evaluating the circuit repeatedly within a classical optimiser. However, this optimisation often suffers from barren plateaus and has a cost associated with each evaluation, both directly (through energy usage) and indirectly (through time taken). To reduce the number of optimisation evaluations required, work has therefore been done to determine suitable initial parameters for the quantum circuit. The initial parameters can be determined using, for instance, bilinear strategy, TQA initialisation [\[3\]](#ref-3), or transfer learning [\[4\]](#ref-4).

For hardware implementations, each operation has an associated error attached to it. The accumulation of these errors negatively impacts the results produced, reducing the probability of the optimum result. For QAOA, the gate errors comprise mainly of the `Rzz` and `Rx` gates, which can be thought of as rotations around the Z or X axis of a Bloch sphere respectively. If the error of each operation is a function of the angle of rotation applied, overall error could be reduced by applying offsets to the gates to reduce the error at the angles of rotation given in the initialisation strategies (which are expected to be close to the final rotation angles used). This is interpreted as an adjustment to the initial preparation state of the qubits or a different global phase. These changes will have errors associated with them, but this is neglected here.

The efficacy of this potential approach is dependent upon the existence and strength of a relationship between the error profile of `Rzz` and `Rx` gates and their rotation angle.

---

## 3. Methodology

For this investigation, freely-available IBM hardware was used due to its accessibility and record of strong documentation online through the open-source library QISKIT [\[5\]](#ref-5). All devices offered under the free plan have identical specifications. The device `ibm_brisbane` was chosen arbitrarily.

On IBM devices, QAOA algorithms are implemented using layers of `Rx(θ)` and `Rzz(θ)` gates, where a single layer QAOA can be decomposed as shown in [Figure 1](#fig-1) [\[6\]](#ref-6). In this implementation, the error rate is dominated by the 2-qubit `Rzz` gate, with IBM reporting an error rate two orders of magnitude higher for the `Rzz` gate as compared to the `Rx` gate for `ibm_brisbane` [\[7\]](#ref-7). In this investigation, these gates were probed independently for their relationship between fidelity and angle of rotation. Due to the larger contribution of the `Rzz` gate to the overall QAOA circuit error, this gate was investigated using the limited free resources of the `ibm_brisbane` device. The `Rx` gate was investigated using only the IBM simulator provided in QISKIT, loaded with an `ibm_brisbane` noise model.

![QAOA Single Layer Circuit](images/QAOA_single_layer_rx_rzz.png)  
**Figure 1:** A single layer of the IBM implemented QAOA circuit, showing the arrangement of `Rx` and `Rzz` gates.  
<a id="fig-1"></a>

The `Rx` gate was investigated using the circuit shown in [Figure 2](#fig-2). This circuit was evaluated on the IBM simulator with an `ibm_brisbane` noise model using an input of `|1⟩` for \(2^{16}\) shots, repeated 5 times. When loaded with the input `|1⟩`, the anticipated result is `|1⟩`. The fidelity of this gate can be measured directly by finding the probability of generating the expected `|1⟩` state. This was done for 50 angles equally spaced between 0 and π, which covers the full angle range of the `Rx` gate due to symmetries around 0 and π.

![Circuit for Rx Investigation](images/rx_investigation_circuit.png)  
**Figure 2:** Circuit used to explore the error profile of the `Rx` gate.  
<a id="fig-2"></a>

The `Rzz` gate was also probed by comparing the results of an evaluated circuit to anticipated results. However, as a 2-qubit gate, the `Rzz` gate requires a more complex circuit to probe as compared to the `Rx` gate, as shown in [Figure 3](#fig-3).

![Circuit for Rzz Investigation](images/rzz_investigation_circuit.png)  
**Figure 3:** Circuit used to explore the error profile of the `Rzz` gate.  
<a id="fig-3"></a>

This circuit was evaluated on the `ibm_brisbane` hardware device using an input of `|00⟩` 2^{16} shots, repeated 3 times over differing dates (other hardware options were left as default values, see [\[8\]](#ref_default_options) for details). When loaded with the input `|00⟩`, the anticipated result, `|φ⟩`, is an equal superposition between all possible output states, given by:

|φ⟩ = (1/2) (|00⟩ + |01⟩ + |10⟩ + |11⟩)

This was done for 20 equally spaced angles between 0 and π, which covers the full angle range of the `Rzz` gate due to symmetries around 0 and π. This implementation of the `Rzz` gate has four possible outcomes, so simple approaches to the fidelity (as taken for the `Rx` gate) could obscure behaviour of specific outcomes. Therefore, for each outcome, the measured counts for each output were compared to the expected count using:

RelError = (N<sub>measured</sub> - N<sub>expected</sub>) / N<sub>expected</sub>

where:

N<sub>expected</sub> = N<sub>shots</sub> / 4

This was done for 3 separate initialisations of the `ibm_brisbane` device over 2 separate dates, for a number of shots given by (2<sup>16</sup>, 2<sup>15</sup>, 2<sup>15</sup>). The reduced number of shots was necessitated by limitations on the IBM device runtime available.

A summary of this can be seen in [Table 1](#gate-table).

---

<a id="gate-table"></a>

### Table 1: Summary of Gate Investigations

| Gate | Circuit | Input | Expected Output |

| ------ | -------------------------------- | ----- | --------------- | ----- | ----- | ----- | ----- | ---- |

| Rx(θ) | H → Rx(θ) → H → Measure | | 0⟩ | | 1⟩ |

| Rzz(θ) | H ⊗ H → Rzz(θ) → H ⊗ H → Measure | |00⟩ | 1/2 ( |00⟩ + |01⟩ + |10⟩ + |11⟩) |

---

## 4. Results

The results of the `Rzz` gate investigation can be seen in [Figure 4](#fig-4), where the errors are the total length of the standard deviation across the three initialisations of the devices over the separate dates.

![Rzz Gate Results](images/rzz_err_by_angle_hardware_3reps.png)  
**Figure 4:**Results of the `Rzz` gate angle investigation, showing the relative error for each output channel. Different behaviour can be observed for each of the channels, but these is limited evidence of a relationship between the rotation angle and error rate for each channel.
<a id="fig-4"></a>

It is clear from [Figure 4](#fig-4) that there is different behaviour of each of the output channels, with |01⟩ and |11⟩ systematically being detected more often than expected (showing leakage into these channels). Channel |00⟩ is systematically detected less often than expected (showing leakage out of this channel) and the channel |10⟩ shows evidence of both under and over detecting. Channels |01⟩ and |11⟩ also show no evidence of a relationship between the rotation angle and the error rate, the difference between the expected and measured counts being roughly stable across the 0 to π range. Channels |00⟩ and |10⟩ show potential relationships between the rotation angle and fidelity. Interestingly, the responses of these channels are roughly symmetrical around the x = 0.5π line. Channel |00⟩ has a high error rate over the [0π to 0.6π] range, peaking near 0.2π, and a low error rate over the [0.6π to 1.0π] range. On the other hand, channel |10⟩ has a high error rate over the [0.6π to 1.0π] range, peaking near 0.8π, and a low error rate over the [0.0π to 0.6π] range. However, the lack of evidence of a strong relationship between angle and fidelity in [Figure 4](#fig-4) and the mirrored responses of the channels |00⟩ and |10⟩ mean the proposed error minimisation strategy through angle offsets is not likely to succeed, as any improvement made to the error rate of the |00⟩ channel would be offset by deteriorations in the |10⟩ channel error rate, and vice verse (while the error rates of channels |01⟩ and |11⟩ will be roughly unchanged).

![Rx Gate Results](images/ibm_rx_error_5_16384_even_more.png)  
**Figure 5:** Results of the `Rx` gate angle investigation, showing the relative error against the rotation angle. A clear sinusodial relationship can be seen, with a period of 0.5\(\pi\) and amplitude of .
<a id="fig-5"></a>

The results of the `Rx` gate investigation can be seen in [Figure 5](#fig-5). This investigation shows clear evidence of a sinusoidal dependence between the angle of rotation and the fidelity of the gate. This relationship has a period of 0.5π, and the `Rx` gate has its highest error rates at rotation angles of [0π, 0.5π, 1.0π] and lowest error rates at rotation angles near [0.25π, 0.75π]. The peak to trough difference is significant, varying between a rate of 0.45 and 0.04, a peak to trough drop of 90%. It is noted that this error rate far exceeds the reported `Rx` error value for `ibm_brisbane`, likely due to error mitigation techniques employed by the hardware which are not utilised here (the `Rx` gate investigation was conducted using an IBM simulator loaded with an `ibm_brisbane` noise model).

While the `Rx` gate shows significant correlation between its fidelity and rotation angle, the error rate current QAOA implementations are dominated by the `Rzz` gate contribution. While this remains the case, improvements to the fidelity of the `Rx` gate would provide negligible (and undetectable) benefit to the quality of QAOA generated results. This inhibits investigations into whether QAOA results can be improved by leveraging `Rx` gates tuned to low error rotation angles.

---

## 5. Conclusion

This preliminary work indicates that the `Rx` gate has a strong and sinusoidal dependence between its fidelity and rotation angle, with the error rate reducing by 90% from peak to trough. However, the overall contribution of this gate's error in the QAOA implementation is negligible. The error accumulations in QAOA are instead dominated by the effects of the `Rzz` gate. The work done here shows potential evidence of a relationship between rotation angle and the fidelity of the `Rzz` gate for the output channels of 00 and 10. However, evidence of this relationship is weak, and these channels have mirrored error profiles, meaning there are no angles at which the overall error profile of the `Rzz` gate is minimised.

---

## References

1. <a id="ref-1"></a> E. Farhi, J. Goldstone. "A Quantum Approximate Optimization Algorithm," 2014. [arXiv:1411.4028](https://arxiv.org/abs/1411.4028).
2. <a id="ref-2"></a> L. Zhou et al. "Quantum Approximate Optimization Algorithm: Performance, Mechanism, and Implementation on Near-Term Devices," 2019. [arXiv:1812.01041](https://arxiv.org/pdf/1812.01041).
3. <a id="ref-3"></a> X. Lee et al. "Parameters Fixing Strategy for Quantum Approximate Optimization Algorithm," 2021. [arXiv:2108.05288](https://arxiv.org/pdf/2108.05288).
4. <a id="ref-4"></a> R. Shaydulin et al. "Parameter Transfer for Quantum Approximate Optimization of Weighted MaxCut," 2023. [arXiv:2201.11785](https://arxiv.org/pdf/2201.11785).
5. <a id="ref-5"></a> IBM. QISKIT, accessed 2025. [Docs](https://docs.quantum.ibm.com/guides).
6. <a id="ref-6"></a> IBM. QISKIT QAOA Documentation, accessed 2025. [Docs](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.qaoa_ansatz).
7. <a id="ref-7"></a> IBM. `ibm_brisbane` specifications, accessed 2025. [Link](https://quantum.ibm.com/services/resources?resourceType=current-instance&system=ibm_brisbane).
8. <a id="ref-8"></a> IBM. Default hardware options, accessed 2025. [Link](https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/sampler-v2).
