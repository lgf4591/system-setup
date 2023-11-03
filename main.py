import platform
import subprocess
import psutil


# print(platform.system())

shell_command_prefix_map = {
    "cmd.exe": "cmd.exe /c ",
    "powershell.exe": "powershell.exe -noprofile -c ",
    "pwsh.exe": "pwsh.exe -noprofile -c ",
    "pwsh": "pwsh -noprofile -c ",
    "sh.exe": "sh.exe -c ",
    "sh": "sh -c ",
    "bash.exe": "bash.exe -c ",
    "bash": "bash -c ",
    "zsh.exe": "zsh.exe -c ",
    "zsh": "zsh -c ",
    "fish.exe": "fish.exe -c ",
    "fish": "fish -c ",
    "nu.exe": "nu.exe -c ",
    "nu": "nu -c "
}

def is_empty(variable):
    if variable is None:
        return True
    if isinstance(variable, str) and variable == "":
        return True
    if isinstance(variable, (list, tuple, dict, set)) and len(variable) == 0:
        return True
    return False

class System(object):
    def __init__(self) -> None:
        pass
    
    @property
    def os(self):
        return platform.system().lower()
    @property
    def arch(self):
        return platform.machine().lower()
    @property
    def shell(self):
        current_process = psutil.Process()
        parent_process = current_process.parent()
        # print("Parent PID: ", parent_process.pid)
        # print("Parent Name: ", parent_process.name())
        return parent_process.name().lower()
    
    def run_command(self, command: str = "") -> int:
        command = shell_command_prefix_map[self.shell] + command
        print(f"当前系统为：{self.os}, 当前的shell为：{self.shell}, 当前执行的完整命令为：{command}")
        result = subprocess.run(command, capture_output=True, shell=True, text=True)  # https://blog.51cto.com/u_16175493/7917058
        if result.returncode == 0:
            print('命令执行成功！输出结果为：')
            print(result.stdout)
        else:
            print('命令执行不成功！错误结果为：')
            print(result.stderr)
        return result.returncode
    
    def run_script(self, path: str = "") -> int:
        try:
            print(f"当前系统为：{self.os}, 当前的shell为：{self.shell}, 当前执行脚本文件的完整路径为：{path}")
            if self.shell in ["powershell","powershell.exe","pwsh","pwsh.exe"]:
                result = subprocess.run([self.shell, '-noprofile', '-file', path], capture_output=True, text=True)
            elif self.shell == "cmd.exe":
                result = subprocess.run([self.shell, '/c', path], capture_output=True, text=True)
            else:
                result = subprocess.run([self.shell, path], capture_output=True, text=True) 
            if result.returncode == 0:
                print('脚本执行成功！输出结果为：')
                print(result.stdout)
            else:
                print('脚本执行不成功！错误结果为：')
                print(result.stderr)
            return result.returncode
        except Exception as e:
            print("脚本执行出错：", e)
    
    def setup(self):
        print(f"setup for {self.os} system now!!!")



print(f"current python version is : {platform.python_version()}")
system = System()
print(system.os)
print(system.arch)
print(system.shell)
system.setup()
# system.run_command("dir")
# system.run_command("ls")
# system.run_script("main.ps1")
system.run_script("main.bat")
# platform.freedesktop_os_release()["VERSION_ID"] # 22.04
# platform.freedesktop_os_release()["ID"] # ubuntu