import subprocess
import os
import sys
import webbrowser
import time

MARKER_FILE = ".setup_done"

def run_command(command, shell=False, capture_output=False):
    """Utility to run shell commands."""
    try:
        # result = subprocess.run(...)
        # On Windows, using shell=True is often necessary for docker commands if not in PATH properly, 
        # but here we'll assume it is.
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            capture_output=capture_output,
            text=True
        )
        return (result.stdout.strip() if capture_output else True)
    except subprocess.CalledProcessError as e:
        if not capture_output:
            print(f"\n[!] Error executing command: {e}")
        return False
    except FileNotFoundError:
        print(f"\n[!] Error: 'docker' command not found. Please install Docker and Docker Compose.")
        return False

def check_project_active():
    """Checks if any project containers are already running."""
    # Using 'docker compose ps --status running' to see if anything is up
    output = run_command("docker compose ps --status running --format json", shell=True, capture_output=True)
    if output and output != "[]" and output != "":
        return True
    return False

def check_setup_done():
    """Checks if the setup marker file exists."""
    return os.path.exists(MARKER_FILE)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def reconfigure_docker_compose(is_simple):
    """Dynamically updates network settings in docker-compose.yaml."""
    print(f"[*] Reconfiguring docker-compose.yaml for {'Simple' if is_simple else 'Complete'} mode...")
    
    try:
        with open("docker-compose.yaml", "r") as f:
            content = f.read()
        
        # Simple mode: Enable network_mode: host, Comment out ports
        if is_simple:
            content = content.replace("# network_mode: host", "network_mode: host")
            # If it's already active, we don't want to double comment or comment out existing uncommented ports 
            # if we are already in simple mode. 
            # But let's assume the user starts from a known state or we just make it idempotent.
            if '    ports:' in content and '    # ports:' not in content:
                 content = content.replace("    ports:", "    # ports:")
                 content = content.replace('      - "7681:7681"', '      # - "7681:7681"')
        else:
            # Complete mode: Comment out network_mode: host, Enable ports
            content = content.replace("    network_mode: host", "    # network_mode: host")
            content = content.replace("    # ports:", "    ports:")
            content = content.replace('      # - "7681:7681"', '      - "7681:7681"')
            
        with open("docker-compose.yaml", "w") as f:
            f.write(content)
        print("[+] docker-compose.yaml updated successfully.")
        return True
    except Exception as e:
        print(f"[!] Error reconfiguring docker-compose.yaml: {e}")
        return False

def main_menu():
    clear_screen()
    print("========================================")
    print("   Red Team Docker - AI Pentest Lab     ")
    print("========================================")
    print("\nSelect an installation option:")
    print("1. Simple Install")
    print("   - Build and start only 'hexstrike-ai' (Gemini Lab)")
    print("   - Automatically connect to the container terminal")
    print("\n2. Complete Install")
    print("   - Deploy all services (Database, GUI, Files, Terminal)")
    print("   - Open the Web Dashboard in your browser")
    print("\nQ. Quit")
    print("\n----------------------------------------")
    
    choice = input("\nYour choice: ").strip().lower()
    return choice

def simple_install():
    print("\n[*] Starting Simple Install...")
    reconfigure_docker_compose(True)
    print("[*] Building and starting hexstrike-ai container...")
    if run_command("docker compose up -d --build hexstrike-ai", shell=True):
        with open(MARKER_FILE, "w") as f:
            f.write(f"Setup completed at {time.ctime()}\n")
        
        print("[+] Success! Connecting to the lab terminal...")
        time.sleep(2)
        # Replacing the current process with docker exec
        if os.name == 'nt':
            # On Windows, we use subprocess to keep it interactive
            subprocess.run("docker exec -it hexstrike_gemini_lab /bin/bash", shell=True)
        else:
            os.execvp("docker", ["docker", "exec", "-it", "hexstrike_gemini_lab", "/bin/bash"])
    else:
        print("\n[!] Setup failed. Please check the logs above.")
        input("\nPress Enter to return to menu...")

def complete_install():
    print("\n[*] Starting Complete Install...")
    reconfigure_docker_compose(False)
    print("[*] Deploying all docker-compose services...")
    if run_command("docker compose up -d --build", shell=True):
        with open(MARKER_FILE, "w") as f:
            f.write(f"Setup completed at {time.ctime()}\n")
        
        print("[+] Success! All services are up.")
        
        # --- NEW TTYD INTEGRATION ---
        print("[*] Configuring TTYD terminal on hexstrike-ai container...")
        # Downloading official ttyd x86_64 binary as it is not in default repos
        run_command("docker exec hexstrike_gemini_lab curl -fsSL https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 -o /usr/local/bin/ttyd", shell=True)
        run_command("docker exec hexstrike_gemini_lab chmod +x /usr/local/bin/ttyd", shell=True)
        
        # Start TTYD in detached mode on port 7681 (exposed via docker-compose ports)
        print("[+] Starting TTYD terminal on http://localhost:7681...")
        # Adding --writable to ensure terminal accepts input correctly
        run_command("docker exec -d hexstrike_gemini_lab ttyd --writable -p 7681 /bin/bash", shell=True)
        # ----------------------------

        print("[*] Opening frontend dashboard...")

        time.sleep(5)
        
        frontend_path = os.path.abspath("frontend/index.html")
        if os.path.exists(frontend_path):
            # Using webbrowser to open the local file
            webbrowser.open(f"file://{frontend_path}")
        else:
            print(f"[!] Warning: Frontend file not found at {frontend_path}")
        
        print("\n[!] Complete setup finished. You can now access the GUI at http://localhost:6080")
        input("\nPress Enter to exit...")
    else:
        print("\n[!] Setup failed. Please check the logs above.")
        input("\nPress Enter to return to menu...")

def reset_setup():
    print("\n[!] WARNING: This will stop all containers and remove the setup marker.")
    confirm = input("[?] Are you sure you want to reset the setup? (y/N): ").lower()
    if confirm == 'y':
        print("[*] Stopping containers...")
        run_command("docker compose down", shell=True)
        if os.path.exists(MARKER_FILE):
            os.remove(MARKER_FILE)
        print("[+] Setup reset successfully.")
        time.sleep(1)
        return True
    return False

def main():
    while True:
        # Check if project is already active or setup was done
        active = check_project_active()
        setup_done = check_setup_done()

        if active and setup_done:
            clear_screen()
            print("========================================")
            print("   Red Team Docker - AI Pentest Lab     ")
            print("========================================")
            print("\n[*] Project is already active and setup was completed previously.")
            print("\nOptions:")
            print("1. Enter Lab Terminal")
            print("2. Reset/Override Setup (Fresh Install)")
            print("Q. Quit")
            
            choice = input("\nYour choice: ").strip().lower()
            if choice == '1':
                subprocess.run("docker exec -it hexstrike_gemini_lab /bin/bash", shell=True)
                return
            elif choice == '2':
                if reset_setup():
                    continue # Re-run loop to show main menu
            elif choice == 'q':
                sys.exit(0)
            continue

        choice = main_menu()
        if choice == '1':
            simple_install()
            break
        elif choice == '2':
            complete_install()
            break
        elif choice == 'q':
            sys.exit(0)
        else:
            print("\n[!] Invalid choice. Try again.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Setup interrupted. Goodbye!")
        sys.exit(0)
