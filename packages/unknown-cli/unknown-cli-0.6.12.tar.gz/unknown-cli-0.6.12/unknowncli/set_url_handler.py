import pyuac, winreg

handler_name = "sn2"
key = f"{handler_name}\shell\open\command"

@pyuac.main_requires_admin
def main():
    try:
        h = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, handler_name)
        winreg.SetValueEx(h, "URL Protocol", 0, winreg.REG_SZ, "")
        h = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key)
        cmd = "unk.exe unreal asset \"%1\""
        winreg.SetValueEx(h, "", 0, winreg.REG_SZ, cmd)
    except PermissionError as e:
        print(f"Unable to set url handler for sn2://. Please open up your shell as Administrator (through shift-right click menu) and run this command again ({str(e)})")

if __name__ == "__main__":
    main()