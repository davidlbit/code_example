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

#define _GNU_SOURCE 1
#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/stat.h>
#include <fcntl.h>
#define O_RDWR 02
#define O_CREAT 0100


//int setuid(uid_t uid);

//int setgid(gid_t gid);



using namespace std;
/*
int main()
{
    vector<string> config = {"program.config", "uid.config", "gid.config"};

    for (int i = 0; i < 3; i++)
    {
        // std::ifstream is RAII, i.e. no need to call close
        ifstream cFile (config[i]);
        if (cFile.is_open())
        {
            string line;
            while(getline(cFile, line))
            {
                line.erase(remove_if(line.begin(), line.end(), ::isspace),
                                    line.end());
                if(line[0] == '#' || line.empty())
                    continue;
                auto delimiterPos = line.find("=");
                auto name = line.substr(0, delimiterPos);
                auto value = line.substr(delimiterPos + 1);
                cout << name << " " << value << '\n';

                if(name == "url"){
                    char* argumente[5] = {"ls", "-l", "-R", "-a", NULL};
                    char* env[] = {"SHELL=/bin/zsh", "LOGNAME=davidlbit", "OSTYPE=L1NuX", NULL};
                    pid_t pid = fork();
                    switch (pid)
                    {
                        case -1:
                            perror("fork()");
                            return EXIT_FAILURE;
                        case 0:
                            execve("/bin/ls", argumente, env);
                            cout << "Works\n";
                            break;
                        default:
                            if (waitpid (pid, NULL, 0) != pid)
                            {
                                perror("waitpid()");
                                return EXIT_FAILURE;
                            }
                    }
                }
                //const char * c = value.c_str();

                //system(c);
            }

        } else
        {
            cerr << "Couldn't open config file for reading.\n";
        }
    }

}*/

const char* getData(string configName)
{
    static char buffer[64];
    int fd = open(configName.c_str(), O_RDONLY);
    if(fd == -1)
    {
        cout << "Can't read file: " << configName << "\n";
        exit(1);
    } else {
        cout << "Reading file: " << configName << " successfully\n";
        ssize_t read(int fd, void *buffer, size_t count[64]);
    }
    return buffer;
}


int main()
{
    vector<string> config = {"program.config", "uid.config", "gid.config"};

    const char* path = getData(config[0]);        //program.config"
    const uid_t uid = atoi(getData(config[1]));   //"uid.config"
    const uid_t gid = atoi(getData(config[2]));   //"gid.config"

    printf("uid: %d, gid: %d, path: %s\n", uid, gid, path);

    uid_t ruid = 0;
    uid_t euid = 0;
    uid_t suid = 0;


    int returnvalue = getresuid(&ruid, &euid, &suid);
    if(returnvalue != 0)
    {
        printf("Error, the getresuid call failed\n");
    } else
    {
            printf("ruid: %d, euid: %d, suid: %d\n", ruid, euid, suid);
    }
    //int setresuid(uid_t ruid, uid_t euid, uid_t suid);
    //On success, zero is returned.  On error, -1 is returned, and  errno  is set appropriately.
    int val = setresuid(ruid, ruid, ruid);
    if(val != 0)
    {
        printf("Error, the setresuid call failed\n");

    } else
    {
        cout << val << "\n";
        cout << getuid() << "\n";
        //setegid()

        //getgid()
        returnvalue = getresuid(&ruid, &euid, &suid);
        printf("ruid: %d, euid: %d, suid: %d\n", ruid, euid, suid);
    }


    char* binaryArgs[2] = {(char*)"/usr/bin/id", NULL};

    pid_t child_pid = fork();
    //int child_status;

    if(child_pid == 0)
    {
        /* This is done by the child process. */

        execv(binaryArgs[0], binaryArgs);

        /* If execv returns, it must have failed. */

        printf("Unknown command\n");
        exit(0);
    }
    else
    {
        /* This is run by the parent.  Wait for the child
        to terminate. */

    }

}