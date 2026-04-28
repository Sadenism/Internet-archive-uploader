### Sadenism Archive Uploader

#### Like `ia`, but beautiful. 

**Sadenism Archive Uploader** is a fully interactive, terminal-based tool built in Python. It is designed to act as a powerful bridge to [Archive.org](https://archive.org/), bypassing the limitations of massive browser uploads and the overly complex parameters of traditional CLI text tools.

---

### ✨ Specifications & Core Features

* ** Interactive TUI**
  Navigate via keyboard arrows! Configured with `rich` and `questionary`, it eliminates manual typing errors by providing dynamic visual menus and drop-down selectors.
  
* ** Dynamic Account Mapping**
  No more pasting URLs. Connect your account once, and the script fetches every item you've ever uploaded directly to your terminal. Select where to push and pull your data automatically.

* ** Multi-Threaded Engine**
  Upload thousands of items safely. The tool maps local chunks natively via Python's `ThreadPoolExecutor`, completely avoiding Internet Archive connection dropouts.

* ** Intelligent Duplicate Prevention**
  The script parses your Archive.org metadata recursively. It compares your local files with remote items—even if they're hidden deeply inside subfolders on the server—and skips them if they match.

* ** Native Downloader with Telemetry**
  Pull remote datasets natively directly into custom directories. Features real-time visual `tqdm` logs displaying file speeds, exact bytes, and ETA. 

* ** Zero-Touch Dependencies**
  Run the script right out of the box. The tool intercepts missing package errors and forcefully commands your OS to `pip install` what it needs in the background.

---

###  Getting Started

#### Prerequisites
- `Python 3.7+`

#### Installation & Run
Simply clone the script and run it natively:
```bash
python "internet upload.py"
```

#### Workflow
1. **Login:** Authenticate safely (your credentials are obfuscated and stored securely using the native `internetarchive` API config wrapper).
2. **Configure Paths:** Determine how many threads you want open and provide your Local PC directories.
3. **Execute:** Monitor your upload natively inside the terminal with instant `✓` and `❌` success indicators drawn linearly above your progress bar!

---
*Developed by Sadenism.* 
*(Support via [Patreon](https://www.patreon.com/c/Sadenism) or Discord: `rubygaveissues`)*
