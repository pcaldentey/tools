#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import configparser
import re
import os

from urllib.request import urlopen


class Scan:
    def __init__(self, configFile):
        self.configFile = configFile

    def getComputersFromConf(self):
        self.config = configparser.ConfigParser()
        self.config.read([self.configFile])
        return [(self.config.get(each_section, 'ip'), self.config.get(each_section, 'mac'),
                self.config.get(each_section, 'maker')) for each_section in self.config.sections()]

    def getConnectedComputers(self):

        try:
            command = self.config.get('DEFAULT', 'arpCommand')
            os.system(command + ' > /tmp/scan.tmp')
            output = open('/tmp/scan.tmp', 'r').read().splitlines()
        except Exception as err:
            raise Exception(err)

        comps = []
        for i in output:
            row = re.compile("(.+)\t(.+)\t(.+)", re.DOTALL)
            result = row.search(i)
            if result:
                elem = (result.group(1), result.group(2), result.group(3))
                comps.append(elem)
        return comps

    def getUnknownConnectedComputers(self):
        our_comps = self.getComputersFromConf()
        comps = self.getConnectedComputers()
        for i in our_comps:
            for j in comps:
                if i == j:
                    comps.remove(j)
                if i[0] == '*' and i[1] == j[1] and i[2] == j[2]:
                    comps.remove(j)

        self.comps = comps

    def notify(self):
        if len(self.comps) > 0:
            body = "Unknown computer\\n"
            for i in self.comps:
                body = '%s %s %s %s\\n' % (body, i[0], i[1], i[2])

            command = "echo \"%s\" | mail -s \"ARP scanner\" root" % (body.replace('(', '').replace(')', ''),)
            os.system(command)

            token = self.config.get('DEFAULT', 'telegramToken')
            chatid = self.config.get('DEFAULT', 'telegramChatId')

            message = "****ARP%20Scanner***%0A%0A" + body.replace("\\n", "%0A").replace(" ", "%20")
            url = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (token, chatid, message,)
            try:
                urlopen(url).read()
            except Exception as err:
                raise Exception(err)

    def run(self):
        self.getUnknownConnectedComputers()
        self.notify()


configfile = '/usr/local/sbin/scan.ini'
scan = Scan(configfile)
scan.run()
