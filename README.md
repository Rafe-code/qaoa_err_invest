<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Angle Dependence of Rzz and Rx Gate Errors on IBM Quantum Hardware</title>
  <style>
    body { font-family: sans-serif; margin: 2rem; line-height: 1.6; }
    h1, h2 { color:rgb(228, 231, 232); }
    code { background: #f4f4f4; padding: 2px 5px; border-radius: 4px; }
    pre { background: #f4f4f4; padding: 1em; overflow-x: auto; }
    .note { background: #e8f0fe; padding: 1em; border-left: 4px solid #4285f4; margin: 1em 0; }
  </style>
  <script type="text/javascript" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>

</head>
<body>

  <h1>Investigating Angle-Dependent Errors in Rzz and Rx Gates on IBM Quantum Hardware</h1>

  <p><strong>Author:</strong> Rafe Whitehead <br />
  <strong>Date:</strong> April 2025</p>

  <h2>1. Overview</h2>
  <p>
    This project investigates how the error profiles of the IBM <code>Rzz</code> and <code>Rx</code> quantum gates vary as a function of rotation angle. These gates are significant sources of error in the implementations of near-term quantum algorithms, such as the Quantum Approximation Optimisation Algorithm (QAOA). If the <code>Rzz</code> and <code>Rx</code> gates have lower error rates at specific rotation angles, it is possible the error accumulation of the implemented circuits could be reduced by tuning the circuit such that the expected rotations of the <code>Rzz</code> and <code>Rx</code> gates lie within low error domains.
  </p>

  <h2>2. Background</h2>
  <p>
    The QAOA algorithm <a href="#ref_qaoa_foundation">[1]</a> holds potential within the Noisy Intermediate Scale Quantum (NISQ) era of quantum computers due to its low required circuit depth and application to combinatorial optimisation problems <a href="#ref_qaoa_rev">[2]</a>. This algorithm optimises gate parameters in the quantum circuit by evaluating the circuit repeatedly within a classical optimiser. However, this optimisation often suffers from barren plateaus and has a cost associated with each evaluation, both directly (through energy usage) and indirectly (through time taken). Therefore, work has been done to determine suitable initial parameters for the quantum circuit. The initial parameters can be determined using, for instance, bilinear strategy, TQA initialisation <a href="#ref_init_strats">[3]</a> or transfer learning <a href="#ref_qaoa_transfer">[4]</a>.
  </p>

  <p>
  For hardware implementations, each operation has an associated error attached to it. The accumulation of these errors negatively impacts the results produced, reducing the probability of the optimum result. For QAOA, the gate errors comprise mainly of the <code>Rzz</code> and <code>Rx</code> gates, which can be thought of as rotations around the Z or X axis of a Bloch sphere respectively. If the error of each operation is a function of the angle of rotation applied, overall error could be reduced by  applying offsets to the gates to reduce the error at the angles of rotation given in the initialisation strategies (which are expected to be close to the final rotation angles used). This is interpreted as an adjustment to the initial preparation state of the qubits or a different global phase. These changes will have errors associated with them, but this is neglected here. 
  </p>

  <p>
  The efficacy of this potential approach is dependent upon the existence and strength of a relationship between the error profile of <code>Rzz</code> and <code>Rx</code> gates and their rotation angle.
  </p>

  <h2>3. Methodology</h2>
  <p>
    For this investigation, freely-available IBM hardware will be used due to its accessibility and record of strong documentation online through the open-source library QISKIT <a href="#ref_qiskit_general">[5]</a>. All devices offered under the free plan have identical specifications. The device <code>ibm_brisbane</code> was chosen arbitrarily.

</p>
<p>
    On IBM devices, QAOA algorithms are implemented using layers of <code>Rx(θ)</code> and <code>Rzz(θ)</code> gates, where a single layer QAOA can be decomposed according to <a href="#qaoa_rx_rzz">Figure 1</a> <a href="#ref_qiskit_qaoa">[6]</a>. In this implementation, the error rate is dominated by the 2-qubit <code>Rzz</code> gate, with IBM reporting an error rate two orders of magnitude higher for the <code>Rzz</code> gate as compared to the <code>Rx</code> gate for <code>ibm_brisbane</code> <a href="#ref_brisbane_specs">[7]</a>. In this investigation, these gates were probed independently for their relationship between fidelity and angle of rotation. Due to the larger contribution of the <code>Rzz</code> gate to the overall QAOA circuit error, this gate was investigated using the limited free resources of the <code>ibm_brisbane</code> device. The <code>Rx</code> gate was investigated using only the IBM simulator provided in QISKIT, loaded with an <code>ibm_brisbane</code> noise model.
</p>
  <img src="images/QAOA_single_layer_rx_rzz.png", id="qaoa_rx_rzz",alt="QAOA Single Layer Circuit.", width="600" />
  <figcaption id="qaoa_rx_rzz_caption">Figure 1: A single layer of the IBM implemented QAOA circuit, showing the arrangement of <code>Rx</code> and <code>Rzz</code> gates.</figcaption>
<p>
    The Rx gate was investigated using the circuit given in <a href="#rx_invest_circ">Figure 2</a>. This circuit was evaluated on the IBM simulator with <code>ibm_brisbane</code> a noise model using an input of \(|1\rangle\) for \(2^{16}\) shots, repeated 5 times. When loaded with the input \(|1\rangle\), the anticipated result is \(|1\rangle\). The fidelity of this gate can be measured directly by finding the probability of generating the expected \(|1\rangle\) state. This was done for 50 angles equally spaced between 0 and \(\pi\), which covers the full angle range of the <code>Rx</code> gate due to symmetries around 0 and \(\pi\). 
</p>
  <img src="images/rx_investigation_circuit.png" id="rx_invest_circ" alt="Circuit used to explore error profile of the Rx gate." width="600" />
  <figcaption id="rx_invest_circ_caption">Figure 2: Circuit used to explore the error profile of the <code>Rx</code> gate.</figcaption>

<p>
    The <code>Rzz</code> gate is also probed by comparing the results of an evaluated circuit to anticipated results. However, as a 2-qubit gate, the <code>Rzz</code> gates requires a more complex circuit to probe as compared to the <code>Rx</code> gate, which can be seen in <a href="#rzz_invest_circ">Figure 3</a>. 
</p>
  <img src="images/rzz_investigation_circuit.png", id="rzz_invest_circ",alt="Circuit used to explore error profile of the Rzz gate.", width="600" />
  <figcaption id="rzz_invest_circ_caption">Figure 3: Circuit used to explore the error profile of the <code>Rzz</code> gate.</figcaption>
<p>
    This circuit was evaluated on the <code>ibm_brisbane</code> hardware device using an input of \(|00\rangle\) \(2^{16}\) shots, repeated 3 times over differing dates (other hardware options were left as default values, see <a href="#ref_default_options">[8]</a> for details). When loaded with the input \(|00\rangle\), the anticipated result, \(|\phi\rangle\) is an equal superposition between all possible output states, given by 
</p>
  <p>\[
    |\phi\rangle = \frac{1}{2} \left( |00\rangle + |01\rangle + |10\rangle + |11\rangle \right)
    \]</p>

<p>
    This was done for 20 equally spaced angles between 0 and \(\pi\), which covers the full angle range of the <code>Rzz</code> gate due to symmetries around 0 and \(\pi\). This implementation of the Rzz gate has four possible outcomes, so simple approaches to the fidelity (as taken for the <code>Rx</code> gate) could obscure behaviour of specific outcomes. Therefore, for each outcome, the measured counts for each output was compared to the expected count using
</p>
<p>
  \[
  \text{RelError} = \frac{N_{\text{measured}} - N_{\text{expected}}}{N_{\text{expected}}}
  \]
</p>
<p>
  where
</p>
<p>
  \[
  N_{\text{expected}} = \frac{N_{\text{shots}}}{4}
  \]
</p>
<p>
    This was done for 3 separate initialisations of the <code>ibm_brisbane</code> device over 2 separate dates, for a number of shots given by (\(2^{16}\), \(2^{15}\), \(2^{15}\)). The reduced number of shots was necessitated by limitations on the IBM device runtime available.
</p>
<p>
  A summary of this can be seen in <a href="#gate-table">Table 1</a>.
  </p>

<table id="gate-table" border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>Gate</th>
      <th>Circuit</th>
      <th>Input</th>
      <th>Expected Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Rx(θ)</td>
      <td>H → Rx(θ) → H → Measure</td>
      <td>\(|0\rangle\)</td>
      <td>\(|1\rangle\)</td>
    </tr>
    <tr>
      <td>Rzz(θ)</td>
      <td>H ⊗ H → Rzz(θ) → H ⊗ H → Measure</td>
      <td>\(|00\rangle\)</td>
      <td>\frac{1}{2} \left( |00\rangle + |01\rangle + |10\rangle + |11\rangle \right)\</td>
    </tr>
  </tbody>

</table>

  <h2>4. Results</h2>
  <p>
    The results of the <code>Rzz</code> gate investigation can be seen in <a href="#rzz_results">Figure 4</a>, where the error are the total length of the standard deviation across the three initialisations of the devices over the separate dates. 
    </p>
    <img src="images/rzz_err_by_angle_hardware_3reps.png" id="rzz_results" alt="Results of the Rzz angle investigation." width="800" />
    <figcaption id="rzz_results_caption">Figure 4: Results of the <code>Rzz</code> gate angle investigation, showing the relative error for each output channel. Different behaviour can be observed for each of the channels, but these is limited evidence of a relationship between the rotation angle and error rate for each channel.</figcaption>
    <p>
    It is clear from <a href="#rzz_results">Figure 4</a> that there is different behaviour of each of the output channels, with 01 and 11 systematically being detected more often than expected (showing leakage into these channels). Channel 00 is systematically detected less often than expected (showing leakage out of this channel) and the channel 10 shows evidence of both under and over detecting. Channels 01 and 11 also show no evidence of a relationship between the rotation angle and the error rate, the difference between the expected and measured counts being roughly stable across the 0 to \(\pi\) range. Channels 00 and 10 show potential relationships between the rotation angle and fidelity. Interestingly, the responses of these channels are roughly symmetrical around the x = 0.5\(\pi\) line. Channel 00 has a high error rate over the [0\(\pi\) to 0.6\(\pi\)] range, peaking near 0.2\(\pi\), and a low error rate over the [0.6\(\pi\) to 1.0\(\pi\)] range. On the other hand, channel 10 has a high error rate over the [0.6\(\pi\) to 1.0\(\pi\)] range, peaking near 0.8\(\pi\), and a low error rate over the [0.0\(\pi\) to 0.6\(\pi\)] range. However, the lack of evidence of a strong relationship between angle and fidelity in FIGURE ?? and the mirrored responses of the channels 00 and 10 mean the proposed error minimisation strategy through angle offsets is not likely to succeed, as any improvement made to the error rate of the 00 channel would be offset by deteriorations in the 10 channel error rate, and vice verse (while the error rates of channels 01 and 11 will be roughly unchanged).
  </p>
  
  <div class="note">
    <strong>Note:</strong> To do, a real statistical test (KS?) to check for strength of fidelity-angle relationship.
  </div>
  <img src="images/ibm_rx_error_5_16384_even_more.png", id="rx_results",alt="Results of the Rx angle investigation.", width="800" />
  <figcaption id="rx_results_caption">Figure 5: Results of the <code>Rx</code> gate angle investigation, showing the relative error against the rotation angle. A clear sinusodial relationship can be seen, with a period of 0.5\(\pi\) and amplitude of .</figcaption>
<p>
  The results of the <code>Rx</code> gate investigation can be seen in <a href="#rx_results">Figure 5</a>. This investigation shows clear evidence of a sinusodal dependence between the angle of rotation and the fidelity of the gate. This relationship has a period of 0.5\(\pi\), and the <code>Rx</code> gate has its highest error rates at rotation angles of [0\(\pi\), 0.5\(\pi\), 1.0\(\pi\)] and lowest error rates at rotation angles near [0.25\(\pi\), 0.75\(\pi\)]. The peak to trough difference is significant, varying between a rate of 0.45 and 0.04, a peak to trough drop of 90%. It is noted that this error rate far exceeds the reported <code>Rx</code> error value for <code>ibm_brisbane</code>, likely due to error mitigation techniques employed by the hardware which are not utilised here (the <code>Rx</code> gate investigation was conducted using an IBM simulator loaded with an <code>ibm_brisbane</code> noise model).  
  </p>

  <div class="note">
    <strong>Note:</strong> To do, check real numbers instead of eyeballing
  </div>

  <div class="note">
    <strong>Note:</strong> To do, plot little things (check titles, legends).
    Check double angle stuff
  </div>

  <p>
  While the <code>Rx</code> gate shows significant correlation between its fidelity and rotation angle, the error rate current QAOA implementations are dominated by the <code>Rzz</code> gate contribution. While this remains the case, improvements to the fidelity of the <code>Rx</code> gate would provide negligible (and undetectable) benefit to the quality of QAOA generated results. This inhibits investigations into whether QAOA results can be improved by leveraging <code>Rx</code> gates tuned to low error rotation angles. 
  </p>

  <h2>5. Conclusion</h2>
  <p>
    This preliminary work indicates that the <code>Rx</code> gate has a strong and sinusodal dependence between its fidelity and rotation angle, the error rate reducing by 90% from peak to trough. However, the overall contribution of this gate's error in the QAOA implementation is negligible. The error accumulations in QAOA are instead dominated by the effects of the <code>Rzz</code>. The work done here shows potential evidence of a relationship between rotation angle and the fidelity of the <code>Rzz</code> gate for the output channels of 00 and 10. However, evidence of this relationship is weak and these channels have mirrored error profiles, meaning there are not angles at which the overall error profile of the <code>Rzz</code> gate is minimised. Future work could investigate this behaviour on different hardware devices but, unless differing evidence is found, the lack of tunability of the <code>Rzz</code> gate and the negligable contribution of the <code>Rx</code> gate means the liklihood of minimising QAOA error by tuning circuits such that the gates operate at rotation angles corresponding to high fidelity performance is low.
  </p>

  <div class="note">
    <strong>Note:</strong> This is an ongoing investigation. Contributions and suggestions are welcome!
  </div>

  <!-- <h2>6. Code & Data</h2>
  <p>
    All code and data used for this project are available on GitHub:
    <a href="https://github.com/yourusername/quantum-angle-errors" target="_blank">github.com/yourusername/quantum-angle-errors</a>
  </p> -->

  <h2>References</h2>
<ol>
  <li id="ref_qaoa_foundation">E. Farhi, J. Goldstone. "A Quantum Approximate Optimization Algorithm," 2014. <a href="https://arxiv.org/abs/1411.4028" target="_blank">arXiv:1411.4028</a>.</li>

  <li id="ref_qaoa_rev">L. Zhou et al. "Quantum Approximate Optimization Algorithm: Performance, Mechanism, and Implementation on Near-Term Devices," 2019. <a href="https://arxiv.org/pdf/1812.01041" target="_blank">arXiv:1812.01041</a>.</li>

  <li id="ref_init_strats">X. Lee et al. "Parameters Fixing Strategy for Quantum Approximate Optimization Algorithm," 2021. <a href="https://arxiv.org/pdf/2108.05288" target="_blank">arXiv:2108.05288</a>.</li>

  <li id="ref_qaoa_transfer">R. Shaydulin et al. "Parameter Transfer for Quantum Approximate Optimization of Weighted MaxCut," 2023. <a href="https://arxiv.org/pdf/2201.11785" target="_blank">arXiv:2201.11785</a>.</li>

  <li id="ref_qiskit_general">IBM. QISKIT, accessed 2025. <a href="https://docs.quantum.ibm.com/guides" target="_blank">Docs</a>.</li>

  <li id="ref_qiskit_qaoa">IBM. QISKIT QAOA Documentation, accessed 2025. <a href="https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.qaoa_ansatz" target="_blank">Docs</a>.</li>

  <li id="ref_brisbane_specs">IBM. <code>ibm_brisbane</code> specifications, accessed 2025. <a href="https://quantum.ibm.com/services/resources?resourceType=current-instance&system=ibm_brisbane" target="_blank">Link</a>.</li>

  <li id="ref_default_options">IBM. Default hardware options, accessed 2025. <a href="https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/sampler-v2" target="_blank">Link</a>.</li>

</ol>
<!-- 
The error of Rzz gates has been studied in prior work  -->

</body>
</html>
