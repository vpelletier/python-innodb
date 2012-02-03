#!/usr/bin/env python

import innodb
from pprint import pprint

def main():
    idb = innodb.InnoDB()
    idb.startup('barracuda')

    pprint(idb.getOptionDict())
    pprint(idb.getStatusDict())

    idb.shutdown()

if __name__ == '__main__':
    main()
