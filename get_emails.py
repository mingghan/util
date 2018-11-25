import imaplib
import email
from email.header import decode_header, make_header
from bs4 import BeautifulSoup
from dateutil.parser import parse as date_parse
import pandas as pd
import hashlib
from imapclient import imap_utf7
import re
from tqdm import tqdm_notebook

imap = imaplib.IMAP4_SSL('imap.yandex.ru')
imap.login('<login>', '<password>')

imap.select('inbox')

message_ids_all = imap.search(None, "ALL")
message_ids = message_ids_all[1][0].split()

messages = []
dups = {}
N_CHUNK = 1000
k = 1


def list_folders(imap):
    lst = imap.list()
    for folder in lst[1]:
        # b'(\\Marked \\HasNoChildren) "|" "&BB0EEAQRBB4EIA-"'
        decoded_folder = imap_utf7.decode(folder)
        # (\Marked \HasNoChildren) "|" "НАБОР"
        folder_name = decoded_folder.split(' "|" ')
        print(folder_name, folder)


def get_text_from_html(html):
    soup = BeautifulSoup(html, "lxml")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def from_email_parse(msg):
    email = str(make_header(decode_header(msg['From'])))
    name = ''
    fields = email.split("<")
    if len(fields) > 1:
        name = fields[0]
        email = fields[1].replace(">", "")
    return name, email

def parser(pattern, text):
    res = None
    if text is not np.NaN and type(text) is str:
        res = re.search(pattern, text)
    if res:
        return res.group(1)
    else:
        return text


def parse_email(text):
    return parser('([\w\.\-_]+@([\w-]+\.)+[A-Za-z]{2,4})', text)


def parse_phone(text):
    return parser("([\+0-9\-\(\) ]+)", text)


def extract_from_text(message):
    from_name = re.search("Имя посетителя:(.*)\n", message["text"])
    if from_name:
        message["from_name"] = from_name.group(1)

    phone = re.search("Телефон:(.*)\n", message["text"])
    if phone:
        message["phone"] = parse_phone(phone.group(1))

    email = re.search("Email:(.*)\n", message["text"])
    if email:
        message["from_email"] = parse_email(email.group(1))

    return message


def get_emails(login, password, folder):
    retry_count = 0

    while retry_count <= 1 and k+1 < len(message_ids):
        imap = imaplib.IMAP4_SSL('imap.yandex.ru')
        imap.login(login, password)
        imap.select(folder)
        retry_count += 1
        lst = [i for i in range(k, len(message_ids))]
        try:
            for n, i in tqdm_notebook(enumerate(lst), total=len(lst)):
                print("Got here")
                message = {}
                email_id = message_ids[-1*i]
                status, data = imap.fetch(email_id, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                k = i
                try:
                    message["id"] = email_id
                    message["date"] = date_parse(msg["Date"]).strftime('%Y-%m-%d %H:%M:%S')
                    message["subject"] = subject = str(make_header([(decode_header(msg['Subject'])[0][0], 'utf-8')])) # str(make_header(decode_header(msg['Subject'])))
                    message["from_name"], message["from_email"] = from_email_parse(msg)
                    message["phone"] = ""
                    message["text"] = ""

                    for part in msg.walk():
                        body = part.get_payload(None, True)
                        if body:
                            if part.get_content_charset():
                                body = body.decode(part.get_content_charset())
                            message["text"] += get_text_from_html(body)
                            message = extract_from_text(message)
                    md5 = hashlib.md5(message["text"].encode('utf-8')).hexdigest()
                    if md5 not in dups:
                        messages.append(message)
                        dups[md5] = 1
                except Exception as e:
                    out = open("error_log.txt", "a")
                    out.write(str(e) + "\n======\nemail_id =" + str(email_id) + "\n")
                    out.close()
                if i % N_CHUNK == 0:
                    df = pd.DataFrame(messages)
                    df.to_excel("updated/mulcha_%d.xlsx" % (i // N_CHUNK),
                                columns=["id", "date", "subject", "from_email", "from_name", "phone", "text"],
                                header=["id", "Дата", "Тема", "email", "От кого", "Телефон", "Текст"],
                                index=False
                                )
                    messages = []
        except Exception as e:
            out = open("error_log.txt", "a")
            out.write("+++++%s\n+++++k=%d\n+++++retry_count=%d\n" % (str(e), k, retry_count))
            out.close()

        df = pd.DataFrame(messages)
        df.to_excel("kraska_final.xlsx",
                    columns=["id", "date", "subject", "from_email", "from_name", "phone", "text"],
                    header=["id", "Дата", "Тема", "email", "От кого", "Телефон", "Текст"],
                    index=False
                    )
