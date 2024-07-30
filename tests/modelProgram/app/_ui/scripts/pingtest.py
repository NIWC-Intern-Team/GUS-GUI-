import subprocess
ip =  "192.168.53.100"
result = subprocess.run(["dir"], shell=True, capture_output=True, text=True)
result = subprocess.run(['ping', ip], capture_output=True, text=True, check=True)

print(result.stdout)
