# Logisim construction handoff

Build the circuit in this directory as `GhanaCore5.circ` using the exact signal names and packed widths in `docs/pipeline_register_spec.md`. That document specifies the four pipeline-register subcircuits, top-level blocks, reset/enable behavior, branch flush, and observable probes. `docs/control_truth_table.md` gives the control ROM word packing.

Recommended build order:

1. `RegisterFile16x32_2R1W`: two combinational read ports, one clocked write port, reset-to-zero, hardwired `r0`.
2. `ControlUnit`: 6-bit opcode to 11-bit control word.
3. `REG_IF_ID_65`, `REG_ID_EX_157`, `REG_EX_MEM_145`, `REG_MEM_WB_77`.
4. `ALU32`, PC/branch adder, instruction ROM, and data RAM.
5. Top-level `GhanaCore5` and the named probes.

Load `programs/momo_routine_nop_padded.hex` into instruction ROM and `programs/data_memory.hex` into data RAM. For the accepted test, the final expected state is `memory[0]=840`, `r8=1`. The generated software oracle is `build/momo_trace.csv` after `make run`.

This repository deliberately provides an unambiguous construction spec rather than fabricating a binary `.circ` file for an unverified Logisim version. Record the Logisim/Logisim-evolution version in the report when the Hardware Lead creates the circuit.
