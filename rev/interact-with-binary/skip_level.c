#include <sys/ptrace.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
    long data = 0;
    int pid = atoi(argv[1]);
    printf("%d\n", pid);
    int *address = (int*)strtol(argv[2], NULL, 16);
    printf("%p\n", address);

    ptrace(PTRACE_ATTACH, pid, NULL, NULL);
    perror("attach");
    waitpid(pid, NULL, WUNTRACED);
    perror("wait");

    long long k;
    k = ptrace(PTRACE_PEEKDATA, pid, address, NULL);
    perror("read");
    /*data |= k; // are chestii extra*/
    ptrace(PTRACE_POKETEXT, pid, address, (void*)data);
    perror("write");
    ptrace(PTRACE_DETACH, pid, NULL, NULL);
    perror("detach");

    return 0;
}
