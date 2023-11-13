import subprocess

operations = [
    "remap",
    "permutate",
    "forxor",
    "remap",
    "permutate",
    "forxor",
    "remap",
    "permutate",
    "forxor",
    "remap",
    "permutate",
    "forxor",
    "remap",
    "permutate",
    "forxor",
    "remap",
    "permutate",
    "forxor",
    "remap",
    "permutate",
    "forxor",
    "remap",
    "permutate",
    "forxor",
    "remap",
    "permutate",
    "forxor",
    "remap",
    "permutate",
]

flagenc = "c55e8b7b42cf7a359a9227bc14822a927ac5c9817dba99083" \
          "27f0a879f683edac8bddc70c9bd9b75cfa9c887d91d3fb7f4" \
          "05191f510c5377a55f4a8b6c6584e03ecc5c7d1031baa9102" \
          "4832c72cc7720"

def c_string(s) -> str:
    ret: str = ""
    for i in range(0, 32, 2):
        ret += f'0x{s[i: i + 2]}, '
    return ret

def reverse_op(block, operation) -> str:
    # add operation and target string to the header
    with open("./solve.h", "w") as f:
        f.write(f"#include <stdint.h>\n\n")
        f.write(f"#define OPERATION {operation}\n")
        f.write(f"const uint8_t target[16] = {{{c_string(block)}}};")

    # compile
    subprocess.run(['clang-14', '-emit-llvm', '-c', \
                    '-g', '-O0', './solve.c'], stdout=subprocess.DEVNULL)
    # run with klee
    subprocess.run(['klee', '-exit-on-error-type=Assert', './solve.bc'], stderr=subprocess.DEVNULL)
    # run the test again and get the output
    result = subprocess.run(['ktest-tool', './klee-last/test000001.ktest'], \
                            capture_output=True)
    # select hex string
    hex_string = result.stdout.split(b'\n')[6].split(b': ')[-1][2:]
    return hex_string.decode()

def reverse_block(block):
    # take each operation in reverse
    for op in operations[::-1]:
        # reverse the operation for this block
        block = reverse_op(block, op)
        print('.', end='', flush=True)
    print(flush=True)
    return block

def solve():
    flag = ""
    # iterate blocks
    for i in range(0, 160, 32):
        block = flagenc[i:i + 32]
        flag += reverse_block(block)
        print(f"block {i} done", flush=True)
    print(bytes.fromhex(flag))

if __name__ == '__main__':
    solve()
    subprocess.run(['rm', '-rf', 'klee*'])
    subprocess.run(['rm', '-rf', 'solve.bc'])
