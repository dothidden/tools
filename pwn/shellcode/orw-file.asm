/*
	-= ORW (Open-Read-Write) file =-
	> Opens "flag.txt"
	> Reads it and writes content (0x40 bytes) to stdout
	> Change 0x40 bytes if you want to read more
	> Gracefully exits
	> Change flag string if you want to open/write another file
	> GAS syntax
*/
.global _start
.intel_syntax noprefix
_start:
open:
	mov rax, 0x2
	lea rdi, [rip+flag]
	xor rsi, rsi
	xor rdx, rdx
	syscall

read:
	mov rdi, rax
	xor rax, rax
	mov rsi, rsp
	mov rdx, 0x40
	syscall

write:
	mov rax, 0x1
	mov rdi, 0x1
	syscall

exit:
	mov rax, 0x3c
	xor rdi, rdi
	syscall


flag:
	.string "flag.txt"
