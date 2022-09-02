#include <windows.h>
#include <stdio.h>

void combine(char *destiny, const char *path1, const char *path2) {
	strcpy(destiny, "\"");
	if (path1 == NULL || strlen(path1) == 0) {
		strcat(destiny, path2);
	}
    else if (path2 == NULL || strlen(path2) == 0) {
        strcat(destiny, path1);
    }
	else {
		strcat(destiny, path1);
		size_t idx = 0, sep = 0;
		size_t size1 = strlen(path1);
		while (idx < size1) { // Get last separator
			idx++;
			if (destiny[idx] == '\\' || destiny[idx] == '/') {
				sep = idx;
			}
		}
		// Trim destiny to obtain directory.
        destiny[sep+1] = '\0';
        strcat(destiny, path2);
	}
	strcat(destiny, "\"");
}

int main(int argc, char** argv) {
	char path[MAX_PATH]; // Get Wrapper path
	GetModuleFileNameA(NULL, path, MAX_PATH);
    char lib[MAX_PATH] = "libraries\\ZStart.exe";
	char exe_path[MAX_PATH];
	combine(exe_path, path, lib); // Combine paths
	system(exe_path);
	return 0;
}