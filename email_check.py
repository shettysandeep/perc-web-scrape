""" Email check """

from smtplib import SMTP
import re
import requests
import dns.resolver


def ping_school(hostname):
    """ Check if website is active """
    r = requests.get(hostname)
    return r.status_code


def valid_email(email_add):
    """ Check email syntax """
    ptn1 = "^[_a-z0-9-]+(\.[_a-z0-9-]+)"
    ptn2 = "*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"
    match = re.match(ptn1 + ptn2, email_add)
    if match is None:
        return "Check Email - Incorrect Syntax"
    else:
        return "Email syntax valid"


def get_mx(email_add):
    """ Obtain the MX from an email address"""
    domain_name = email_add.split('@')[-1]
    try:
        records = dns.resolver.resolve(domain_name, 'MX')
        mx_data = records[0].exchange
        return str(mx_data)
    except (dns.resolver.NoAnswer):
        return "NoAnswer"
    except (dns.resolver.NXDOMAIN):
        return "NoDomain"


def reach_smtp( email_add, sender_mail, host):
    """ Ping the email via SMTP to verify if active"""
    mx_add = get_mx(email_add)
    with SMTP(mx_add) as server:
        server.set_debuglevel(0)
        server.helo(host)
        server.mail(sender_mail)
        code, message = server.rcpt(email_add)
    return (code, message)


if __name__ == '__main__':
    email_add = "recipient@domain.com"
    host = "domain.com"
    sender_mail = 'sender@domain.org'
    print(get_mx(email_add))
    code, message = reach_smtp(email_add = email_add,
                               host = host,
                               sender_mail = sender_mail)
    print(code, message)
