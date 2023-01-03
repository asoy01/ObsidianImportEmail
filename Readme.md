# Obsidian Import Email
## What is this?
This is a script to easily import email messages into an Obsidian vault. The basic workflow is the following:

1. Save an email message as an EML file into a certain directory specified in the configuration file.
1. This EML file is automatically converted into an MD file created in an Obsidian vault.
1. Attachment files will also be put in the Obsidian vault. Links to the attachments are automatically included in the MD file.

This way, you can import an email message into Obsidian just by saving it into an EML file. Vast majority of email softwares and web services, such as Thunderbird, Gmail and Outlook, can save messages in the EML format.

## Supported platforms
I developed and tested the scripts using Windows. The explanations in this README assumes you are using Windows. However, the Python script should also work on Linux and Mac (I have not tested it though).

## Prerequisite 
- Python: 3.9 or above
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