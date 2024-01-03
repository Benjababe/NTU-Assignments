# CZ4031 Project 1

## Prerequisites to build the project

1. Follow steps 1-6 under prerequisites [here](https://code.visualstudio.com/docs/cpp/config-mingw#_prerequisites)
2. Ensure the `g++ --version` and `gdb --version` commands can be run from any directory.

Eg.
```
PS C:\Users\Benjababe\Desktop\CZ4031-Database-Principles\Project 1> g++ --version
g++.exe (Rev5, Built by MSYS2 project) 10.3.0
Copyright (C) 2020 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO 
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

PS C:\Users\Benjababe\Desktop\CZ4031-Database-Principles\Project 1>    
```

## Running as a Developer

Guide uses VSCode as the IDE, other IDEs will work but different setup methods may be required.

### With g++ & gdb
1. Ensure `g++` and `gdb` are accessible in any directory, `tasks.json` and `launch.json` assume they are.
2. Enter the `Run and Debug` tab on the left and run the `(Windows) Build & Launch` configuration.
3. Place a breakpoint somewhere in `main.cpp` and it should stop there.

### Running with CMake (Optional)

1. Install [CMake](https://cmake.org/download/) and its [VSCode extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cmake-tools)
2. Select a kit from the bottom left of the VSCode window.
3. Configure CMake with `Ctrl+Shift+P` and type `CMake: Configure` and select that option. The `out/build` folder should be created.
4. Build and launch using the `(Windows) CMake Build & Launch` configuration.
5. Place a breakpoint somewhere in `main.cpp` and it should stop there.

## Running as the Examiner

1. Run either `compile.bat` or `compile.sh` depending on your operating system, the `cz4031_project_1` executable should be created in the project root directory.
2. Run the executable and the initialisation and experiments should run.

