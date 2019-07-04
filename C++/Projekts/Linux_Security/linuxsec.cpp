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
        perror("r1\n");
        exit(EXIT_FAILURE);
    } else {
        read(fd, buffer, bytesize);
    }
    return buffer;
}

int main()
{
    const vector<string> CONFIG = {"program.config", "uid.config", "gid.config"};

    // the second parameters refer to the bytesize of the read function
    const char* PATH = confData(CONFIG[0], 32);
    const uid_t UID = atoi(confData(CONFIG[1], 8));
    const gid_t GID = atoi(confData(CONFIG[2], 12));

    uid_t ruid, euid, suid;
    gid_t rgid, egid, sgid;

    setgroups(0, NULL);

    int getresgidExitCode = getresgid(&rgid, &egid, &sgid);
    if(getresgidExitCode != 0) {
        perror("Error (getresgid): the getresgid call failed!\n");
        exit(EXIT_FAILURE);
    }

    int getresuidExitCode = getresuid(&ruid, &euid, &suid);
    if(getresuidExitCode != 0) {
        perror("Error (getresuid): the getresuid call failed!\n");
        exit(EXIT_FAILURE);
    }

    int setgidExitCode = setgid(GID);
    if(setgidExitCode != 0) {
        perror("Error (Capability-GID): Check if the cap_setgid capability has been assigned.\n");
        exit(EXIT_FAILURE);
    } else {
        getresgidExitCode = getresgid(&rgid, &egid, &sgid);
    }

    int setuidExitCode = setuid(UID);
    if(setuidExitCode != 0) {
        perror("Error (Capability-UID): Check if the cap_setuid capability has been assigned.\n");
        exit(EXIT_FAILURE);
    } else {
        getresuidExitCode = getresuid(&ruid, &euid, &suid);
    }

    char* binaryArgs[2] = {(char *) PATH, NULL};

    const pid_t child_pid = fork();

    if(child_pid == 0) {
        //This is done by the child process.
        execv(binaryArgs[0], binaryArgs);

        //If execv returns, it must have failed.
        perror("Unknown command\n");
        exit(EXIT_SUCCESS);

    } else {
        //This is run by the parent.

    }
}