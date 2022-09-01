#include <windows.h>
#include <iostream>

using namespace std;

void combine(char *destiny, const char *path1, const char *path2) {
	if (path1 == NULL || strlen(path1) == 0) {
		strcpy(destiny, path2);
	}
    else if (path2 == NULL || strlen(path2) == 0){
        strcpy(destiny, path1);
    }
	else {
		strcpy(destiny, path1);
		size_t idx = 0, sep = 0;
		size_t size1 = strlen(path1);
		while (idx < size1) {
			idx++;
			if (destiny[idx] == '/' || destiny[idx] == '\\') {
				sep = idx;
			}
		}
		// Trim destiny: delete from last sep to end.
        destiny[sep+1] = '\0';
        strcat(destiny, path2);
	}
}

int main(int argc, char** argv) {
	char path[MAX_PATH]; // Get Wrapper path
	GetModuleFileNameA(NULL, path, MAX_PATH);
    char lib[MAX_PATH] = "libraries\\ZStart.exe";
	char exe_path[MAX_PATH];
	combine(exe_path, path, lib); // Combine paths
	
	char file[sizeof(exe_path)]; // Add quotes
	strcpy(file, "\"");
	strcat(file, exe_path);
	strcat(file, "\"");
	
	system(file); // Run program
	return 0;
}