#!/usr/bin/env python3
# THIS ASS DOT PY

import sys

INSTR_SIZE = 2
END = b"\xFF\xFF"
CODE_DETECTION_THRESHOLD = 4
ZERO_THRESHOLD = 4

# instructions are of format: [OPCODE REG ARG]
OPCODE_MAP = {
        0x00 : "CP",  # copies in REG bytes from [REG] of length ARG
        0x10 : "UNKN1",  # this must be true after: REG $ ARG = reg0
        0x20 : "MEM",
        0x30 : "LI",  # loads immediate ARG into REG
        0x40 : "LR",  # loads value from register ARG into REGa
        0x50 : "JZ",  # jumps to ARG if REG is 0
        0x60 : "JN",  # jumps to ARG if REG is not 0
        0x70 : "OP",  # prints value from REG of length ARG
        0x80 : "AD",  # add register ARG to REG
        0x90 : "SU",  # substracts register ARG from REG
        0xB0 : "ML",  # multiplies register REG with register ARG
        0xC0 : "SL",  # shift left
        0xD0 : "XR",  # XOR
        0xE0 : "UNKN3",
        0xF0 : "SR",  # shift right
}

def get_opcode(instr):
    return OPCODE_MAP[instr[-1] & 0xF0]

def get_register(instr):
    return instr[-1] & 0x0F

def get_arg(instr):
    return instr[0] & 0xFF

def is_code(section):
    cp_count = 0
    zero_count = 0
    for i in range(0, len(section), 2):
        if section[i] != 0x00 and section[i+1] == 0x00:
            cp_count += 1
        if section[i] == 0x00 and section[i+1] == 0x00:
            zero_count += 2
    if cp_count > CODE_DETECTION_THRESHOLD:
        return False # no way we find that many CP, this is .data
    if zero_count == len(section):
        return False

    return True  # probably code

def print_data(data_section):
    # might be more data vars than 1
    # this won't work in that case
    data = b""
    for i in range(0, len(data_section), 2):
        if data_section[i] == 0x00:
            continue
        data += chr(data_section[i]).encode()
    if len(data):
        print()
        print(b".data: " + data)


if len(sys.argv) != 2:
    print("Please pass the file to disassemble as argument :)")
    exit()

program = open(sys.argv[1], "rb").read()

for i in range(0, len(program), INSTR_SIZE):
    curr_instr = program[i:i+INSTR_SIZE]
    if curr_instr == END:
        print(f"{i//2}: ST")
        rem_data = program[i+INSTR_SIZE:]
        if is_code(rem_data):
            continue
        else:
            print_data(rem_data)
            break

    op = get_opcode(curr_instr)
    reg = get_register(curr_instr)
    arg = get_arg(curr_instr)

    if arg > ord('A') and arg < ord('z'):
        arg = "'" + chr(arg) + "'    # " + str(arg)

    print(f"{i//2}:", op, reg, arg)

