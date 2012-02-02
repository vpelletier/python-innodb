#!/usr/bin/env python
import sys
import ctypes
import innodb
import libinnodb
import test0aux

DATABASE = 'test'
TABLE = 't'

def create_table(txn, table):
    table_sch = table.newSchema(column_list=(
        ('c1', libinnodb.IB_INT, ctypes.sizeof(ctypes.c_int)),
    ))
    table_sch.newIndex('PRIMARY', (('c1', ), ), clustered=True)
    txn.begin()
    txn.lockSchema(True)
    table_sch.create(txn)
    txn.commit()

def insert_rows(crsr):
    tpl = crsr.getReadTuple()
    for i in xrange(10):
        tpl[0] = i
        crsr.insert(tpl)
        tpl.clear()

def iterate(crsr, selector):
    tpl = crsr.getReadTuple()
    for tpl in crsr.iterForward():
        if not selector(tpl):
            break

def print_all(tpl):
    test0aux.print_tuple(sys.stdout, tpl._tuple)
    return True

def print_eq_5(tpl):
    result = tpl[0] == 5
    if result:
        test0aux.print_tuple(sys.stdout, tpl._tuple)
    return result

def print_lt_5(tpl):
    result = tpl[0] < 5
    if result:
        test0aux.print_tuple(sys.stdout, tpl._tuple)
    return result

def main():
    idb = innodb.InnoDB()
    test0aux.test_configure()
    idb.startup('barracuda')
    db = idb[DATABASE]
    db.create()
    table = db[TABLE]
    txn = innodb.Transaction(libinnodb.IB_TRX_REPEATABLE_READ)
    create_table(txn, table)
    txn.begin()
    crsr = table.open(txn)
    crsr.lockTable(libinnodb.IB_LOCK_IX)
    insert_rows(crsr)
    print 'SELECT * FROM T;'
    crsr.goFirst()
    iterate(crsr, print_all)
    print 'SELECT * FROM T WHERE c1 = 5;'
    tpl = crsr.getSearchTuple()
    tpl[0] = 5
    crsr.goTo(tpl, libinnodb.IB_CUR_GE)
    iterate(crsr, print_eq_5)
    print 'SELECT * FROM T WHERE c1 > 5;'
    crsr.goTo(tpl, libinnodb.IB_CUR_G)
    iterate(crsr, print_all)
    print 'SELECT * FROM T WHERE c1 < 5;'
    crsr.goFirst()
    iterate(crsr, print_lt_5)
    print 'SELECT * FROM T WHERE c1 >= 1 AND c1 < 5;'
    tpl = crsr.getSearchTuple()
    tpl[0] = 1
    crsr.goTo(tpl, libinnodb.IB_CUR_GE)
    iterate(crsr, print_lt_5)
    crsr.close()
    txn.commit()
    txn.begin()
    txn.lockSchema(True)
    table.drop(txn)
    txn.commit()
    idb.shutdown()

if __name__ == '__main__':
    main()

