import email
from email.header import decode_header
from email.utils import parsedate_to_datetime

class MailParser:
    def __init__(self, mail_file_path):
        with open(mail_file_path, 'rb') as email_file:
            self.email_message = email.message_from_bytes(email_file.read())

    def get_subject(self):
        return self._get_decoded_header("Subject")

    def get_body(self):
        body = ""
        for part in self.email_message.walk():
            if part.get_content_maintype() == 'text':
                charset = str(part.get_content_charset())
                if charset:
                    body += part.get_payload(decode=True).decode(charset, errors="replace")
        return body

    def get_date(self):
        date_str = self._get_decoded_header("Date")
        if date_str:
            return parsedate_to_datetime(date_str)
        return None

    def _get_decoded_header(self, key_name):
        raw_obj = self.email_message.get(key_name)
        if raw_obj is None:
            return ""
        return "".join(
            fragment.decode(encoding or "UTF-8") if isinstance(fragment, bytes) else fragment
            for fragment, encoding in decode_header(raw_obj)
        )
