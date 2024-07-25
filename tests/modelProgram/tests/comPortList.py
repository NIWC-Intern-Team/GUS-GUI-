import serial.tools.list_ports
import time
import win32com.client

def list_serial_ports():
    ports = list(serial.tools.list_ports.comports())
    ports_info = {}
    for port in ports:
        ports_info[port.device] = port.description
    return ports_info

def print_ports(ports_info):
    for device, description in ports_info.items():
        print(f"Port: {device}, Description: {description}")

def list_usb_devices():
    wmi = win32com.client.GetObject("winmgmts:")
    for usb in wmi.InstancesOf("Win32_USBHub"):
        print(f"Device ID: {usb.DeviceID}")
        print(f"Description: {usb.Description}")
        print(f"Name: {usb.Name}")
        print("")

list_usb_devices()

print("Unplug the Xbox controller and press Enter...")
input()
ports_before = list_serial_ports()
print("Available Serial Ports before connecting the Xbox controller:")
print_ports(ports_before)

print("\nNow plug in the Xbox controller and press Enter...")
input()
ports_after = list_serial_ports()
print("Available Serial Ports after connecting the Xbox controller:")
print_ports(ports_after)

new_ports = {device: description for device, description in ports_after.items() if device not in ports_before}
if new_ports:
    print("\nNewly detected ports after connecting the Xbox controller:")
    print_ports(new_ports)
else:
    print("\nNo new ports detected. Ensure the Xbox controller is properly connected.")
