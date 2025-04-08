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
</head>
<body>

  <h1>Investigating Angle-Dependent Errors in Rzz and Rx Gates on IBM Quantum Hardware</h1>

  <p><strong>Author:</strong> Rafe Whitehead <br />
  <strong>Date:</strong> April 2025</p>

  <h2>1. Overview</h2>
  <p>
    This project works towards answering the larger question of: can we improve QAOA implementations by leveraging knowledge of expected gate angles and a gate angle dependent error profile to optimise QAOA circuits for specific problem types? Answering this requires two things: 
    1. Knowledge of the dependence on angle of the error rate of the relevant gates?
    2. Knowledge of how to tune the error profile of these gates for specific angles. 
    This project aims to answer the first question by investigating how the error rates of the <code>Rzz</code> and <code>Rx</code> quantum gates vary as a function of rotation angle on IBM's quantum hardware.
  </p>

  <h2>2. Background</h2>
  <p>
    Quantum Approximate Optimisation Algorithms (QAOA) [REF QAOA FOUNDATION] can be used to solve combinatorial optimisation problems and have emerged as a leading candidate for realising potential benefits of Noisy Intermediate Scale Quantum (NISQ) devices [REF QAOA REVIEW]. The QAOA is a hybrid algorithm, using a parameterised quantum evolution contained within a classical optimisation process to determine the quantum circuit parameters. This allows for shallow quantum circuits to be used, required given the limitations to circuit depth necessitated by the level of noise (or error) in current quantum devices. However, this algorithm suffers from barren plateaus and becoming trapped in local minima, making parameter determination difficult [REF QAOA REVIEW]. Currently, QAOA implementations ???? [REF]. Reducing the error rates on quantum circuits implementing QAOA algorithms would improve the quality of results, allow for deeper quantum circuits to be used, improving the viability of the QAOA algorithm.
</p>
<p>
    Each evaluation of the optimisation loop to determine QAOA circuit parameters has a cost associated with it, both directly (through energy usage) and indirectly (through time taken). Therefore, work has been done to 'guess' suitable initial parameters for the quantum circuit. The initial parameters can be determined using XXXX [REF JAP METHODS] or transfer learning [REF JP MORGAN]. If circuit gates have error rated dependent on their parameters, using the anticipated values of the parameters gained from these initialisation methods could allow for the reduction of circuit error by tuning the circuit to have reduced error at these anticipated angle values.

  </p>

  <h2>3. Methodology</h2>
  <p>
    For this investigation, freely-available IBM hardware will be used due to its accessibility and record of strong documentation online through the open-source library QISKIT. All devices offered under the free plan have identical specifications. The device <code>ibm_brisbane</code> was chosen arbitrarily.

    TALK SOMEWHERE LINKING QAOA PARAMS TO ROTATION ANGLE OF GATES.

</p>
<p>
    On IBM devices, QAOA algorithms are implemented using <code>Rx(θ)</code> and <code>Rzz(θ)</code> gates, as per [FIGURE QAOA ALGORITHM DECOMPOSED] [REF QISKIT DOCUMENTATION]. In this implementation, the error rate is dominated by the 2-gate Rzz gate [REF SOMETHING, IBM BRISBANE DATA?]. These gates were probed independently for the dependence of their fidelity on the their parameter (the angle of rotation). Due to the larger contribution to the error of the Rzz gate, this will be focussed on more (informal, tighten). However, the Rx investigation was more simple, and will be discussed first. The Rzz gate was investigated using the ibm_brisbane device, but the Rx gate was investigated using the IBM simulator in QISKIT, loaded with an ibm_brisbane noise model, to preserve the limited hardware running time available to the more important Rzz gate.
</p>
<p>
    The Rx gate was investigated using the circuit given in [FIGURE RX CIRCUIT]. This circuit was evaluated on the IBM simulator with ibm_brisbane a noise model using an input of [RX INPUT] [SHOT NUM] times, repeated over XXX times. When loaded with the input [RX INPUT], the antipated result is [RX OUTPUT]. By measuring the output of the circuit after each evaluation and comparing it to the anticipated result, the error rate of the gate can be determined.
</p>'
<p>
    The Rzz gate is also probed by comparing the results of an evaluated circuit to anticpated results. However, the Rzz (being a 2-qubit gate) requires a more complex circuit to probe, as seen in [RZZ FIGURE]. This circuit was evaluated on the ibm_brisbane hardware device using an input of [RX INPUT] [SHOT NUM] times, repeated over XXX times (other hardware options were left as default values, see [REF HARDWARE OPTIONS] for details). When loaded with the input [RX INPUT], the antipated result is [RX OUTPUT]. By measuring the output of the circuit after each evaluation and comparing it to the anticipated result, the error rate of the gate can be determined.
</p>
<p>
    A summary of this can be seen in [TABLE RX RZZ INPUTS OUTPUTS ETC]

    [HOW ERRORS WERE CALCULATED SECTION??]
    [PI??]
    [can probably condense this section, lots of repeats]

  </p>

  <h2>4. Results</h2>
  <p>
    Below is a plot showing the gate error as a function of rotation angle:
  </p>
  <img src="rzz_rx_error_plot.png" alt="Gate error vs angle" width="600" />

  <h2>5. Observations</h2>
  <ul>
    <li>For <code>Rx</code>, the error shows slight periodic variation, possibly due to hardware pulse shape artifacts.</li>
    <li><code>Rzz</code> gates exhibit higher error around specific rotation angles, possibly linked to cross-resonance implementation details.</li>
    <li>The error pattern is reproducible across runs but slightly varies between devices.</li>
  </ul>

  <h2>6. Conclusion</h2>
  <p>
    This preliminary study suggests that gate error can depend nontrivially on rotation angle. Further work could involve comparing results across more qubits, more devices, or running randomized benchmarking on parameterized gates.
  </p>

  <div class="note">
    <strong>Note:</strong> This is an ongoing investigation. Contributions and suggestions are welcome!
  </div>

  <h2>7. Code & Data</h2>
  <p>
    All code and data used for this project are available on GitHub:
    <a href="https://github.com/yourusername/quantum-angle-errors" target="_blank">github.com/yourusername/quantum-angle-errors</a>
  </p>

</body>
</html>
