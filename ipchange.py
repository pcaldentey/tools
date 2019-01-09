#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import commands

DEBUG = False


def save_in_file(filename, content):
    """
    Save @content in @filename
    """
    command = "rm -rf %s" % (filename)
    commands.getoutput(command)
    file = open(r'%s' % filename, 'w')
    try:
        file.write(content)
    finally:
        file.close()


def get_actual_ip():
    command = "wget -qO- ifconfig.me/ip"
    output = commands.getoutput(command)
    return output.strip()


def get_ip_from_file(filename):
    """
    Returns saved ip
    """
    try:
        f = open(filename, 'r')
        page = f.read()
    except IOError:
        return

    return page.strip()


def main():
    global DEBUG
    ip_now = get_actual_ip()
    ip_before = get_ip_from_file("ip.txt")
    if ip_now != ip_before and ip_now != '':
        command = "echo \"Actual IP: %s\" | mail -s \"HERMEN IP changed\" root" % (ip_now,)
        if DEBUG:
            print("IP_CHANGED\nactual IP: [%s]".format(ip_now))
            print(command)
        else:
            save_in_file("ip.txt", ip_now)
            os.system(command)


if __name__ == '__main__':
    main()
