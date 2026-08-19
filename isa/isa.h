#ifndef GHANACORE_ISA_H
#define GHANACORE_ISA_H

#include <stdint.h>

#define GHANACORE_SEED 7u
#define GHANACORE_REGISTER_COUNT 16u
#define GHANACORE_OPCODE_SHIFT 26u
#define GHANACORE_RD_SHIFT 22u
#define GHANACORE_RS1_SHIFT 18u
#define GHANACORE_RS2_SHIFT 14u
#define GHANACORE_OPCODE_MASK 0x3Fu
#define GHANACORE_REGISTER_MASK 0x0Fu
#define GHANACORE_IMMEDIATE_MASK 0x3FFFFu

typedef enum {
    OP_NOP = 0x00,
    OP_ADD = 0x01,
    OP_SUB = 0x02,
    OP_AND = 0x03,
    OP_OR = 0x04,
    OP_XOR = 0x05,
    OP_SLT = 0x06,
    OP_ADDI = 0x08,
    OP_LW = 0x10,
    OP_SW = 0x11,
    OP_BEQ = 0x18,
    OP_BNE = 0x19
} GhanaOpcode;

typedef struct {
    GhanaOpcode opcode;
    uint8_t rd;
    uint8_t rs1;
    uint8_t rs2;
    int32_t immediate;
} GhanaDecoded;

static inline int32_t ghana_sign_extend_18(uint32_t value) {
    value &= GHANACORE_IMMEDIATE_MASK;
    if ((value & 0x20000u) != 0u) {
        return (int32_t)(value | 0xFFFC0000u);
    }
    return (int32_t)value;
}

static inline uint32_t ghana_encode_r(GhanaOpcode opcode, uint8_t rd, uint8_t rs1, uint8_t rs2) {
    return ((uint32_t)opcode << GHANACORE_OPCODE_SHIFT)
        | (((uint32_t)rd & GHANACORE_REGISTER_MASK) << GHANACORE_RD_SHIFT)
        | (((uint32_t)rs1 & GHANACORE_REGISTER_MASK) << GHANACORE_RS1_SHIFT)
        | (((uint32_t)rs2 & GHANACORE_REGISTER_MASK) << GHANACORE_RS2_SHIFT);
}

static inline uint32_t ghana_encode_i(GhanaOpcode opcode, uint8_t rd, uint8_t rs1, int32_t immediate) {
    return ((uint32_t)opcode << GHANACORE_OPCODE_SHIFT)
        | (((uint32_t)rd & GHANACORE_REGISTER_MASK) << GHANACORE_RD_SHIFT)
        | (((uint32_t)rs1 & GHANACORE_REGISTER_MASK) << GHANACORE_RS1_SHIFT)
        | ((uint32_t)immediate & GHANACORE_IMMEDIATE_MASK);
}

static inline uint32_t ghana_encode_sb(GhanaOpcode opcode, uint8_t rs1, uint8_t rs2, int32_t immediate) {
    return ((uint32_t)opcode << GHANACORE_OPCODE_SHIFT)
        | (((uint32_t)rs2 & GHANACORE_REGISTER_MASK) << GHANACORE_RD_SHIFT)
        | (((uint32_t)rs1 & GHANACORE_REGISTER_MASK) << GHANACORE_RS1_SHIFT)
        | ((uint32_t)immediate & GHANACORE_IMMEDIATE_MASK);
}

static inline GhanaDecoded ghana_decode(uint32_t word) {
    GhanaDecoded decoded;
    decoded.opcode = (GhanaOpcode)((word >> GHANACORE_OPCODE_SHIFT) & GHANACORE_OPCODE_MASK);
    decoded.rd = (uint8_t)((word >> GHANACORE_RD_SHIFT) & GHANACORE_REGISTER_MASK);
    decoded.rs1 = (uint8_t)((word >> GHANACORE_RS1_SHIFT) & GHANACORE_REGISTER_MASK);
    decoded.rs2 = (uint8_t)((word >> GHANACORE_RS2_SHIFT) & GHANACORE_REGISTER_MASK);
    decoded.immediate = ghana_sign_extend_18(word);

    if (decoded.opcode == OP_SW || decoded.opcode == OP_BEQ || decoded.opcode == OP_BNE) {
        decoded.rs2 = decoded.rd;
        decoded.rd = 0u;
    }
    if (decoded.opcode == OP_ADDI || decoded.opcode == OP_LW) {
        decoded.rs2 = 0u;
    }
    if (decoded.opcode == OP_NOP) {
        decoded.rd = decoded.rs1 = decoded.rs2 = 0u;
        decoded.immediate = 0;
    }
    return decoded;
}

#endif
