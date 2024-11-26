import psutil
import ctypes
from ctypes import wintypes
import sys

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", wintypes.LPVOID),
        ("AllocationBase", wintypes.LPVOID),
        ("AllocationProtect", wintypes.DWORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
    ]

VirtualQuery = ctypes.windll.kernel32.VirtualQuery
VirtualQuery.argtypes = [wintypes.LPCVOID, ctypes.POINTER(MEMORY_BASIC_INFORMATION), ctypes.c_size_t]
VirtualQuery.restype = ctypes.c_size_t

def print_memory_status():
    memory_info = psutil.virtual_memory()
    print(f"Granularity of memory allocation: {memory_info.total} bytes")
    print(f"Page file size: {memory_info.total / 1024} KB")
    print(f"Total reserved regions: {memory_info.available / 1024} KB")

def print_virtual_memory_map(start_address, end_address):
    mbi = MEMORY_BASIC_INFORMATION()
    address = start_address

    while address < end_address:
        ret = VirtualQuery(ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi))
        if ret == 0:
            break

        if mbi.State == 0x2000:  # MEM_RESERVE
            print(f"Region Address: {mbi.BaseAddress} Size: {mbi.RegionSize / 1024} KB Protection Attributes: {mbi.AllocationProtect}")

        address += mbi.RegionSize

def main():
    print_memory_status()

    start_address = 0x40000000  # 1 Гб
    end_address = 0x80000000    # 2 Гб
    print_virtual_memory_map(start_address, end_address)

if __name__ == "__main__":
    if sys.platform != "win32":
        print("Windows.")
    else:
        main()
