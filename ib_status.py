#!/usr/bin/env python

import innodb
from pprint import pprint

def main():
    idb = innodb.InnoDB()
    idb.startup('barracuda')

    for name in idb.getOptionNameList():
        print idb.getOptionType(name), '\t', idb.getOption(name), '\t', name
    pprint(idb.getStatusDict())

    idb.shutdown()

if __name__ == '__main__':
    main()
