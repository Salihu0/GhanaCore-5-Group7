"""Shared GhanaCore-5 ISA constants and encoding helpers.

Instruction words are 32 bits. The opcode occupies bits 31:26.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


GHANACORE_SEED = 7  # Development seed derived from Group 7.
WORD_BITS = 32
OPCODE_BITS = 6
REGISTER_BITS = 4
IMMEDIATE_BITS = 18
REGISTER_COUNT = 1 << REGISTER_BITS

OPCODE_SHIFT = 26
RD_SHIFT = 22
RS1_SHIFT = 18
RS2_SHIFT = 14

OPCODE_MASK = (1 << OPCODE_BITS) - 1
REGISTER_MASK = (1 << REGISTER_BITS) - 1
IMMEDIATE_MASK = (1 << IMMEDIATE_BITS) - 1
R_RESERVED_MASK = (1 << RS2_SHIFT) - 1


class Opcode(IntEnum):
    NOP = 0x00
    ADD = 0x01
    SUB = 0x02
    AND = 0x03
    OR = 0x04
    XOR = 0x05
    SLT = 0x06
    ADDI = 0x08
    LW = 0x10
    SW = 0x11
    BEQ = 0x18
    BNE = 0x19


R_OPS = {Opcode.ADD, Opcode.SUB, Opcode.AND, Opcode.OR, Opcode.XOR, Opcode.SLT}
I_OPS = {Opcode.ADDI, Opcode.LW}
SB_OPS = {Opcode.SW, Opcode.BEQ, Opcode.BNE}


@dataclass(frozen=True)
class DecodedInstruction:
    opcode: Opcode
    rd: int = 0
    rs1: int = 0
    rs2: int = 0
    immediate: int = 0


def check_register(register: int) -> int:
    if not 0 <= register < REGISTER_COUNT:
        raise ValueError(f"register r{register} is outside r0-r{REGISTER_COUNT - 1}")
    return register


def check_immediate(immediate: int) -> int:
    minimum = -(1 << (IMMEDIATE_BITS - 1))
    maximum = (1 << (IMMEDIATE_BITS - 1)) - 1
    if not minimum <= immediate <= maximum:
        raise ValueError(f"immediate {immediate} is outside signed {IMMEDIATE_BITS}-bit range")
    return immediate & IMMEDIATE_MASK


def encode_r(opcode: Opcode, rd: int, rs1: int, rs2: int) -> int:
    if opcode not in R_OPS:
        raise ValueError(f"{opcode.name} is not an R-format opcode")
    return (
        (int(opcode) << OPCODE_SHIFT)
        | (check_register(rd) << RD_SHIFT)
        | (check_register(rs1) << RS1_SHIFT)
        | (check_register(rs2) << RS2_SHIFT)
    )


def encode_i(opcode: Opcode, rd: int, rs1: int, immediate: int) -> int:
    if opcode not in I_OPS:
        raise ValueError(f"{opcode.name} is not an I-format opcode")
    return (
        (int(opcode) << OPCODE_SHIFT)
        | (check_register(rd) << RD_SHIFT)
        | (check_register(rs1) << RS1_SHIFT)
        | check_immediate(immediate)
    )


def encode_sb(opcode: Opcode, rs1: int, rs2: int, immediate: int) -> int:
    if opcode not in SB_OPS:
        raise ValueError(f"{opcode.name} is not an S/B-format opcode")
    return (
        (int(opcode) << OPCODE_SHIFT)
        | (check_register(rs2) << RD_SHIFT)
        | (check_register(rs1) << RS1_SHIFT)
        | check_immediate(immediate)
    )


def encode_nop() -> int:
    return 0


def sign_extend_18(value: int) -> int:
    value &= IMMEDIATE_MASK
    sign_bit = 1 << (IMMEDIATE_BITS - 1)
    return value - (1 << IMMEDIATE_BITS) if value & sign_bit else value


def decode(word: int) -> DecodedInstruction:
    opcode = Opcode((word >> OPCODE_SHIFT) & OPCODE_MASK)
    if opcode == Opcode.NOP:
        return DecodedInstruction(opcode)
    if opcode in R_OPS:
        return DecodedInstruction(
            opcode=opcode,
            rd=(word >> RD_SHIFT) & REGISTER_MASK,
            rs1=(word >> RS1_SHIFT) & REGISTER_MASK,
            rs2=(word >> RS2_SHIFT) & REGISTER_MASK,
        )
    if opcode in I_OPS:
        return DecodedInstruction(
            opcode=opcode,
            rd=(word >> RD_SHIFT) & REGISTER_MASK,
            rs1=(word >> RS1_SHIFT) & REGISTER_MASK,
            immediate=sign_extend_18(word),
        )
    if opcode in SB_OPS:
        return DecodedInstruction(
            opcode=opcode,
            rs2=(word >> RD_SHIFT) & REGISTER_MASK,
            rs1=(word >> RS1_SHIFT) & REGISTER_MASK,
            immediate=sign_extend_18(word),
        )
    raise ValueError(f"unsupported opcode 0x{int(opcode):02X}")


MNEMONIC_TO_OPCODE = {opcode.name: opcode for opcode in Opcode}

