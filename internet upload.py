import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import subprocess

def install_missing_packages():
    print("Required packages are missing. Installing them automatically via OS...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "internetarchive", "questionary", "pyfiglet"])
        print("\nPackages installed successfully! Restarting the script...\n")
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"Failed to auto-install packages: {e}")
        sys.exit(1)

try:
    import internetarchive as ia
    import questionary
    import pyfiglet
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
    from rich.text import Text
except ImportError:
    install_missing_packages()

# --- INITIAL ASCII ART & MENU ---
try:
    # Adding pyfiglet with 'ansi_shadow' style as requested
    ASCII_LOGO = pyfiglet.figlet_format("INTERNET ARCHIVE", font="ansi_shadow")
except Exception:
    ASCII_LOGO = "ARCHIVE.ORG UPLOADER v2.0"

console = Console()

custom_style = questionary.Style([
    ('qmark', 'fg:cyan bold'), 
    ('question', 'bold'), 
    ('answer', 'fg:green bold'),
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan bold')
])

# Default Settings (Changeable via Menu)
config = {
    "IDENTIFIER": "",
    "LOCAL_PATH": r"",
    "THREADS": 5
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    clear_screen()
    logo_text = Text(ASCII_LOGO, style="bold cyan")
    console.print(logo_text, justify="center")
    console.print(Panel("Welcome to the Internet Archive Uploader v2.0", style="bold green", expand=False))

def upload_engine(file_info):
    remote_path, local_path = file_info
    try:
        ia.upload(config["IDENTIFIER"], {remote_path: str(local_path)}, 
                  metadata={'mediatype': 'movies'}, checksum=True, quiet=True)
        return True, local_path
    except Exception as e:
        return False, e

def login_ia():
    show_header()
    console.print(Panel("[bold yellow]Internet Archive Authentication[/bold yellow]\nLogin with your archive.org email and password.", expand=False))
    email = questionary.text("Enter Email:").ask()
    
    if email is None: return # Ctrl+C handling
    password = questionary.password("Enter Password:").ask()
    if password is None: return
    
    with console.status("[bold green]Authenticating...", spinner="dots"):
        try:
            # internetarchive uses configure to write the config file
            ia.configure(email, password)
            console.print("\n[bold green] Login successful! Credentials saved.[/bold green]")
        except Exception as e:
            console.print(f"\n[bold red] Login failed: {e}[/bold red]")
            
    questionary.press_any_key_to_continue("Press any key to return to menu...").ask()

def interactive_get_identifier(default_val=""):
    choice = questionary.select(
        "How would you like to select the Identifier?",
        choices=[
            questionary.Choice(" Select from my Archive.org Account", "account"),
            questionary.Choice(" Type Link or Identifier manually", "manual")
        ],
        style=custom_style
    ).ask()
    
    if choice == "account":
        with console.status("[bold cyan]Fetching your items from Archive.org...[/bold cyan]", spinner="dots"):
            try:
                cfg = ia.config.get_config().get('s3', {})
                email = ia.get_username(cfg.get('access'), cfg.get('secret'))
                if not email:
                    raise Exception("You are not logged in.")
                items = list(ia.search_items(f'uploader:{email}'))
                identifiers = [item['identifier'] for item in items]
            except Exception as e:
                console.print(f"[bold red]❌ Failed to fetch items: {e}[/bold red]")
                return None
                
        if not identifiers:
            console.print("[bold yellow]No items found in your account![/bold yellow]")
            return None
            
        ident = questionary.select(
            "Select an Item:",
            choices=identifiers,
            style=custom_style
        ).ask()
        return ident
    
    elif choice == "manual":
        item_link = questionary.text("Enter Item Link or Identifier:", default=default_val).ask()
        if not item_link: return None
        if "archive.org/details/" in item_link:
            return item_link.split("archive.org/details/")[-1].split("/")[0]
        else:
            return item_link.strip().strip("/")
            
    return None

def configure_tool():
    show_header()
    console.print(Panel("[bold cyan]Configure Settings[/bold cyan]", expand=False))
    
    ident = interactive_get_identifier(default_val=config["IDENTIFIER"])
    if ident is None: return
    config["IDENTIFIER"] = ident
    
    loc = questionary.path("Enter Local Path:", default=config["LOCAL_PATH"]).ask()
    if loc is None: return
    config["LOCAL_PATH"] = loc
    
    # Validation for threads to ensure it's a number
    def validate_threads(t):
        if str(t).isdigit() and int(t) > 0:
            return True
        return "Please enter a valid positive number"
        
    threads = questionary.text("Enter Thread Count:", default=str(config["THREADS"]), validate=validate_threads).ask()
    if threads is None: return
    config["THREADS"] = int(threads)
    
    console.print("\n[bold green]✓ Settings saved successfully![/bold green]")
    questionary.press_any_key_to_continue("Press any key to return to menu...").ask()

def start_upload():
    show_header()
    
    # Check if local path exists
    local_path = Path(config["LOCAL_PATH"])
    if not local_path.exists() or not local_path.is_dir():
        console.print(f"[bold red]❌ Error: Local path '{local_path}' does not exist or is not a directory.[/bold red]")
        questionary.press_any_key_to_continue("Press any key to return...").ask()
        return

    with console.status(f"[bold cyan]Scanning Archive Identifier: {config['IDENTIFIER']}...[/bold cyan]", spinner="dots"):
        try:
            item = ia.get_item(config['IDENTIFIER'])
            # Extract files successfully from the item, evaluating all remote folders
            uploaded_files = []
            for f in item.files:
                name = f.name if not isinstance(f, dict) else f.get('name')
                if name:
                    # Extracts just the file name, ignoring any archive.org directory paths
                    uploaded_files.append(name.split('/')[-1])
        except Exception as e:
            console.print(f"[bold red] Connection failed or Identifier not found: {e}[/bold red]")
            questionary.press_any_key_to_continue("Press any key to return...").ask()
            return

    all_local = [f for f in local_path.iterdir() if f.is_file()]
    
    # Remote Prefix is removed, files are uploaded to the root of the item directly
    to_upload = [(f.name, f) for f in all_local if f.name not in uploaded_files]

    console.print(Panel(f"[*] Local Files: [cyan]{len(all_local)}[/cyan] | Remaining to Upload: [cyan]{len(to_upload)}[/cyan]", expand=False))
    
    if not to_upload:
        console.print("[bold green]✓ All files are already synced![/bold green]")
        questionary.press_any_key_to_continue("Press any key to return...").ask()
        return

    confirm = questionary.confirm(f"Upload {len(to_upload)} files using {config['THREADS']} threads?", default=True).ask()
    if confirm:
        success_count = 0
        error_count = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            upload_task = progress.add_task("[cyan]Uploading files...", total=len(to_upload))
            
            with ThreadPoolExecutor(max_workers=config['THREADS']) as executor:
                future_to_file = {executor.submit(upload_engine, f): f for f in to_upload}
                
                for future in as_completed(future_to_file):
                    file_tuple = future_to_file[future]
                    file_name = file_tuple[0]
                    success, result = future.result()
                    if success:
                        success_count += 1
                        console.print(f"[green]✓ Uploaded:[/green] {file_name}")
                    else:
                        error_count += 1
                        console.print(f"[red] Failed:[/red] {file_name} ({result})")
                    progress.advance(upload_task, 1)
        
        console.print("\n[bold green]✓ Upload Complete![/bold green]")
        if error_count > 0:
            console.print(f"[bold red]⚠ {error_count} files failed to upload.[/bold red]")
        questionary.press_any_key_to_continue("Press any key to return...").ask()

def start_download():
    show_header()
    console.print(Panel("[bold cyan]Download from Archive.org[/bold cyan]", expand=False))
    
    identifier = interactive_get_identifier()
    if not identifier: return
        
    down_path = questionary.path("Enter Download Path:", default=os.getcwd()).ask()
    if down_path is None: return
    
    target_dir = Path(down_path)
    if not target_dir.exists():
        console.print("[bold yellow]Path does not exist. Creating it...[/bold yellow]")
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            console.print(f"[bold red] Failed to create directory: {e}[/bold red]")
            questionary.press_any_key_to_continue("Press any key to return...").ask()
            return

    console.print(f"\n[cyan]Starting download for '{identifier}' into '{target_dir}'...[/cyan]")
    
    console.print("[bold green]Initializing live download log...[/bold green]")
    try:
        ia.download(identifier, destdir=str(target_dir), verbose=True)
        console.print("\n[bold green]✓ Download Complete![/bold green]")
    except Exception as e:
        console.print(f"\n[bold red] Download failed: {e}[/bold red]")
            
    questionary.press_any_key_to_continue("Press any key to return...").ask()

def contact_creator():
    show_header()
    content = """
[bold]Developed by:[/bold] Sadenism
[bold]Project:[/bold] Sadenism archive uploader 
[bold]Support:[/bold] https://www.patreon.com/c/Sadenism
[bold]discord:[/bold] rubygaveissues
    """
    console.print(Panel(content, title="[bold magenta]Contact Creator[/bold magenta]", border_style="magenta", expand=False))
    questionary.press_any_key_to_continue("Press any key to return to menu...").ask()

def main():
    while True:
        show_header()
        
        choice = questionary.select(
            "Select an option to proceed:",
            choices=[
                questionary.Choice(" Login to Archive.org", "1"),
                questionary.Choice(" Configure Paths & Project", "2"),
                questionary.Choice(" Start Upload Process", "3"),
                questionary.Choice(" Start Download Process", "4"),
                questionary.Choice(" Contact Creator", "5"),
                questionary.Choice(" Exit", "6")
            ],
            style=custom_style
        ).ask()

        if choice == '1': login_ia()
        elif choice == '2': configure_tool()
        elif choice == '3': start_upload()
        elif choice == '4': start_download()
        elif choice == '5': contact_creator()
        elif choice == '6': break
        elif choice is None: break  # User pressed Ctrl+C or Esc during menu

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Operation cancelled by user. Exiting...[/bold red]")
        sys.exit(0)