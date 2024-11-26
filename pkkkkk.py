import ctypes
from ctypes import wintypes

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wintypes.DWORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
    ]

MEM_RESERVE = 0x2000
MEM_COMMIT = 0x1000
PAGE_READWRITE = 0x04

def reserve_virtual_memory(size):
    return ctypes.windll.kernel32.VirtualAlloc(None, size, MEM_RESERVE, PAGE_READWRITE)

def commit_virtual_memory(base_address, size):
    return ctypes.windll.kernel32.VirtualAlloc(base_address, size, MEM_COMMIT, PAGE_READWRITE)

if __name__ == "__main__":
    reserved_address = reserve_virtual_memory(1024 * 1024)
    if reserved_address:
        print(f"Память зарезервирована: {hex(reserved_address)} (Размер: 1 МБ)")
        committed_address = commit_virtual_memory(reserved_address, 512 * 1024)
        if committed_address:
            print(f"Физическая память выделена: {hex(committed_address)} (Размер: 512 КБ)")

