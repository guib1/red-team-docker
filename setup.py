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
    print("   - Deploy hexstrike with XFCE4 Desktop + noVNC, TTYD, Files")
    print("   - Open the Web Dashboard in your browser")
    print("\nQ. Quit")
    print("\n----------------------------------------")
    
    choice = input("\nYour choice: ").strip().lower()
    return choice

def simple_install():
    print("\n[*] Starting Simple Install...")
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
    print("[*] Building hexstrike-ai with XFCE4 + noVNC desktop environment...")
    
    # Set the build arg via environment variable (docker-compose interpolates it)
    os.environ["INSTALL_GUI"] = "true"
    
    if not run_command("docker compose build hexstrike-ai", shell=True):
        print("\n[!] Build failed. Please check the logs above.")
        input("\nPress Enter to return to menu...")
        return
    
    print("[*] Deploying all docker-compose services (including TTYD sidecar)...")
    if run_command("docker compose up -d", shell=True):
        with open(MARKER_FILE, "w") as f:
            f.write(f"Setup completed at {time.ctime()}\n")
        
        print("[+] Success! All services are up.")
        print("[+] noVNC Desktop available at http://localhost:6080")
        print("[+] TTYD terminal available at http://localhost:7681")
        print("[+] Your host network (VPN, WireGuard, etc.) is shared with the lab.")

        print("[*] Opening frontend dashboard...")

        time.sleep(5)
        
        frontend_path = os.path.abspath("frontend/index.html")
        if os.path.exists(frontend_path):
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
