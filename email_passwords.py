#!/usr/bin/python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

import argparse
import codecs
import csv
import logging
import socket
import os.path
import ssl
from smtplib import SSLFakeFile

LOGGER = logging.getLogger(__name__)

def setup_args(parser):
    group = parser.add_argument_group('email_passwords')
    group.add_argument('--passwords_csv', default=None)
    group.add_argument('--template_file', default='email_template.txt')
    group.add_argument('--subject', default='[CS194-16] Credentials for Lab 9')
    group.add_argument('--from', dest='from_', default='charles.reiss+cs194@berkeley.edu')
    group.add_argument('--cc', default=None)

    group.add_argument('--smtp_gateway')
    group.add_argument('--smtp_username')
    group.add_argument('--smtp_password')

    group.add_argument('--smtp_certs', default='/etc/ssl/certs/AddTrust_External_Root.pem')

    group.add_argument('--dry_run', action='store_true', default=False)

class MySMTP_SSL(smtplib.SMTP):
    default_port = 465

    def __init__(self, host='', port=0, local_hostname=None,
                 ca_certs=None,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.ca_certs = ca_certs
        smtplib.SMTP.__init__(self, host, port, local_hostname, timeout)

    def _get_socket(self, host, port, timeout):
        if self.debuglevel > 0:
            print>>stderr, 'connect:', (host, port)
        new_socket = socket.create_connection((host, port), timeout)
        new_socket = ssl.wrap_socket(new_socket, cert_reqs=ssl.CERT_REQUIRED,
                                      ca_certs=self.ca_certs)
        self.file = SSLFakeFile(new_socket)
        return new_socket

def generate_email(args, to_email, name, hostname, password):
    with codecs.open(args.template_file, 'r', 'utf-8') as fh:
        template = fh.read() 
        filled_template = template.format(
            to_email=to_email,
            name=name,
            hostname=hostname,
            password=password,
        )
    message = MIMEText(filled_template.encode('utf-8'), 'plain', 'UTF-8')
    message['Subject'] = args.subject
    message['From'] = args.from_
    message['To'] = to_email
    if args.cc:
        message['Cc'] = args.cc
    return message

def send_email(args, message, to_email):
    server = MySMTP_SSL(host=args.smtp_gateway, ca_certs=args.smtp_certs)
    server.login(args.smtp_username, args.smtp_password)
    all_to_emails = [to_email]
    if args.cc:
        all_to_emails = all_to_emails + [args.cc]
    server.sendmail(args.from_, all_to_emails, message.as_string())
    server.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    setup_args(parser)
    args = parser.parse_args()
    logging.basicConfig()
    LOGGER.setLevel(logging.DEBUG)
    with open(args.passwords_csv) as fh:
        reader = csv.DictReader(fh)
        for record in reader:
            message = generate_email(args,
                to_email=record['email'],
                name=record['name'],
                hostname=record['hostname'],
                password=record['password']
            )
            LOGGER.debug('message is %s', message)
            if not args.dry_run:
                send_email(args, message, record['email'])
