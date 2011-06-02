"""
Comes from "test0aux.c", provided with libinnodb source.
"""

import os
import sys
import ctypes
import innodb
import platform
import libinnodb

log_group_home_dir = 'log'
data_file_path = 'ibdata1:32M:autoextend'

def test_configure():
    try:
        os.mkdir(log_group_home_dir)
    except OSError, (err, msg):
        if err != 17:
            raise
    if platform.system() != 'Windows':
        flush_method = 'O_DIRECT'
    else:
        flush_method = 'async_unbuffered'
    innodb.cfg_set_text('flush_method', flush_method)
    innodb.cfg_set_int('log_files_in_group', 2)
    innodb.cfg_set_int('log_file_size', 32 * 1024 * 1024)
    innodb.cfg_set_int('log_buffer_size', 24 * 16384)
    innodb.cfg_set_int('buffer_pool_size', 5 * 1024 * 1024)
    innodb.cfg_set_int('additional_mem_pool_size', 4 * 1024 * 1024)
    innodb.cfg_set_int('flush_log_at_trx_commit', 1)
    innodb.cfg_set_int('file_io_threads', 4)
    innodb.cfg_set_int('lock_wait_timeout', 60)
    innodb.cfg_set_int('open_files', 300)
    innodb.cfg_set_bool_on('doublewrite')
    innodb.cfg_set_bool_on('checksums')
    innodb.cfg_set_bool_on('rollback_on_timeout')
    innodb.cfg_set_bool_on('print_verbose_log')
    innodb.cfg_set_bool_on('file_per_table')
    innodb.cfg_set_text('data_home_dir', './')
    try:
        innodb.cfg_set_text('log_group_home_dir', log_group_home_dir)
    except innodb.InnoDBError:
        print >>sys.stderr, 'syntax error in log_group_home_dir, or a ' \
            'wrong number of mirrored log groups'
        sys.exit(1)
    try:
        innodb.cfg_set_text('data_file_path', data_file_path)
    except innodb.InnoDBError:
        print >>sys.stderr, 'InnoDB: syntax error in data_file_path'
        sys.exit(1)

def drop_table(dbname, name):
    table_name = '%s/%s' % (dbname, name)
    ib_trx = innodb.trx_begin(libinnodb.IB_TRX_REPEATABLE_READ)
    innodb.schema_lock_exclusive(ib_trx)
    innodb.table_drop(ib_trx, table_name)
    innodb.trx_commit(ib_trx)

_int_col_fmt = {
    (1, libinnodb.IB_COL_UNSIGNED): innodb.tuple_read_u8,
    (1, libinnodb.IB_COL_NONE): innodb.tuple_read_i8,
    (2, libinnodb.IB_COL_UNSIGNED): innodb.tuple_read_u16,
    (2, libinnodb.IB_COL_NONE): innodb.tuple_read_i16,
    (4, libinnodb.IB_COL_UNSIGNED): innodb.tuple_read_u32,
    (4, libinnodb.IB_COL_NONE): innodb.tuple_read_i32,
    (8, libinnodb.IB_COL_UNSIGNED): innodb.tuple_read_u64,
    (8, libinnodb.IB_COL_NONE): innodb.tuple_read_i64,
}

def print_int_col(stream, tpl, i, col_meta):
    stream.write('%d' % (_int_col_fmt[(
        col_meta.type_len, col_meta.attr & libinnodb.IB_COL_UNSIGNED
    )](tpl, i)))

def print_tuple(stream, tpl):
    write = stream.write
    for i in xrange(innodb.tuple_get_n_cols(tpl)):
        data_len, col_meta = innodb.col_get_meta(tpl, i)
        col_type = col_meta.type
        if col_type == libinnodb.IB_SYS:
            continue
        if data_len != libinnodb.IB_SQL_NULL:
            if col_type == libinnodb.IB_INT:
                print_int_col(stream, tpl, i, col_meta)
            elif col_type == libinnodb.IB_FLOAT:
                write('%f' % (innodb.tuple_read_float(tpl, i), ))
            elif col_type == libinnodb.IB_DOUBLE:
                write('%lf' % (innodb.tuple_read_double(tpl, i), ))
            elif col_type in (libinnodb.IB_CHAR, libinnodb.IB_BLOB,
                    libinnodb.IB_DECIMAL, libinnodb.IB_VARCHAR):
                write('%d:%r' % (data_len,
                    ctypes.string_at(innodb.col_get_value(tpl, i), data_len)))
            else:
                raise AssertionError(col_type)
        write('|')
    write('\n')

