# GhanaCore-5 - Group 7

University of Ghana, CPEN 438 Advanced Computer Architecture, Project 2.

This repository contains complete Week 1 and Week 2 implementation artifacts for a fixed-width, five-stage RISC processor targeting a simplified mobile-money transaction-validation routine.

## Reproducibility assumption

The lecturer-assigned seed was not supplied with the implementation request. The repository therefore uses `GHANACORE_SEED = 7` as a deterministic **development seed derived from Group 7**. If the official seed is different, change only `GHANACORE_SEED` in `isa/isa.py` and `GHANACORE_SEED` in `isa/isa.h`; the instruction encoding and simulator remain unchanged.

## Architecture decisions

- 32-bit fixed-width instructions.
- 6-bit opcode, sixteen 32-bit registers (`r0`-`r15`), and 18-bit signed immediates for I/S/B formats.
- `r0` is hardwired to zero.
- Memory addresses and branch displacements are measured in 32-bit words.
- Five stages: IF, ID, EX, MEM, WB.
- No data forwarding or automatic data-hazard stalls. The baseline program inserts NOPs manually.
- Register-file writes occur before ID-stage reads in the same cycle.
- Branches resolve in EX. A taken branch flushes the two younger instructions in IF/ID and ID/EX.

## Repository layout

```text
GhanaCore-5-Group7/
|-- isa/
|   |-- isa.h                  C ISA constants and encoding helpers
|   `-- isa.py                 Python ISA constants and encoding helpers
|-- assembler/
|   `-- assembler.py           Two-pass assembler
|-- simulator/
|   |-- simulator.c            Five-stage golden reference simulator
|   |-- control_unit.h         Opcode-to-control mapping for C/Logisim
|   |-- control_unit.py        Matching executable Python mapping
|   `-- register_file.h        Dual-read, single-write register file
|-- programs/
|   |-- momo_routine.s         18 functional MoMo instructions
|   |-- momo_routine_nop_padded.s
|   |-- data_memory.hex        Accepted-transaction input
|   `-- data_memory_reject.hex Rejected-transaction input
|-- logisim/
|   `-- README.md              Hardware build contract and signal names
|-- docs/
|   |-- opcode_and_instruction_formats.md
|   |-- instruction_opcodes.csv
|   |-- momo_routine_machine_code.md
|   |-- pipeline_register_fields.csv
|   |-- pipeline_register_spec.md
|   |-- control_truth_table.md
|   |-- control_truth_table.csv
|   |-- paper_review_slides.md
|   `-- testing_verification_results.md
|-- tests/
|   |-- test_core.c
|   |-- test_assembler.py
|   |-- test_control_unit.py
|   `-- test_integration.py
|-- Makefile
`-- README.md
```

## Quick start

Requirements: a C11 compiler, `make`, and Python 3.10 or newer. No third-party packages are needed.

```sh
make all
make test
make run
```

`make all` builds the simulator and assembles both the 18-instruction functional routine and the explicitly NOP-padded baseline. `make run` executes the baseline with the accepted-transaction data and writes `build/momo_trace.csv`.

The unpadded 18-word file is the Week 1 architectural routine and machine-code deliverable. The 31-word NOP-padded file is the executable baseline for the Week 2 pipeline, which intentionally has no forwarding or automatic data-hazard interlock.

## Expected accepted-transaction result

The supplied data image starts with balance 1000, amount 150, fee 10, and transfer limit 500. The routine should finish with:

- `memory[0] = 840`
- `r8 = 1` (accepted)

The rejection image sets amount to 600. It should finish with:

- `memory[0] = 1000` (unchanged)
- `r8 = 0` (rejected)

## Git setup

```sh
git init
git add .
git commit -m "Implement GhanaCore-5 Week 1 and Week 2 deliverables"
```
