#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include <sys/types.h>

const char* getData(char datName[64]){
    const int fd1 = open(datName, O_RDONLY);
    printf("%d\n", fd1);
    static char buf[64];
    read(fd1, buf, 64);
    return buf;
}


int main() {
    
    const uid_t uid = atoi(getData("UID"));
    const uid_t gid = atoi(getData("GID"));
    const char* pfad = getData("Pfad");
    
    printf("uid: %d, gid: %d, pfad: %s\n", uid, gid, pfad);

    //chmod()
    //chown()

    uid_t ruid = 0;
    uid_t euid = 0;
    uid_t suid = 0;

    int returnvalue = getresuid(&ruid, &euid, &suid);
    printf("ruid: %d, euid: %d, suid: %d\n", ruid, euid, suid);    

    setresuid(gid, uid, 343);    
    //setegid()

    //getgid()
    returnvalue = getresuid(&ruid, &euid, &suid);
    printf("ruid: %d, euid: %d, suid: %d\n", ruid, euid, suid);

    
    //execve(pfad);
    

    char* argv2[2];
    argv2[0] = "/usr/bin/id";
    argv2[1] = NULL;

    pid_t child_pid;
    int child_status;

    child_pid = fork();
    if(child_pid == 0) {
        /* This is done by the child process. */

        //execv(argv2[0], argv2);

        /* If execv returns, it must have failed. */

        //printf("Unknown command\n");
        exit(0);
    }
    else {
        /* This is run by the parent.  Wait for the child
        to terminate. */

    }
}