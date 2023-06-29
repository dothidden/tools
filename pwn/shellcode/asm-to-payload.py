with open("message", "r") as f:
    lines = f.readlines()
    bytes = ''

    # print(lines)

    for l in lines:
        if len(l) == 0: continue
        if l[0].isdigit(): continue

        if ':' in l:
            instr = l[l.index(':') + 2:]
            instr = instr[:instr.index('\t')]

            instrs = instr.split()
            instrs = ''.join([fr'\x{x.strip()}' for x in instrs])
            bytes += instrs.strip()
    print(fr"`{bytes}`")
