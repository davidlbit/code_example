/*
University:             Hochschule Aalen, Germany
Module:                 Linux Security
Professor:              Prof. Dr. Marcus Gelderie
Exam type:              Project

Project members:
    Matnr: 62314        Nachname: Parham        Vorname: David Anthony
    Matnr: 73876        Nachname: Özyürek       Vorname: Eren
    Matnr: 54340        Nachname: Knies         Vorname: Adrian

*/

#include <fstream>
#include <vector>
#include <unistd.h>
#include <fcntl.h>
#include <grp.h>
#include <sys/prctl.h>

using namespace std;

const char* confData(string configname, int bytesize)
/*
This function opens passed files as parameter in read-only mode, if they exist.
Also a file descriptor is created in the process and added to a memory address.
The buffer value is then returned.
 */
{
    char* buffer = new char[bytesize * 2];
    const char* file = configname.c_str();
    int fd = open(file, O_RDONLY);
    if(fd == -1) {
        perror("r1");
        exit(EXIT_FAILURE);
    } else {
        printf("Reading file: <%s> successfully\n", file);
        read(fd, buffer, bytesize);
    }
    return buffer;
}

int main()
{
    const vector<string> CONFIG = {"program.config", "uid.config", "gid.config"};

    const char* PATH = confData(CONFIG[0], 32);
    const uid_t UID = atoi(confData(CONFIG[1], 8));
    const gid_t GID = atoi(confData(CONFIG[2], 12));

    printf("\nuid: %d, gid: %d, PATH: %s\n", UID, GID, PATH);

    //prctl(PR_SET_DUMPABLE, 0);
    printf("\npctl: %d\n", prctl(PR_GET_DUMPABLE));

    uid_t ruid, euid, suid;
    gid_t rgid, egid, sgid;

    setgroups(0, NULL);

    int getresgidExitCode = getresgid(&rgid, &egid, &sgid);
    if(getresgidExitCode != 0) {
        perror("Error (getresuid): the getresuid call failed!\n");
        exit(EXIT_FAILURE);
    } else {
        printf("rgid: %d, egid: %d, sgid: %d\n", rgid, egid, sgid);
    }

    int getresuidExitCode = getresuid(&ruid, &euid, &suid);
    if(getresuidExitCode != 0) {
        perror("Error (getresuid): the getresuid call failed!\n");
        exit(EXIT_FAILURE);
    } else {
        printf("\nruid: %d, euid: %d, suid: %d\n", ruid, euid, suid);
    }

    int setgidExitCode = setgid(GID);
    if(setgidExitCode != 0) {
        perror("\nError (Set-UID-Binary): The setgid call failed!\n\n");
        //exit(EXIT_FAILURE);
    } else {
        getresgidExitCode = getresgid(&rgid, &egid, &sgid);
        printf("rgid: %d, egid: %d, sgid: %d\n\n", rgid, egid, sgid);

    }

    int setuidExitCode = setuid(UID);
    if(setuidExitCode != 0) {
        perror("\nError (Set-UID-Binary): The setuid call failed!\n\n");
        exit(EXIT_FAILURE);
    } else {
        getresuidExitCode = getresuid(&ruid, &euid, &suid);
        printf("ruid: %d, euid: %d, suid: %d\n\n", ruid, euid, suid);

    }

    char* binaryArgs[2] = {(char *) PATH, NULL};

    const pid_t child_pid = fork();

    if(child_pid == 0) {
        /* This is done by the child process. */
        execv(binaryArgs[0], binaryArgs);

        /* If execv returns, it must have failed. */
        perror("\nUnknown command\n");
        exit(0);

    } else {
        /* This is run by the parent.  Wait for the child
        to terminate. */

    }

}