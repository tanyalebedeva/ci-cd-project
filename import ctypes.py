import ctypes
from ctypes import wintypes

# Структуры для WinAPI
class SYSTEM_INFO(ctypes.Structure):
    _fields_ = [
        ("wProcessorArchitecture", wintypes.WORD),
        ("wReserved", wintypes.WORD),
        ("dwPageSize", wintypes.DWORD),
        ("lpMinimumApplicationAddress", wintypes.LPVOID),
        ("lpMaximumApplicationAddress", wintypes.LPVOID),
        ("dwActiveProcessorMask", wintypes.DWORD),
        ("dwNumberOfProcessors", wintypes.DWORD),
        ("dwProcessorType", wintypes.DWORD),
        ("dwAllocationGranularity", wintypes.DWORD),
        ("wProcessorLevel", wintypes.WORD),
        ("wProcessorRevision", wintypes.WORD),
    ]

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

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", wintypes.DWORD),
        ("dwMemoryLoad", wintypes.DWORD),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

# Константы для атрибутов памяти
MEM_FREE = 0x10000
MEM_RESERVE = 0x2000
MEM_COMMIT = 0x1000

# Функции
def get_system_info():
    sys_info = SYSTEM_INFO()
    ctypes.windll.kernel32.GetSystemInfo(ctypes.byref(sys_info))
    return sys_info

def get_memory_status():
    mem_status = MEMORYSTATUSEX()
    mem_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem_status))
    return mem_status

def virtual_memory_map(start_address, end_address):
    mbi = MEMORY_BASIC_INFORMATION()
    address = start_address
    reserved_regions = 0
    total_reserved_size = 0
    print("Карта виртуальной памяти:")
    while address < end_address:
        result = ctypes.windll.kernel32.VirtualQuery(
            ctypes.c_void_p(address),
            ctypes.byref(mbi),
            ctypes.sizeof(mbi)
        )
        if not result:
            break
        if mbi.State == MEM_RESERVE:
            reserved_regions += 1
            total_reserved_size += mbi.RegionSize
        print(f"Адрес: {hex(mbi.BaseAddress)}, Размер: {mbi.RegionSize}, Атрибут защиты: {mbi.Protect}")
        address += mbi.RegionSize
    return reserved_regions, total_reserved_size

def reserve_memory(size):
    address = ctypes.windll.kernel32.VirtualAlloc(
        None,
        size,
        MEM_RESERVE,
        0x04  # PAGE_READWRITE
    )
    if address:
        print(f"Память зарезервирована по адресу: {hex(address)}")
    else:
        print("Ошибка при резервировании памяти")
    return address

# Основная программа
if __name__ == "__main__":
    print("Получение системной информации...")
    sys_info = get_system_info()
    print(f"Гранулярность размещения: {sys_info.dwAllocationGranularity} байт")

    print("\nПолучение информации о памяти...")
    mem_status = get_memory_status()
    print(f"Размер файла подкачки: {mem_status.ullTotalPageFile // (1024**2)} МБ")
    print(f"Суммарный объем доступной виртуальной памяти: {mem_status.ullAvailVirtual // (1024**2)} МБ")

    print("\nАнализ карты виртуальной памяти в диапазоне 1-2 ГБ...")
    reserved_regions, total_reserved_size = virtual_memory_map(0x40000000, 0x80000000)
    print(f"Количество зарезервированных регионов: {reserved_regions}")
    print(f"Общий объем зарезервированных регионов: {total_reserved_size // 1024} КБ")

    print("\nРезервирование памяти...")
    reserve_memory(1024 * 1024)  # Резервирование 1 МБ

    print("\nПовторный анализ карты виртуальной памяти...")
    reserved_regions, total_reserved_size = virtual_memory_map(0x40000000, 0x80000000)
    print(f"Количество зарезервированных регионов: {reserved_regions}")
    print(f"Общий объем зарезервированных регионов: {total_reserved_size // 1024} КБ")
