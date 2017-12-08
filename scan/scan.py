#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from ConfigParser import ConfigParser
import commands
import re,os

class Scan:
    def __init__(self, configFile):
        self.configFile = configFile

    def getComputersFromConf(self):
        self.config = ConfigParser()
        self.config.read([self.configFile])
        return [(self.config.get(each_section,'ip'), each_section,
            self.config.get(each_section, 'maker')) for each_section in self.config.sections() ]

    def getConnectedComputers(self):
        command = self.config.get('DEFAULT', 'arpCommand')
        output = commands.getoutput(command).split('\n')
        comps = []
        for i in output:
            row = re.compile("(.+)\t(.+)\t(.+)",re.DOTALL)
            result = row.search(i)
            if result:
                elem = (result.group(1),result.group(2), result.group(3))
                comps.append(elem)
        return comps

    def getUnknownConnectedComputers(self):
        our_comps = self.getComputersFromConf()
        comps = self.getConnectedComputers()
        for i in our_comps:
           for j in comps:
               if i == j:
                   comps.remove(j)
               if i[0] == '*' and  i[1] == j[1] and i[2] == j[2]:
                   comps.remove(j)

        self.comps = comps

    def notify(self):
        if len(self.comps) > 0:
            body ="Unknown computer\\n"
            for i in self.comps:
                body = '%s %s %s %s\\n' % (body, i[0], i[1], i[2])

            #print body
            command = "echo \"%s\" | mail -s \"HERMEN scaner\" root" % (body.replace('(','').replace(')',''),)
            os.system(command)

    def run(self):
        self.getUnknownConnectedComputers()
        self.notify()


configfile = 'scan.ini'
scan = Scan(configfile)
scan.run()
