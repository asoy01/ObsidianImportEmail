# Obsidian Import Email
## What is this?
This is a script to easily import email messages into an Obsidian vault. The basic workflow is the following:

1. Save an email message as an EML file into a certain directory specified in the configuration file.
1. This EML file is automatically converted into an MD file created in an Obsidian vault.
1. Attachment files will also be put in the Obsidian vault. Links to the attachments are automatically included in the MD file.

This way, you can import an email message into Obsidian just by saving it into an EML file. Vast majority of email softwares and web services, such as Thunderbird, Gmail and Outlook, can save messages in the EML format. Therefore, this method should work robustly.

## Supported platforms
I developed and tested the script using Windows. The explanations in this README assumes you are using Windows. However, the Python script should also work on Linux and Mac (I have not tested it though).

## Prerequisite 
- Python: 3.9 or above
    - Older version may work, but I haven't tested it.
- watchdog package
    - Install with `pip install watchdog`
- markdownify package
    - Install with `pip install markdownify`

## Installation
Download the python script and Settings.json.example file. Put them in a directory, such as ```C:\Users\UserName\ObsidianImportEmail\```. It can be anywhere.

Edit `Settings.json.example` and rename it to `Settings.json`. This file should be located in the same directory as `ImportEML.py`.

## Configuration
You need to edit `Settings.json` to make the script work properly. In this JSON file, you specify the directories of your Obsidian Vault as well as a directory to be watched for new EML files.

The directory structure of your Obsidian Vault is assumed to be the following.
If the root directory of the Vault is `/Path/To/Vault/`, `.md` files are stored in a subdirectory of this, such as `/Path/To/Vault/MarkdownDir/`.
Attachment files are stored in a dedicated directory, such as `/Path/To/Vault/AttachmentDir/`. When an email message is imported into the Vault, `ImportEML.py` will create a Markdown file in `/Path/To/Vault/MarkdownDir/`. Attachment files are stored in the directory `/Path/To/Vault/AttachmentDir/XXXXXX/`, where `XXXXXX` is the Message-ID of the imported message. All the attachments of the message are saved in this subdirectory to avoid name conflicts with attachments of other messages.

In `Settings.json`, `VaultDir` specifies the full path to your Vault's root directory. `MarkdownDir` is the subdirectory name for `.md` files. This can be empty if you keep the MD files in the root of the Vault, which is what I actually do. `AttachmentDir` specifies the subdirectory name for keeping attachment files. This can also be empty.

`WatchDir` specifies the full path of a directory, where new EML files will be saved. The Python script monitors changes to this directory. If a file with the extension `.eml` is created, the file will be processed to be imported into the Vault.

## Running the script
You can run the script from the command line like:
```
python .\ImportEML.py
```
This python script takes a commandline option `-c` or `--config`.
With this option, you can specify the location of the configuration file such as,

```
python .\ImportEML.py -c C:\Users\UserName\Obsidian\Settings.json
```
When this option is omitted, the script tries to read `Settings.json` in the same directory as the script file.

While invoking the script from commandline works fine, this will keep a terminal window opened as long as the script is running. If it is annoying for you, you can try the tricks below.


### Starting the script at the login on Windows
If you want to start the script without opening a terminal window, you can try the following.

1. Open the Task Scheduler
1. Create a task
1. In the Triggers tab, make it start at a login
1. In the Actions tab, create an action to start a program.
    - Program name should be a full path to `pythonw.exe`
        - For example, `C:\Users\UserName\anaconda3\pythonw.exe`
    - Do not use `python.exe`, because it will invoke a terminal window.
    - In the "Add arguments" field, put the full path to `ImportEML.py`.

This way, `ImportEML.py` will be started every time you login to the system.
You can also stop the script from the Task Scheduler.

### Starting the script as a systemd service on Linux.
I created a service file, `save-email-to-obsidian.service`, for systemd to start the script when the system is booted. However, I have never tested it myself. You can try it at your own risk.

### What about Mac?
Since I do not have any Mac, I cannot say anything about it.

## 2023-09-26 RHM:

Test:

The server, running without modification to the code, in a (conda) virtual environment appears to work as advertised.

When in the MacOS, you can run the script from the command line like:

```
python ImportEML.py
```

This python script takes a commandline option `-c` or `--config`.

Without the command line argument `--nohup`, the server will stop when you close the terminal window in which the script is running. Thus, –nohup allows running the server headlessly.

Just remember to disable `--nohup` when you’re troubleshooting or debugging. 🛠️

*Note: It is unclear as to whether the script is designed to allow enabling `nohup` by a durable variable i.e. in `.env.` As best practice, it should be toggled via command line argument on each run.*

### Possible: Automatic Server Restart on MacOS. 🍎

Want the server to start every time you log into your Mac? 

If the python program is invoked with a shell script (start.sh), this might work:

- Open “System Preferences” ➡️ “Login Items.”
- Click ‘+’ ➡️ add `start.sh`.
