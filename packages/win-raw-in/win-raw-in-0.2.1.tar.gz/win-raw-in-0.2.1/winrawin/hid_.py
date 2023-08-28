import ctypes

# Define constants and structures for Windows API calls
HIDP_STATUS_SUCCESS = 0x110000
MAX_STRING_LENGTH = 126
DIGCF_PRESENT = 0x00000002
DIGCF_DEVICEINTERFACE = 0x00000010



class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8)
    ]


class SP_DEVICE_INTERFACE_DATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("InterfaceClassGuid", GUID),
        ("Flags", ctypes.c_ulong),
        ("Reserved", ctypes.POINTER(ctypes.c_ulong))
    ]


class SP_DEVINFO_DATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("ClassGuid", GUID),
        ("DevInst", ctypes.c_ulong),
        ("Reserved", ctypes.POINTER(ctypes.c_ulong))
    ]


class SP_DEVICE_INTERFACE_DETAIL_DATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("DevicePath", ctypes.c_char * 1)
    ]


input_id = "\\\\?\\HID#VID_046D&PID_C336&MI_00#8&178e0225&0&0000#{884b96c3-56ef-11d1-bc8c-00a0c91405dd}"

# Load the required DLLs
setupapi = ctypes.windll.LoadLibrary("setupapi")
hid = ctypes.windll.LoadLibrary("hid")

# Get the HID GUID
hid_guid = GUID()
hid.HidD_GetHidGuid(ctypes.byref(hid_guid))

# Get a handle to a device information set for all HID devices
# devinfo = setupapi.SetupDiGetClassDevsA(ctypes.byref(hid_guid), None, None, DIGCF_PRESENT | DIGCF_DEVICEINTERFACE)
devinfo = setupapi.SetupDiGetClassDevsA(ctypes.byref(hid_guid), None, None, DIGCF_PRESENT | DIGCF_DEVICEINTERFACE)

# Enumerate the device interfaces in the device information set
index = 0
device_found = False
device_interface_data = SP_DEVICE_INTERFACE_DATA()
device_interface_data.cbSize = ctypes.sizeof(device_interface_data)
while setupapi.SetupDiEnumDeviceInterfaces(devinfo, None, ctypes.byref(hid_guid), index, ctypes.byref(device_interface_data)):
    index += 1
    print("Device")

    # Get the device path for this device interface
    detail_data_size = ctypes.c_ulong()
    setupapi.SetupDiGetDeviceInterfaceDetailA(devinfo, ctypes.byref(device_interface_data), None, 0, ctypes.byref(detail_data_size), None)
    detail_data_buffer = ctypes.create_string_buffer(detail_data_size.value)
    detail_data = ctypes.cast(detail_data_buffer, ctypes.POINTER(SP_DEVICE_INTERFACE_DETAIL_DATA)).contents
    detail_data.cbSize = 5  # sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA)
    setupapi.SetupDiGetDeviceInterfaceDetailA(devinfo, ctypes.byref(device_interface_data), ctypes.byref(detail_data), detail_data_size, None, None)

    # Get the device id for this device interface
    device_id_buffer = ctypes.create_string_buffer(MAX_STRING_LENGTH)
    hid.HidD_GetHidGuid(ctypes.byref(device_id_buffer))

    # Check if the device id matches the input id
    device_id = device_id_buffer.value.decode("utf-8")
    if device_id == input_id:
        print(device_id)
        device_found = True
        break
else:
    raise ctypes.WinError(ctypes.GetLastError())

# If the device is found, get its manufacturer and product name
if device_found:
    # Open the device with read access
    device_handle = setupapi.CreateFileA(detail_data.DevicePath, 0x80000000, 0, None, 3, 0, None)

    # Get the manufacturer name
    manufacturer_buffer = ctypes.create_string_buffer(MAX_STRING_LENGTH)
    hid.HidD_GetManufacturerString(device_handle, manufacturer_buffer, MAX_STRING_LENGTH)

    # Get the product name
    product_buffer = ctypes.create_string_buffer(MAX_STRING_LENGTH)
    hid.HidD_GetProductString(device_handle, product_buffer, MAX_STRING_LENGTH)

    # Close the device handle
    setupapi.CloseHandle(device_handle)

    # Print the manufacturer and product name
    manufacturer_name = manufacturer_buffer.value.decode("utf-16")
    product_name = product_buffer.value.decode("utf-16")

    print(f"Manufacturer: {manufacturer_name}")
    print(f"Product: {product_name}")
else:
    print(f"No device with id {input_id} found")

# Destroy the device information set
setupapi.SetupDiDestroyDeviceInfoList(devinfo)