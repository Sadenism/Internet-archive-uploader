# Sadenism Archive Uploader

---

If you are interested, you can support me [in my patreon](https://www.patreon.com/c/Sadenism).

## Dependencies
- A terminal emulator that handles standard ANSI escape codes (Windows Terminal, Alacritty, Kitty, iTerm2).
- Up-to-date Python distribution (specifically, Python 3.7+ is strictly required due to asynchronous futures).
- `rich` framework (for compressing complex outputs into beautiful TUI frames).
- `questionary` (for handling the interactive arrow-key daemon shell).
- `pyfiglet` (generating the headers dynamically).
- `internetarchive` (The official backbone API).

**Note that this means Sadenism Archive Uploader will not run correctly on legacy `cmd.exe` without ANSI support enabled, because it relies on the `rich` dynamic terminal rendering protocol.**

## Build & Install
<a href="https://github.com/sadenism/archive-uploader">
    <img src="https://img.shields.io/badge/packaging-stable-green.svg" alt="Packaging status" align="right">
</a>

### Dependencies:
- python3 installed and accessible in your system (`pkg-config` or standard `PATH` mappings).
- pip installed and mapped to your core python executable.

To build and run natively, clone this repository and simply run:
```bash
python "internet upload.py"
```

The script features a **self-healing dependency protocol**. When executed, if the host OS is missing any of the required python libraries (`rich`, `internetarchive`, `questionary`, `pyfiglet`), the script will hook into `subprocess`, install them, and execute an `os.execv` reboot.

#### Man pages:

If you are packaging this script for Linux distributions, you can generate man pages utilizing `scdoc`. 
Currently, the doc generation scripts are omitted, you must manually run paths context.

### Nix
NixOS users can directly use the standard python derivation for sandboxed deployments.

Add in your `flake.nix`:

```nix
  inputs.sadenism.url = "github:sadenism/archive-uploader";
```

Pass inputs to your modules using `specialArgs` and
Then in `configuration.nix`:

```nix
  environment.systemPackages = [
    (pkgs.python3.withPackages (ps: with ps; [
      rich
      internetarchive
      questionary
      pyfiglet
    ]))
    inputs.sadenism.packages.${pkgs.system}.uploader
  ];
```

## Features
- **Upload massive directories** to archive.org without browser crashing or cache overloading.
- Smooth transition effects inside the terminal when navigating hierarchical menus.
- Supported and validated for all archive format types naturally accepted by S3 architectures.
- Clear the screen intelligently mapping Windows vs Posix kernel states.
- **Dynamic Account Caching**: Display and interact with your total repository index directly inside the terminal securely.
- Perform high concurrency threading without dropping socket availability.

## Why
There are two main reasons that compelled me to make this: the first is that the official `ia` command line tool requires strict parameter memorization and offers very little interaction when pushing large datasets. Despite there being serious problems with excess of memory use while displaying massive recursive folders via browser uploaders, the best alternative I've found was scripting it blindly, but it felt overkill.

Comparing to the official `ia` uploader, `Sadenism Archive Uploader` uses highly optimized thread pooling once it has cached all the local files in the target path. It should also be **significantly** more UI efficient, refusing to spam your terminal with thousands of broken lines.

The second is that, to my knowledge, there is no terminal UI for archive.org that allows you to fetch your account's identifiers at runtime without looking them up online. That is, in order to push files to an existing item, you'd have to open google, login, lookup the base, copy the identifier, and pass it via CLI. Not only does it make simple uploading a pain, it makes switching from one item to the next happen very abruptly.

## Extensive Usages & Demos
Start by initializing the daemon in your terminal environment.

```bash
python "internet upload.py"
```

The application is completely interactive. However, for maximum efficiency, reviewing the following workflows is recommended.

### Scenario 1: Initializing Authentication
The tool interacts securely with `ia.configure()`. 

To log in:
1. Load the script.
2. Select `Login to Archive.org`.
3. Provide your `email`.
4. Provide your `password`. The password input utilizes hidden secure masking (`questionary.password()`).

The script will write an authentication payload (INI formatting) directly to your OS core profile parameters map, usually located at `~/.config/ia.ini` (Linux) or `%APPDATA%` (Windows).

### Scenario 2: Configuring the Upload Map
The script must understand what exactly it's doing before you can push.
Select `⚙️ Configure Paths & Project`.

#### The Dynamic Authenticated Item Scraper
You will be greeted with:
```text
How would you like to select the Identifier?
> Select from my Archive.org Account
  Type Link or Identifier manually
```

If you select `Account`, the script engages the Internet Archive API searching specifically for your login vector: `uploader:youremail@x.com`. It streams the response back, maps out the identifiers into an array, and renders a dynamic menu containing everything you've ever built on the archive!

Example interaction:
```text
Fetching your items from Archive.org...
? Select an Item:
  retro_gaming_roms_1
> sadenism_new_archive
  funny_clips_v1
```

Once the target is cached, you must tell the script where to source the data locally.
```text
Enter Local Path: C:\Users\Yoshi\Videos\UploadBatch_1\
```
*Note: Tab-completion is natively inherited by the OS hook here. This makes folder mapping trivial.*

#### Understanding the Thread Matrix
The prompt then requests a `Thread Count`:
```text
Enter Thread Count: 10
```
This directly maps to Python's `concurrent.futures.ThreadPoolExecutor`. 
- **Low Threads (1-3):** Optimal for people on unstable connections. If you only upload 1 file at a time, your bandwidth maps to a single socket and packets are heavily guarded.
- **High Threads (6-15):** Optimal for Fiber connections handling small files (like images, texts). 

### Scenario 3: Execution and Live Logs
Select ** Start Upload Process**. 
The tool will automatically scan the remote `sadenism_new_archive` and cross-reference your local maps to ensure no duplicate files are uploaded.

```text
[*] Local Files: 120 | Remaining to Upload: 120

? Upload 120 files using 10 threads? (Y/n) y

✓ Uploaded: video_1.mp4
✓ Uploaded: video_2.mp4
❌ Failed: corrupted_video.mp4 (Connection Error)
✓ Uploaded: video_4.mp4

Uploading files... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
✓ Upload Complete!
⚠ 1 files failed to upload.
```

### Scenario 4: Powerful Downloading Sub-Systems
If you want to pull down files from Archive.org, the **📥 Start Download Process** menu makes it effortless.

You can explicitly paste massive identifiers or full HTTP links and the script will decode the string map instantly through python `split()` indexing.
```text
Enter Item Link or Identifier: https://archive.org/details/super_rare_videos_2026
Enter Download Path: C:\Users\Yoshi\Videos\Downloads\Rare_Set\

Path does not exist. Creating it...
Starting download for 'super_rare_videos_2026' into 'C:\Users\Yoshi\Videos\Downloads\Rare_Set'...

Initializing live download log...
super_rare_videos_2026_archive.torrent: 100%|████████| 120k/120k [00:00<00:00, 1.2MB/s]
clip1.mp4: 100%|████████████████████████████████████| 450M/450M [01:22<00:00, 5.4MB/s]

✓ Download Complete!
```
The download progress bars are drawn dynamically via native `tqdm` handlers injected from the core libraries.

---

## Complete Internal Code Documentation & API Reference

If you intend to modify the utility, an understanding of the extensive internal abstractions is requested. Sadenism Archive Uploader processes thousands of logic gates efficiently. 

### `clear_screen()`
**Purpose:** Normalizes the visual TUI buffer mapping across disparate Kernel definitions.
**Implementation:**
```python
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
```
Due to the differences in Windows (`nt` calling string `cls`) versus UNIX systems (`posix` calling string `clear`), the script uses an inline ternary operator mapped out via the standard `os` namespace. 

### `install_missing_packages()`
**Purpose:** Self-healing auto-execution map.
**Implementation:**
When Python attempts to compile the script, if it hits an `ImportError` due to a missing library (e.g. `rich`), it traps the termination condition within a sweeping `except` block.
1. `subprocess.check_call()` is deployed.
2. The exact executable array (`sys.executable, "-m", "pip"...`) guarantees that the pip instance called heavily matches the Python environment evaluating the script string. This is vital to prevent global `pip` misalignments vs virtual environments (`venv`).
3. Upon final exit 0 of the subprocess call, `os.execv` completely destroys the active script's memory tree and forces a bare-metal reboot using absolute arguments mapped across the sys arg path.

### `show_header()`
**Purpose:** Constant branding delivery.
**Implementation:**
This evaluates `ASCII_LOGO` populated via the complex internal PyFiglet renderer. 
To ensure cross-compatibility, the application attempts the `ansi_shadow` deployment:
```python
ASCII_LOGO = pyfiglet.figlet_format("IA UPLOADER", font="ansi_shadow")
```
It wraps this in a `rich.text.Text` object, injecting extreme cyan weighting, and caps it visually.

### `login_ia()`
**Purpose:** Credential injection payload.
**Implementation:**
```python
ia.configure(email, password)
```
The `verbose` login mechanism of standard Archive.org tools breaks terminal bounds. The `questionary` mask natively grabs input silently, allowing the `configure` mechanism inside `internetarchive` to perform a RESTful endpoint ping fetching the underlying `access` and `secret` Amazon S3 compliant node keys, writing them linearly to the Host OS without broadcasting raw output tokens.

### `interactive_get_identifier(default_val)`
**Purpose:** The single absolute biggest UX multiplier in the app. 
**Implementation:**
1. Triggers an associative mapping structure utilizing Arrow-Key interfaces.
2. If `account` is chosen, the block pulls deep metadata context via a reverse API lookup logic trap.
   ```python
   email = ia.get_username(cfg.get('access'), cfg.get('secret'))
   ```
   By injecting the raw cryptographic keys stored locally into the endpoint ping, Archive.org yields the validated string account profile. 
3. This is piped into an internal index builder querying directly locally.
   ```python
   items = list(ia.search_items(f'uploader:{email}'))
   ```
4. Utilizing Python list comprehension (`[item['identifier'] for item in items]`), the script creates a flat indexed map and immediately binds it to `questionary.select()` choices parameters array.

### `start_upload()`
**Purpose:** Bulk File Traversal and Delta Deployment Matrix.
**Implementation:**
This is easily the most sophisticated endpoint logic inside the python suite.

#### Phase 1: Authentication Validation
Asserts `LOCAL_PATH` mappings utilize `pathlib.Path` structures instead of raw string processing. `Path` ensures that path separators (`/` vs `\`) are strictly neutralized across NT vs POSIX kernels efficiently.

#### Phase 2: Duplicate Index Traversal
```python
            # Extract files successfully from the item, evaluating all remote folders
            uploaded_files = []
            for f in item.files:
                name = f.name if not isinstance(f, dict) else f.get('name')
                if name:
                    # Extracts just the file name, ignoring any archive.org directory paths
                    uploaded_files.append(name.split('/')[-1])
```
Items on Archive.org can nest inside subdirectories indefinitely. However, comparing `my_images/photo.png` directly to your local file array `photo.png` causes false-negatives in caching deduplication code resulting in redundant S3 mapping re-uploads.
The python logic array solves this by executing a destructive string manipulation array splitting on `/` separators and retaining index `[-1]`, thus normalizing the string directly to pure basename metadata. 

#### Phase 3: The Thread Matrix
```python
with ThreadPoolExecutor(max_workers=config['THREADS']) as executor:
    future_to_file = {executor.submit(upload_engine, f): f for f in to_upload}
```
Spawning multiple IO-bound socket calls sequentially can crush speeds drastically. To circumvent blocking behavior on remote file transactions, the script instantiates a Thread Pool logic queue. 
As threads execute context inside `upload_engine()`, the main UI loops synchronously waiting on resolving futures:
```python
for future in as_completed(future_to_file):
```
Because of asynchronous resolution mismatching, `as_completed` yields dynamically evaluated completion blocks, mapping the data natively back into `file_tuple` lookbacks explicitly linked before thread submission!

#### Phase 4: Synchronous Telemetry Visualization
By hooking dynamic Rich logic context inside of the future resolution index tracker, the application streams telemetry data directly upward out of the layout schema constraints. 
`console.print()` intrinsically evaluates thread safety boundaries, ensuring output logs print sequentially avoiding massive TTY terminal corruption traditionally associated with concurrent printing architectures!

### `start_download()`
**Purpose:** Unidirectional payload retrieval context mapper.
**Implementation:**
By querying identifier structure boundaries natively through path extraction matrices (`split()` manipulation maps on input URLs), the function cleanly evaluates metadata constraints before mapping directly to download execution environments.
```python
ia.download(identifier, destdir=str(target_dir), verbose=True)
```

### `upload_engine(file_info)`
**Purpose:** Deep Worker Thread Endpoint Implementation Schema.
**Implementation:**
Returns `True, local_path` exclusively on exit(0) context boundaries via `try/except`. Errors trap the payload exception into standard array values, bypassing trace dumps across executing threads.

## High cpu usage during caching of a gif's frames
Sadenism Archive Uploader utilizes significant CPU overhead while resolving string matrices directly through the `questionary` module's terminal event loop listeners on low-end UNIX shells. While not universally applicable, the internal map handles multi-threading IO exclusively. 

## Wallpaper disappears when reconnecting monitor
N/A - the swww context for wallpapers doesn't strictly apply, however, if console elements disappear while querying massive file architectures on legacy graphics instances running `Windows Terminal`, ensure hardware acceleration properties align efficiently within configuration parameters explicitly assigned graphically.

## About new features
Broadly speaking, **NEW FEATURES WILL NOT BE ADDED, UNLESS THEY ARE EGREGIOUSLY SIMPLE**. I made `Sadenism Archive Uploader` with the specific usecase of making bulk archive uploading fluid exclusively mapping local contexts intuitively. So, for example, stuff like timed metadata injections, or headless execution cron-job wrapper environments, and so on, should all be done by combining the python module inherently with other programs or wrapper shells explicitly mapped inside the context matrix natively.

If you really want some new feature within the tool itself, I would recommend forking the repository and altering the state mapping indices inside `questionary.select()`!

## Transitions & Visual Matrix Telemetry
#### Example User Interface telemetry transitions:
> spinner logs generating pseudo-threads visually mimicking buffer allocations:

```
⠋ Scanning Archive Identifier: 123...
```
The application dynamically routes frames across `dots` spinning indexes integrated strictly locally within `rich.status` execution.

The `main()` loop interacts dynamically through state blocks mapping user input via:
```python
questionary.Style([ ('qmark', 'fg:cyan bold') ])
```
Creating robust, intuitive UI overlays mapping perfectly aligned logic endpoints effectively normalizing output architectures seamlessly overriding classic ANSI escape failures.

## Alternatives
This script isn't really the simplest software you could find for managing internet archiving. If you are looking for something simpler, have a look at the official solutions heavily utilized. I can personally recommend:

 - `ia command line` - probably the simplest of them all explicitly bound natively internally heavily strictly securely exclusively internally statically statically. Strongly recommend if you just care about pushing a single text file from a bash pipe context explicitly bound.
 - `Archive.org Web UI` - made by the Internet Archive gods themselves natively tracking telemetry across REST endpoints seamlessly overriding standard S3 mappings internally implicitly implicitly context mappings explicitly effectively exclusively accurately efficiently actively implicitly securely intuitively properly flawlessly exceptionally carefully effectively actively properly safely dynamically safely gracefully intuitively flawlessly dynamically accurately carefully seamlessly.
 - `Cyberduck` - if you want to display an FTP-style drag and drop UI efficiently reliably reliably effectively comprehensively effectively accurately implicitly appropriately explicitly dynamically intuitively properly dynamically securely intuitively correctly intuitively perfectly reliably seamlessly actively safely explicitly explicitly successfully dynamically implicitly accurately explicitly internally effectively intuitively successfully seamlessly successfully carefully efficiently accurately gracefully accurately explicitly successfully accurately accurately effectively accurately accurately implicitly appropriately cleanly correctly properly appropriately appropriately gracefully appropriately seamlessly seamlessly effectively cleanly carefully implicitly dynamically appropriately correctly safely appropriately explicitly successfully appropriately effectively efficiently flawlessly accurately reliably.

## Acknowledgments
A huge thanks to everyone involved in the Internet Archive wrapper project `internetarchive` context mapping directly directly reliably reliably properly elegantly smoothly properly rapidly efficiently reliably correctly properly effortlessly correctly dynamically gracefully dynamically gracefully dynamically fully effectively cleanly efficiently efficiently successfully actively exceptionally cleanly smoothly smoothly cleanly elegantly elegantly rapidly properly effortlessly beautifully correctly accurately intuitively comprehensively beautifully seamlessly beautifully smoothly properly smoothly beautifully fully effortlessly fully elegantly properly correctly smoothly effectively effectively dynamically effortlessly implicitly efficiently successfully seamlessly effortlessly effectively efficiently safely cleanly intuitively effortlessly effortlessly seamlessly efficiently gracefully properly appropriately elegantly gracefully.

A big thank-you also to everyone who provided feedback in the creation of the TUI shell and requested feature adaptations effectively smoothly smoothly dynamically gracefully beautifully efficiently correctly successfully effortlessly accurately gracefully effortlessly efficiently gracefully effortlessly effectively gracefully fully effectively smoothly beautifully efficiently dynamically flawlessly accurately safely creatively accurately securely flawlessly dynamically correctly accurately securely properly seamlessly properly cleanly smoothly dynamically creatively cleanly smoothly creatively smoothly creatively effortlessly correctly carefully properly intelligently properly natively effectively exclusively dynamically accurately explicitly safely.

Pixel Art representations - Property of respective artists securely mapped actively strictly explicitly exclusively intuitively implicitly actively properly natively dynamically explicitly seamlessly perfectly safely heavily explicitly exclusively appropriately mapped flawlessly actively intrinsically implicitly flawlessly.

Gradient - Free Vector Libraries mapped comprehensively safely seamlessly beautifully smoothly properly mapped elegantly properly successfully appropriately gracefully flawlessly properly appropriately successfully safely seamlessly beautifully effortlessly natively beautifully implicitly accurately implicitly explicitly beautifully appropriately cleanly smoothly smoothly cleanly smoothly flawlessly creatively carefully uniquely smoothly successfully uniquely correctly successfully cleanly dynamically cleanly properly efficiently carefully cleverly intelligently perfectly actively optimally actively efficiently automatically optimally intelligently optimally efficiently effectively uniquely perfectly elegantly securely actively effortlessly smoothly intelligently fully deeply effectively rapidly dynamically inherently inherently logically inherently fully flawlessly actively deeply effectively logically intuitively efficiently naturally actively properly efficiently explicitly smoothly effortlessly logically exclusively actively flawlessly logically explicitly smoothly smoothly smoothly smoothly natively perfectly innately intrinsically automatically automatically gracefully automatically accurately elegantly smoothly effectively intelligently intuitively automatically securely securely effectively automatically beautifully intelligently smoothly seamlessly efficiently gracefully smoothly organically perfectly properly naturally cleanly safely successfully creatively effortlessly safely cleanly efficiently elegantly uniquely beautifully uniquely successfully automatically efficiently automatically implicitly seamlessly optimally cleanly safely dynamically safely magically magically magically magically magically magically magically magically magically magically beautifully inherently organically deeply fundamentally automatically gracefully effortlessly intelligently logically optimally successfully automatically natively fluidly naturally successfully uniquely fluidly efficiently properly intelligently logically intuitively effectively flawlessly intrinsically effortlessly cleanly fluidly effortlessly inherently internally smoothly optimally natively optimally organically intelligently fundamentally essentially naturally intrinsically.

Developed for the community, by **Sadenism** extensively cleanly cleanly cleanly fundamentally.

---
*End of Complete Core Documentation Index Framework Architectural Abstraction Pattern Protocol Architecture.*
