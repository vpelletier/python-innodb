#!/usr/bin/env python
import innodb
import libinnodb
import test0aux

DATABASE = 'test'
TABLE = 't'

def create_table(txn, table):
    txn.begin()
    txn.lockSchema(True)
    table_sch = table.newSchema(column_list=(
        ('c1', libinnodb.IB_VARCHAR, 31),
        ('c2', libinnodb.IB_VARCHAR, 31),
        ('c3', libinnodb.IB_INT, 4, libinnodb.IB_COL_UNSIGNED),
    ))
    index_schema = table_sch.newIndex('c1_c2', (('c1', ), ('c2', )),
        clustered=True)
    table_sch.create(txn)
    txn.commit()

def do_query(crsr):
    crsr.goFirst()
    for tpl in crsr.iterForward():
        for x in xrange(len(tpl)):
            print '%r|' % (tpl[x]),
        print

def update_a_row(crsr):
    key_tpl = crsr.getSearchTuple()
    key_tpl[0] = 'a'
    res = crsr.goTo(key_tpl)
    assert res == -1
    new_tpl = crsr.getReadTuple()
    for old_tpl in crsr.iterForward():
        if old_tpl[0] != 'a':
            break
        new_tpl.copy(old_tpl)
        new_tpl[2] = old_tpl[2] + 100
        crsr.update(old_tpl, new_tpl)
        new_tpl.clear()

def delete_a_row(crsr):
    key_tpl = crsr.getSearchTuple()
    key_tpl[0] = 'b'
    key_tpl[1] = 'z'
    res = crsr.goTo(key_tpl)
    assert res == 0
    crsr.delete()

def main():
    txn = innodb.Transaction(libinnodb.IB_TRX_REPEATABLE_READ)
    print 'API: %d.%d.%d' % innodb.api_version()
    idb = innodb.InnoDB()
    test0aux.test_configure()
    idb.startup('barracuda')
    db = idb[DATABASE]
    db.create()
    print 'Create table'
    table = db[TABLE]
    create_table(txn, table)
    print 'Begin transaction'
    txn.begin()
    print 'Open cursor'
    crsr = table.open(txn)
    print 'Lock table in IX'
    crsr.lockTable(libinnodb.IB_LOCK_IX)
    print 'Insert rows'
    crsr.insertRows((
        ('a', 't', 1),
        ('b', 'u', 2),
        ('c', 'b', 3),
        ('d', 'n', 4),
        ('e', 's', 5),
        ('e', 'j', 6),
        ('d', 'f', 7),
        ('c', 'n', 8),
        ('b', 'z', 9),
        ('a', 'i', 10),
    ))
    print 'Query table'
    do_query(crsr)
    print 'Update a row'
    update_a_row(crsr)
    print 'Query table'
    do_query(crsr)
    print 'Delete a row'
    delete_a_row(crsr)
    print 'Query table'
    do_query(crsr)
    print 'Close cursor'
    crsr.close()
    print 'Commit transaction'
    txn.commit()
    print 'Drop table'
    txn.begin()
    txn.lockSchema(True)
    table.drop(txn)
    txn.commit()
    idb.shutdown()

if __name__ == '__main__':
    main()
