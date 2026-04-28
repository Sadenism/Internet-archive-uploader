# Sadenism Archive Uploader - Documentation & Examples

Welcome to the official documentation for the **Sadenism Archive Uploader**. This guide will walk you through setting up the tool, logging in, uploading files in bulk, and downloading datasets effortlessly, providing multiple examples of each workflow.

---

## Table of Contents
1. [Initial Setup: Logging In](#1-initial-setup-logging-in)
2. [Workflow Example: Uploading Files](#2-workflow-example-uploading-files)
3. [Workflow Example: Downloading Files](#3-workflow-example-downloading-files)
4. [Advanced Configuration Parameters](#4-advanced-configuration-parameters)

---

## 1. Initial Setup: Logging In

Before you can query your items or push local files, the tool needs to authenticate with `archive.org`. This only needs to be verified once; the tool will safely cache the config for future sessions!

### Example: First-Time Login
When you run the tool (`python "internet upload.py"`), use your arrow keys to select **Login to Archive.org**:

```text
? Select an option to proceed:
❯ 🔑 Login to Archive.org
  ⚙️ Configure Paths & Project
  🚀 Start Upload Process
  📥 Start Download Process
  💬 Contact Creator
  ❌ Exit
```

The app will prompt you for your Archive.org email and password. Your password will be securely hidden while you type:

```text
Internet Archive Authentication
Login with your archive.org email and password.

Enter Email: sadenism_dev@example.com
Enter Password: **************

✓ Login successful! Credentials saved.
```
*Note: From this point forward, you do not need to re-login unless your session expires.*

---

## 2. Workflow Example: Uploading Files

The Sadenism Archive Uploader is built for rapid, multi-threaded pushing. Here is a step-by-step example.

### Step 2a: Configure the Upload
Select **Configure Paths & Project** from the main menu. 

You'll be prompted to choose an identifier. You can map the upload to an item that already exists in your account, or type one manually:

```text
? How would you like to select the Identifier?
❯ 📚 Select from my Archive.org Account
  ✍️ Type Link or Identifier manually

Fetching your items from Archive.org...
? Select an Item:
  my-previous-collection
❯ sadenism_new_archive
  funny_clips_v1
```

Next, provide the local directory containing your videos or files. You can use your `TAB` key to auto-complete paths!

```text
Enter Local Path: C:\Users\Yoshi\Videos\UploadBatch_1\
Enter Thread Count: 10

✓ Settings saved successfully!
```

### Step 2b: Execution and Live Logs
Select **Start Upload Process**. 
The tool will automatically scan the remote `sadenism_new_archive` and verify no duplicate files are uploaded.

```text
[*] Local Files: 42 | Remaining to Upload: 42

? Upload 42 files using 10 threads? (Y/n) y

✓ Uploaded: video_1.mp4
✓ Uploaded: video_2.mp4
❌ Failed: corrupted_video.mp4 (Connection Error)
✓ Uploaded: video_4.mp4

Uploading files... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
✓ Upload Complete!
⚠ 1 files failed to upload.
```

---

## 3. Workflow Example: Downloading Files

If you want to pull down files from Archive.org directly to your local machine, the **Start Download Process** menu makes it effortless.

### Scenario: Downloading an Entire Collection
```text
? Select an option to proceed:
❯ 📥 Start Download Process

Download from Archive.org
? How would you like to select the Identifier?
  📚 Select from my Archive.org Account
❯ ✍️ Type Link or Identifier manually
```

You can literally paste the entire web URL here, and the tool is smart enough to extract what it needs:
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

---

## 4. Advanced Configuration Parameters

Here's an overview of the technical configurations working under the hood:

| Setting Element | Default | Description |
| :--- | :--- | :--- |
| **THREADS** | `10` | The number of simultaneous files pushing up to `archive.org` at any given time. Lower this to `3-5` if you have a slower internet connection to prevent socket dropping. |
| **Duplicate Prevention** | `ON` | The tool extracts the exact base filename of everything in your Archive.org item. If it detects `video.mp4` locally, and `folder/subfolder/video.mp4` on the site, it correctly skips the file saving you bandwidth. |
| **Auto-Retry & Logs** | `N/A` | During uploads, errors don't crash the interface. Failed tasks log directly to the terminal screen with an `❌` icon alongside the exact error reason, while successful tasks get a `✓` and the queue continues seamlessly. |

---
**Need help?** Reach out via [Discord (`rubygaveissues`)](https://discord.com/) or our [Patreon](https://www.patreon.com/c/Sadenism).
