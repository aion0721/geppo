import os
import email
from email.utils import parsedate_to_datetime, parseaddr
from email.header import decode_header

def decode_to_header(raw_to):
    decoded_parts = []
    for part, encoding in decode_header(raw_to):
        if isinstance(part, bytes):
            decoded_parts.append(part.decode(encoding or 'utf-8', errors='replace'))
        else:
            decoded_parts.append(part)
    return ''.join(decoded_parts)

def parse_eml(file_path):
    with open(file_path, 'rb') as f:
        msg = email.message_from_bytes(f.read())
    
    raw_to = msg.get('To', '')
    to_name, to_email = parseaddr(decode_to_header(raw_to))
    
    # 表示名がなければ、メールアドレスを表示名にもセット
    if not to_name:
        to_name = to_email
    
    date = parsedate_to_datetime(msg.get('Date'))
    
    return to_name, to_email, date

def process_eml_files(eml_directory, output_file):
    eml_files = [f for f in os.listdir(eml_directory) if f.endswith('.eml')]
    unique_emails = {}

    for eml_file in eml_files:
        file_path = os.path.join(eml_directory, eml_file)
        to_name, to_email, date = parse_eml(file_path)
        
        key = (to_email, date)
        if key not in unique_emails:
            unique_emails[key] = file_path

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Toの表示名,Toのメールアドレス,年月日\n")
        for (to_email, date), file_path in unique_emails.items():
            to_name, _, _ = parse_eml(file_path)
            date_str = date.strftime("%Y-%m-%d")
            f.write(f"{to_name},{to_email},{date_str}\n")

    print(f"ファイル '{output_file}' に出力しました。")
