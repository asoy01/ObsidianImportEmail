import optparse
import os
import time
import re
import json
import email, email.policy
from email.header import decode_header, make_header
from markdownify import markdownify as md
import unicodedata
import pathlib
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def parse_options():
    # Parse options
    usage = """usage: %prog [options]
    Process an EML file to create an Obsidian note.
    """
    
    parser = optparse.OptionParser(usage=usage)

    default_config = os.path.join(os.path.dirname(__file__), 'Settings.json')
    parser.add_option("-c", "--config", dest="configuration_file", 
                        default=default_config, help="Path to the configuration file")
    
    (options, args) = parser.parse_args()

    return options

def read_configuration_file(file):
    with open(file, mode='r') as f:
        config = json.load(f)

    vault_dir = config['Obsidian']['VaultDir']
    markdown_dir = config['Obsidian']['MarkdownDir']
    attachment_dir = config['Obsidian']['AttachmentDir']
    watch_dir = config['WatchDir']

    return (vault_dir, markdown_dir, attachment_dir, watch_dir)

def process_a_file(file, vault_dir, markdown_dir, attachment_dir):
    
    while not os.path.exists(file):
        time.sleep(0.1)

    # Check if the file extension is eml or not
    (stem, ext) = os.path.splitext(file)
    if ext != ".eml":
        return

    # Regular expressions
    msg_id_regex = re.compile('[\r\n\t]*<([^>]*)>') # Extract a message ID
    remove_excessive_newlines = re.compile("\n\n\n+") # Detect repeated new lines

    # Read the file
    with open(file, mode='rb') as f:
        msg = email.message_from_binary_file(f, policy=email.policy.default)

    # Get Headers
    subject = str(make_header(decode_header(msg["Subject"])))
    from_addr = str(make_header(decode_header(msg["From"])))
    to_addr = str(make_header(decode_header(msg["To"])))

    if msg["Cc"] is None:
        cc_addr = ''
    else:
        cc_addr = str(make_header(decode_header(msg["Cc"])))

    msg_id = msg_id_regex.search(msg['Message-ID']).groups()[0]   
    date = slugify(str(make_header(decode_header(msg["Date"]))))

    # Initialize the MD file body
    md_body = '#Email\n\n---\n\n# Message\n\n## Header\n\nSubject: {}\nFrom: {}\nTo: {}\nCC: {}\nDate: {}\n\n---\n## Body\n\n'.format(subject, from_addr, to_addr, cc_addr, date)

    # Process a body text
    body = msg.get_body(preferencelist=('plain', 'html'))
    if body is not None:
        md_body = process_text_part(body, md_body)

    # Process attachments
    att_num = 1
    for p in msg.iter_attachments():
        if att_num == 1:
            md_body += '\n\n---\n\n## Attachments\n\n'
        md_body = process_attachment(p, md_body, msg_id, vault_dir, attachment_dir)
        att_num += 1

    # Remove excessive \n
    md_body = md_body.replace('\r\n', '\n')
    md_body = remove_excessive_newlines.sub("\n\n", md_body)

    # MD file path
    md_file_path = os.path.join(vault_dir, markdown_dir, slugify(subject) + '-' + msg_id + '.md')
    while os.path.exists(md_file_path):
        md_file_path = change_filename(md_file_path)

    # Save an MD file
    with open(md_file_path, 'w', encoding='utf_8') as f:
        f.write(md_body)

    # Remove the EML file
    os.remove(file)

def process_text_part(part, md_body):
    payload = part.get_payload(decode=True)
    charset = part.get_content_charset()
    body_text = payload.decode(charset, errors="ignore")
    # Convert to MD
    md_text = md(body_text)
    md_body += md_text

    return md_body

def process_attachment(part, md_body, msg_id, vault_dir, attachment_dir):
    # Make a directory to store attachments
    dir_path = os.path.join(vault_dir, attachment_dir, msg_id)
    os.makedirs(dir_path, exist_ok=True)
    
    # File path of the attachment
    file_name = str(make_header(decode_header(part.get_filename())))
    file_path_rel = pathlib.Path(os.path.join(attachment_dir, msg_id, file_name))
    file_path = os.path.join(dir_path, file_name)

    # Save the attachment
    payload = part.get_payload(decode=True)
    with open(file_path, 'wb') as f:
        f.write(payload)

    # Put a link to the MD file
    md_body += '[[' + file_path_rel.as_posix() + '|' + file_name +']]\n'
    
    return md_body

def slugify(value):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert spaces or repeated dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    value = unicodedata.normalize('NFKC', value)
    value = re.sub(r'[^\w\s-]', '', value)
    return re.sub(r'[-\s]+', '-', value).strip('-_')   

def change_filename(path):
    a = path.split('.')
    return a[0] + "-1." + ".".join(a[1:])


if __name__ == '__main__':
    options = parse_options()
    (vault_dir, markdown_dir, attachment_dir, watch_dir) = read_configuration_file(options.configuration_file)

    def on_created(event):
        process_a_file(event.src_path, vault_dir, markdown_dir, attachment_dir)


    event_handler = PatternMatchingEventHandler(['*.eml'])
    event_handler.on_created = on_created

    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



    

