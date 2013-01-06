#!/usr/bin/env python

import innodb
import test0aux
from pprint import pprint

def main():
    idb = innodb.InnoDB()
    test0aux.test_configure()
    idb.startup('barracuda')

    pprint(idb.getOptionDict())
    pprint(idb.getStatusDict())

    idb.shutdown()

if __name__ == '__main__':
    main()
