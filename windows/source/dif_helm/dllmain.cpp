#include "pch.h"
#include <windows.h>
#include <iostream>

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
        std::cout << "[INFO] DLL loaded into process." << std::endl;
        break;
    case DLL_THREAD_ATTACH:
        std::cout << "[INFO] DLL loaded into thread." << std::endl;
        break;
    case DLL_THREAD_DETACH:
        std::cout << "[INFO] DLL unloaded from thread." << std::endl;
        break;
    case DLL_PROCESS_DETACH:
        std::cout << "[INFO] DLL unloaded from process." << std::endl;
        break;
    }
    return TRUE;
}
