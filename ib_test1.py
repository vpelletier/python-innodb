#!/usr/bin/env python
"""
Simple test case:
- creata database
- create table
- insert rows
- update row
- delete row
- drop table

Comes from "ib_test1.c", provided with libinnodb source.
"""
from ctypes import byref, sizeof, Structure, c_char
import sys
import innodb
import libinnodb
import test0aux

DATABASE = 'test'
TABLE = 't'

class row_t(Structure):
    _fields_ = [
        ('c1', c_char * 32),
        ('c2', c_char * 32),
        ('c3', libinnodb.ib_u32_t),
    ]

in_rows = [
    row_t('a', 't', 1),
    row_t('b', 'u', 2),
    row_t('c', 'b', 3),
    row_t('d', 'n', 4),
    row_t('e', 's', 5),
    row_t('e', 'j', 6),
    row_t('d', 'f', 7),
    row_t('c', 'n', 8),
    row_t('b', 'z', 9),
    row_t('a', 'i', 10),
]

def COL_LEN(n):
    return getattr(row_t, n).size

def create_database(name):
    innodb.database_create(name)

def create_table(dbname, name):
    table_id = libinnodb.ib_id_t(0)
    ib_tbl_sch = libinnodb.ib_tbl_sch_t(None)
    ib_idx_sch = libinnodb.ib_idx_sch_t(None)
    table_name = '%s/%s' % (dbname, name)
    innodb.table_schema_create(table_name, byref(ib_tbl_sch),
        libinnodb.IB_TBL_COMPACT, 0)
    for col_name, col_type, col_signed, col_len_offset in (
                ('c1', libinnodb.IB_VARCHAR, libinnodb.IB_COL_NONE, -1),
                ('c2', libinnodb.IB_VARCHAR, libinnodb.IB_COL_NONE, -1),
                ('c3', libinnodb.IB_INT, libinnodb.IB_COL_UNSIGNED, 0),
            ):
        innodb.table_schema_add_col(ib_tbl_sch, col_name, col_type, col_signed,
            0, COL_LEN(col_name) + col_len_offset)
    innodb.table_schema_add_index(ib_tbl_sch, "c1_c2", byref(ib_idx_sch))
    innodb.index_schema_add_col(ib_idx_sch, "c1", 0)
    innodb.index_schema_add_col(ib_idx_sch, "c2", 0)
    innodb.index_schema_set_clustered(ib_idx_sch)
    ib_trx = innodb.trx_begin(libinnodb.IB_TRX_REPEATABLE_READ)
    innodb.schema_lock_exclusive(ib_trx)
    innodb.table_create(ib_trx, ib_tbl_sch, byref(table_id))
    innodb.trx_commit(ib_trx)
    if ib_tbl_sch:
        innodb.table_schema_delete(ib_tbl_sch)

def open_table(dbname, name, ib_trx, crsr):
    table_name = '%s/%s' % (dbname, name)
    innodb.cursor_open_table(table_name, ib_trx, crsr)

def insert_rows(crsr):
    tpl = innodb.clust_read_tuple_create(crsr)
    assert tpl
    for row in in_rows:
        innodb.col_set_value(tpl, 0, byref((c_char * 32)(row.c1)), len(row.c1))
        innodb.col_set_value(tpl, 1, byref((c_char * 32)(row.c2)), len(row.c2))
        innodb.col_set_value(tpl, 2, byref(libinnodb.ib_u32_t(row.c3)), row_t.c3.size)
        innodb.cursor_insert_row(crsr, tpl)
        tpl = innodb.tuple_clear(tpl)
    if tpl:
        innodb.tuple_delete(tpl)

def do_query(crsr):
    tpl = innodb.clust_read_tuple_create(crsr)
    assert tpl
    innodb.cursor_first(crsr)
    while True:
        try:
            innodb.cursor_read_row(crsr, tpl)
        except innodb.InnoDBError, exc:
            error_code = exc.getErrorCode()
            assert(error_code in (libinnodb.DB_END_OF_INDEX,
                libinnodb.DB_RECORD_NOT_FOUND))
            break
        test0aux.print_tuple(sys.stdout, tpl)
        tpl = innodb.tuple_clear(tpl)
        assert tpl
        try:
            innodb.cursor_next(crsr)
        except innodb.InnoDBError, exc:
            error_code = exc.getErrorCode()
            assert(error_code in (libinnodb.DB_END_OF_INDEX,
                libinnodb.DB_RECORD_NOT_FOUND))
            break
    innodb.tuple_delete(tpl)

def main():
    crsr = libinnodb.ib_crsr_t()
    ib_trx = libinnodb.ib_trx_t()
    print 'API: %d.%d.%d' % innodb.api_version()
    innodb.init()
    test0aux.test_configure()
    innodb.startup('barracuda')
    create_database(DATABASE)
    print 'Create table'
    create_table(DATABASE, TABLE)
    print 'Begin transaction'
    ib_trx = innodb.trx_begin(libinnodb.IB_TRX_REPEATABLE_READ)
    assert ib_trx
    print 'Open cursor'
    open_table(DATABASE, TABLE, ib_trx, byref(crsr))
    print 'Lock table in IX'
    innodb.cursor_lock(crsr, libinnodb.IB_LOCK_IX)
    print 'Insert rows'
    insert_rows(crsr)
    print 'Query table'
    do_query(crsr)
    #print 'Update a row'
    #update_a_row(crsr)
    #print 'Query table'
    #do_query(crsr)
    #print 'Delete a row'
    #delete_a_row(crsr)
    #print 'Query table'
    #do_query(crsr)
    print 'Close cursor'
    innodb.cursor_close(crsr)
    print 'Commit transaction'
    innodb.trx_commit(ib_trx)
    print 'Drop table'
    test0aux.drop_table(DATABASE, TABLE)
    innodb.shutdown(libinnodb.IB_SHUTDOWN_NORMAL)

if __name__ == '__main__':
    main()
