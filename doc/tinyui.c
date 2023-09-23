/**
 * Windows build:
 *      "C:\Program Files\JetBrains\CLion_2023.1.4\bin\cmake\win\x64\bin\cmake.exe" --build C:\Users\xxx\CLionProjects\tinyui\cmake-build-debug --target tinyui -j 3
 *
 * MacOS and Linux build:
 *      gcc -o tinyui tinyui.c
 * */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[]) {
    if (argc <= 0) return -1;
    const char* this_file = argv[0];
//    printf("%s\n", this_file);

    int pos;
    const char* ptr = strrchr(this_file, '/');
    if (!ptr) {
        ptr = strrchr(this_file, '\\');
        if (!ptr) return -2;
    }
    pos = ptr - this_file;
    ++ ptr;

    char this_path[512];
    memcpy(this_path, this_file, pos);
    this_path[pos] = '\0';

    char pyname[128];
    const char* ptr2 = strrchr(ptr, '-');// -mac or -win.exe
    if (!ptr2) {
        ptr2 = strrchr(ptr, '.');// .exe
    }
    if (ptr2) {
        pos = ptr2 - ptr;
        memcpy(pyname, ptr, pos);
        pyname[pos] = '\0';
    } else {
        strcpy(pyname, ptr);
    }

    char cmd[512];
    sprintf(cmd, "python %s/%s.py &", this_path, pyname);
//    printf("%s\n", cmd);

    system(cmd);
    return 0;
}
