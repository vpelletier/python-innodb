from ctypes import *
import ctypes.util as util
from enum import Enum
import sys

_func_type_kw = {}
if sys.version_info[:2] >= (2, 6):
    _func_type_kw['use_errno'] = True
    _func_type_kw['use_last_error'] = True

def _loadLibrary():
    import platform
    system = platform.system()
    if system == 'Linux':
        dll_loader = CDLL
        path = util.find_library('innodb')
    else:
        raise NotImplementedError('System not supported: %r' % (system, ))
    if path is None:
        raise Exception('Can\'t locate innodb library')
    return dll_loader(path, **_func_type_kw)

def FUNCTYPE(*args):
    # XXX: is callback type really C even on windows ?
    return CFUNCTYPE(*args, **_func_type_kw)

libinnodb = _loadLibrary()
del _loadLibrary

db_err = Enum(globals(), [
    ('DB_SUCCESS', 10),
    ('DB_ERROR', None),
    ('DB_INTERRUPTED', None),
    ('DB_OUT_OF_MEMORY', None),
    ('DB_OUT_OF_FILE_SPACE', None),
    ('DB_LOCK_WAIT', None),
    ('DB_DEADLOCK', None),
    ('DB_ROLLBACK', None),
    ('DB_DUPLICATE_KEY', None),
    ('DB_QUE_THR_SUSPENDED', None),
    ('DB_MISSING_HISTORY', None),
    ('DB_CLUSTER_NOT_FOUND', 30),
    ('DB_TABLE_NOT_FOUND', None),
    ('DB_MUST_GET_MORE_FILE_SPACE', None),
    ('DB_TABLE_IS_BEING_USED', None),
    ('DB_TOO_BIG_RECORD', None),
    ('DB_LOCK_WAIT_TIMEOUT', None),
    ('DB_NO_REFERENCED_ROW', None),
    ('DB_ROW_IS_REFERENCED', None),
    ('DB_CANNOT_ADD_CONSTRAINT', None),
    ('DB_CORRUPTION', None),
    ('DB_COL_APPEARS_TWICE_IN_INDEX', None),
    ('DB_CANNOT_DROP_CONSTRAINT', None),
    ('DB_NO_SAVEPOINT', None),
    ('DB_TABLESPACE_ALREADY_EXISTS', None),
    ('DB_TABLESPACE_DELETED', None),
    ('DB_LOCK_TABLE_FULL', None),
    ('DB_FOREIGN_DUPLICATE_KEY', None),
    ('DB_TOO_MANY_CONCURRENT_TRXS', None),
    ('DB_UNSUPPORTED', None),
    ('DB_PRIMARY_KEY_IS_NULL', None),
    ('DB_FATAL', None),
    ('DB_FAIL', 1000),
    ('DB_OVERFLOW', None),
    ('DB_UNDERFLOW', None),
    ('DB_STRONG_FAIL', None),
    ('DB_ZIP_OVERFLOW', None),
    ('DB_RECORD_NOT_FOUND', 1500),
    ('DB_END_OF_INDEX', None),
    ('DB_SCHEMA_ERROR', 2000),
    ('DB_DATA_MISMATCH', None),
    ('DB_SCHEMA_NOT_LOCKED', None),
    ('DB_NOT_FOUND', None),
    ('DB_READONLY', None),
    ('DB_INVALID_INPUT', None),
])

IB_TRUE = 1
IB_FALSE = 0

# Define a subclass, so function having this type for retval can be
# auto-detected.
class ib_err_t(c_int): # XXX: unsure
    pass
ib_byte_t = c_byte
ib_ulint_t = c_ulong
ib_opaque_t = c_void_p
ib_bool_t = ib_ulint_t
ib_charset_t = ib_opaque_t
ib_i8_t = c_byte
assert sizeof(ib_i8_t) == 1
ib_u8_t = c_ubyte
assert sizeof(ib_u8_t) == 1
ib_i16_t = c_short
assert sizeof(ib_i16_t) == 2
ib_u16_t = c_ushort
assert sizeof(ib_u16_t) == 2
ib_i32_t = c_int
assert sizeof(ib_i32_t) == 4
ib_u32_t = c_uint
assert sizeof(ib_u32_t) == 4
ib_i64_t = c_long
assert sizeof(ib_i64_t) == 8
ib_u64_t = c_ulong
assert sizeof(ib_u64_t) == 8
ib_id_t = ib_u64_t

ib_cfg_type = Enum(globals(), [
    ('IB_CFG_IBOOL', None),
    ('IB_CFG_ULINT', None),
    ('IB_CFG_ULONG', None),
    ('IB_CFG_TEXT', None),
    ('IB_CFG_CB', None),
])
ib_cfg_type_t = c_int # XXX: unsure

ib_col_type = Enum(globals(), [
    ('IB_VARCHAR', 1),
    ('IB_CHAR', 2),
    ('IB_BINARY', 3),
    ('IB_VARBINARY', 4),
    ('IB_BLOB', 5),
    ('IB_INT', 6),
    ('IB_SYS', 8),
    ('IB_FLOAT', 9),
    ('IB_DOUBLE', 10),
    ('IB_DECIMAL', 11),
    ('IB_VARCHAR_ANYCHARSET', 12),
    ('IB_CHAR_ANYCHARSET', 13),
])
ib_col_type_t = c_int # XXX: unsure

ib_tbl_fmt = Enum(globals(), [
    ('IB_TBL_REDUNDANT', None),
    ('IB_TBL_COMPACT', None),
    ('IB_TBL_DYNAMIC', None),
    ('IB_TBL_COMPRESSED', None),
])
ib_tbl_fmt_t = c_int # XXX: unsure

ib_col_attr = Enum(globals(), [
    ('IB_COL_NONE', 0),
    ('IB_COL_NOT_NULL', 1),
    ('IB_COL_UNSIGNED', 2),
    ('IB_COL_NOT_USED', 4),
    ('IB_COL_CUSTOM1', 8),
    ('IB_COL_CUSTOM2', 16),
    ('IB_COL_CUSTOM3', 32),
])
ib_col_attr_t = c_int # XXX: unsure

ib_lck_mode = Enum(globals(), [
    ('IB_LOCK_IS', 0),
    ('IB_LOCK_IX', None),
    ('IB_LOCK_S', None),
    ('IB_LOCK_X', None),
    ('IB_LOCK_NOT_USED', None),
    ('IB_LOCK_NONE', None),
])
IB_LOCK_NUM = IB_LOCK_NONE
ib_lck_mode_t = c_int # XXX: unsure

ib_srch_mode = Enum(globals(), [
    ('IB_CUR_G', 1),
    ('IB_CUR_GE', 2),
    ('IB_CUR_L', 3),
    ('IB_CUR_LE', 4),
])
ib_srch_mode_t = c_int # XXX: unsure

ib_match_mode = Enum(globals(), [
    ('IB_CLOSEST_MATCH', None),
    ('IB_EXACT_MATCH', None),
    ('IB_EXACT_PREFIX', None),
])
ib_match_mode_t = c_int # XXX: unsure

class ib_col_meta_t(Structure):
    _fields_ = [
        ('type', ib_col_type_t),
        ('attr', ib_col_attr_t),
        ('type_len', ib_u32_t),
        ('client_type', ib_u16_t),
        ('charset', POINTER(ib_charset_t)),
    ]

ib_trx_state = Enum(globals(), [
    ('IB_TRX_NOT_STARTED', None),
    ('IB_TRX_ACTIVE', None),
    ('IB_TRX_COMMITTED_IN_MEMORY', None),
    ('IB_TRX_PREPARED', None),
])
ib_trx_state_t = c_int # XXX: unsure

ib_trx_level = Enum(globals(), [
    ('IB_TRX_READ_UNCOMMITTED', 0),
    ('IB_TRX_READ_COMMITTED', 1),
    ('IB_TRX_REPEATABLE_READ', 2),
    ('IB_TRX_SERIALIZABLE', 3),
])
ib_trx_level_t = c_int # XXX: unsure

ib_shutdown = Enum(globals(), [
    ('IB_SHUTDOWN_NORMAL', None),
    ('IB_SHUTDOWN_NO_IBUFMERGE_PURGE', None),
    ('IB_SHUTDOWN_NO_BUFPOOL_FLUSH', None),
])
ib_shutdown_t = c_int # XXX: unsure

ib_cb_t = POINTER(FUNCTYPE(None))
ib_msg_stream_t = c_void_p # XXX: actually a FILE *, but asked to handle as
                           # an opaque type in header
#ib_msg_log_t = POINTER(FUNCTYPE(c_int,
#    ib_msg_stream_t, c_char_p)) # va_arg implicit
ib_tpl_t = c_void_p
ib_trx_t = c_void_p
ib_crsr_t = c_void_p
ib_tbl_sch_t = c_void_p
ib_idx_sch_t = c_void_p

ib_schema_visitor_version = Enum(globals(), [
    ('IB_SCHEMA_VISITOR_TABLE', 1),
    ('IB_SCHEMA_VISITOR_TABLE_COL', 2),
    ('IB_SCHEMA_VISITOR_TABLE_AND_INDEX', 3),
    ('IB_SCHEMA_VISITOR_TABLE_AND_INDEX_COL', 4),
])
ib_schema_visitor_version_t = c_int # XXX: unsure

ib_schema_visitor_table_all_t = POINTER(FUNCTYPE(c_int,
    py_object, c_char_p, c_int))
ib_schema_visitor_table_t = POINTER(FUNCTYPE(c_int,
    py_object, c_char_p, ib_tbl_fmt_t, ib_ulint_t, c_int, c_int))
ib_schema_visitor_table_col_t = POINTER(FUNCTYPE(c_int,
    py_object, c_char_p, ib_col_type_t, ib_ulint_t, ib_col_attr_t))
ib_schema_visitor_index_t = POINTER(FUNCTYPE(c_int,
    py_object, c_char_p, ib_bool_t, ib_bool_t, c_int))
ib_schema_visitor_index_col_t = POINTER(FUNCTYPE(c_int,
    py_object, c_char_p, ib_ulint_t))
class ib_schema_visitor_t(Structure):
    _fields_ = [
        ('version', ib_schema_visitor_version_t),
        ('table', ib_schema_visitor_table_t),
        ('table_col', ib_schema_visitor_table_col_t),
        ('index', ib_schema_visitor_index_t),
        ('index_col', ib_schema_visitor_index_col_t),
    ]

ib_client_cmp_t = POINTER(FUNCTYPE(c_int,
    POINTER(ib_col_meta_t), POINTER(ib_byte_t), ib_ulint_t,
        POINTER(ib_byte_t), ib_ulint_t))

IB_SQL_NULL = 0xFFFFFFFF
IB_N_SYS_COLS = 3
MAX_TEXT_LEN = 4096
IB_MAX_COL_NAME_LEN = 64 * 3
IB_MAX_TABLE_NAME_LEN = 64 * 3

def ib_tbl_sch_add_blob_col(s, n):
    return ib_table_schema_add_col(s, n, IB_BLOB, IB_COL_NONE, 0, 0)

def ib_tbl_sch_add_text_col(s, n):
    return ib_table_schema_add_col(s, n, IB_VARCHAR, IB_COL_NONE, 0,
        MAX_TEXT_LEN)

def ib_tbl_sch_add_varchar_col(s, n, l):
    return ib_table_schema_add_col(s, n, IB_VARCHAR, IB_COL_NONE, 0, l)

def ib_tbl_sch_add_u32_col(s, n):
    return ib_table_schema_add_col(s, n, IB_INT, IB_COL_UNSIGNED, 0, 4)

def ib_tbl_sch_add_u64_col(s, n):
    return ib_table_schema_add_col(s, n, IB_INT, IB_COL_UNSIGNED, 0, 8)

def ib_tbl_sch_add_u64_notnull_col(s, n):
    return ib_table_schema_add_col(s, n, IB_INT,
        IB_COL_NOT_NULL | IB_COL_UNSIGNED, 0, 8)

ib_client_compare = ib_client_cmp_t.in_dll(libinnodb, 'ib_client_compare')

ib_api_version = libinnodb.ib_api_version
ib_api_version.restype = ib_u64_t
ib_api_version.argtypes = []

ib_init = libinnodb.ib_init
ib_init.restype = ib_err_t
ib_init.argtypes = []

ib_startup = libinnodb.ib_startup
ib_startup.restype = ib_err_t
ib_startup.argtypes = [c_char_p]

ib_shutdown = libinnodb.ib_shutdown
ib_shutdown.restype = ib_err_t
ib_shutdown.argtypes = [ib_shutdown_t]

ib_trx_start = libinnodb.ib_trx_start
ib_trx_start.restype = ib_err_t
ib_trx_start.argtypes = [ib_trx_t, ib_trx_level_t]

ib_trx_begin = libinnodb.ib_trx_begin
ib_trx_begin.restype = ib_trx_t
ib_trx_begin.argtypes = [ib_trx_level_t]

ib_trx_state = libinnodb.ib_trx_state
ib_trx_state.restype = ib_trx_state_t
ib_trx_state.argtypes = [ib_trx_t]

ib_trx_release = libinnodb.ib_trx_release
ib_trx_release.restype = ib_err_t
ib_trx_release.argtypes = [ib_trx_t]

ib_trx_commit = libinnodb.ib_trx_commit
ib_trx_commit.restype = ib_err_t
ib_trx_commit.argtypes = [ib_trx_t]

ib_trx_rollback = libinnodb.ib_trx_rollback
ib_trx_rollback.restype = ib_err_t
ib_trx_rollback.argtypes = [ib_trx_t]

ib_table_schema_add_col = libinnodb.ib_table_schema_add_col
ib_table_schema_add_col.restype = ib_err_t
ib_table_schema_add_col.argtypes = [ib_tbl_sch_t, c_char_p, ib_col_type_t,
    ib_col_attr_t, ib_u16_t, ib_ulint_t]

ib_table_schema_add_index = libinnodb.ib_table_schema_add_index
ib_table_schema_add_index.restype = ib_err_t
ib_table_schema_add_index.argtypes = [ib_tbl_sch_t, c_char_p,
    POINTER(ib_idx_sch_t)]

ib_table_schema_delete = libinnodb.ib_table_schema_delete
ib_table_schema_delete.restype = None
ib_table_schema_delete.argtypes = [ib_tbl_sch_t]

ib_table_schema_create = libinnodb.ib_table_schema_create
ib_table_schema_create.restype = ib_err_t
ib_table_schema_create.argtypes = [c_char_p, POINTER(ib_tbl_sch_t),
    ib_tbl_fmt_t, ib_ulint_t]

ib_index_schema_add_col = libinnodb.ib_index_schema_add_col
ib_index_schema_add_col.restype = ib_err_t
ib_index_schema_add_col.argtypes = [ib_idx_sch_t, c_char_p, ib_ulint_t]

ib_index_schema_create = libinnodb.ib_index_schema_create
ib_index_schema_create.restype = ib_err_t
ib_index_schema_create.argtypes = [ib_trx_t, c_char_p, c_char_p,
    POINTER(ib_idx_sch_t)]

ib_index_schema_set_clustered = libinnodb.ib_index_schema_set_clustered
ib_index_schema_set_clustered.restype = ib_err_t
ib_index_schema_set_clustered.argtypes = [ib_idx_sch_t]

ib_cursor_set_simple_select = libinnodb.ib_cursor_set_simple_select
ib_cursor_set_simple_select.restype = None
ib_cursor_set_simple_select.argtypes = [ib_crsr_t]

ib_index_schema_set_unique = libinnodb.ib_index_schema_set_unique
ib_index_schema_set_unique.restype = ib_err_t
ib_index_schema_set_unique.argtypes = [ib_idx_sch_t]

ib_index_schema_delete = libinnodb.ib_index_schema_delete
ib_index_schema_delete.restype = None
ib_index_schema_delete.argtypes = [ib_idx_sch_t]

ib_table_create = libinnodb.ib_table_create
ib_table_create.restype = ib_err_t
ib_table_create.argtypes = [ib_trx_t, ib_tbl_sch_t, POINTER(ib_id_t)]

ib_index_create = libinnodb.ib_index_create
ib_index_create.restype = ib_err_t
ib_index_create.argtypes = [ib_idx_sch_t, POINTER(ib_id_t)]

ib_table_drop = libinnodb.ib_table_drop
ib_table_drop.restype = ib_err_t
ib_table_drop.argtypes = [ib_trx_t, c_char_p]

ib_index_drop = libinnodb.ib_index_drop
ib_index_drop.restype = ib_err_t
ib_index_drop.argtypes = [ib_trx_t, ib_id_t]

ib_cursor_open_table_using_id = libinnodb.ib_cursor_open_table_using_id
ib_cursor_open_table_using_id.restype = ib_err_t
ib_cursor_open_table_using_id.argtypes = [ib_id_t, ib_trx_t,
    POINTER(ib_crsr_t)]

ib_cursor_open_index_using_id = libinnodb.ib_cursor_open_index_using_id
ib_cursor_open_index_using_id.restype = ib_err_t
ib_cursor_open_index_using_id.argtypes = [ib_id_t, ib_trx_t,
    POINTER(ib_crsr_t)]

ib_cursor_open_index_using_name = libinnodb.ib_cursor_open_index_using_name
ib_cursor_open_index_using_name.restype = ib_err_t
ib_cursor_open_index_using_name.argtypes = [ib_crsr_t, c_char_p,
    POINTER(ib_crsr_t)]

ib_cursor_open_table = libinnodb.ib_cursor_open_table
ib_cursor_open_table.restype = ib_err_t
ib_cursor_open_table.argtypes = [c_char_p, ib_trx_t, POINTER(ib_crsr_t)]

ib_cursor_reset = libinnodb.ib_cursor_reset
ib_cursor_reset.restype = ib_err_t
ib_cursor_reset.argtypes = [ib_crsr_t]

ib_cursor_close = libinnodb.ib_cursor_close
ib_cursor_close.restype = ib_err_t
ib_cursor_close.argtypes = [ib_crsr_t]

ib_cursor_insert_row = libinnodb.ib_cursor_insert_row
ib_cursor_insert_row.restype = ib_err_t
ib_cursor_insert_row.argtypes = [ib_crsr_t, ib_tpl_t]

ib_cursor_update_row = libinnodb.ib_cursor_update_row
ib_cursor_update_row.restype = ib_err_t
ib_cursor_update_row.argtypes = [ib_crsr_t, ib_tpl_t, ib_tpl_t]

ib_cursor_delete_row = libinnodb.ib_cursor_delete_row
ib_cursor_delete_row.restype = ib_err_t
ib_cursor_delete_row.argtypes = [ib_crsr_t]

ib_cursor_read_row = libinnodb.ib_cursor_read_row
ib_cursor_read_row.restype = ib_err_t
ib_cursor_read_row.argtypes = [ib_crsr_t, ib_tpl_t]

ib_cursor_prev = libinnodb.ib_cursor_prev
ib_cursor_prev.restype = ib_err_t
ib_cursor_prev.argtypes = [ib_crsr_t]

ib_cursor_next = libinnodb.ib_cursor_next
ib_cursor_next.restype = ib_err_t
ib_cursor_next.argtypes = [ib_crsr_t]

ib_cursor_first = libinnodb.ib_cursor_first
ib_cursor_first.restype = ib_err_t
ib_cursor_first.argtypes = [ib_crsr_t]

ib_cursor_last = libinnodb.ib_cursor_last
ib_cursor_last.restype = ib_err_t
ib_cursor_last.argtypes = [ib_crsr_t]

ib_cursor_moveto = libinnodb.ib_cursor_moveto
ib_cursor_moveto.restype = ib_err_t
ib_cursor_moveto.argtypes = [ib_crsr_t, ib_tpl_t, ib_srch_mode_t,
    POINTER(c_int)]

ib_cursor_attach_trx = libinnodb.ib_cursor_attach_trx
ib_cursor_attach_trx.restype = None
ib_cursor_attach_trx.argtypes = [ib_crsr_t, ib_trx_t]

ib_set_client_compare = libinnodb.ib_set_client_compare
ib_set_client_compare.restype = None
ib_set_client_compare.argtypes = [ib_client_cmp_t]

ib_cursor_set_match_mode = libinnodb.ib_cursor_set_match_mode
ib_cursor_set_match_mode.restype = None
ib_cursor_set_match_mode.argtypes = [ib_crsr_t, ib_match_mode_t]

ib_col_set_value = libinnodb.ib_col_set_value
ib_col_set_value.restype = ib_err_t
ib_col_set_value.argtypes = [ib_tpl_t, ib_ulint_t, c_void_p, ib_ulint_t]

ib_col_get_len = libinnodb.ib_col_get_len
ib_col_get_len.restype = ib_ulint_t
ib_col_get_len.argtypes = [ib_tpl_t, ib_ulint_t]

ib_col_copy_value = libinnodb.ib_col_copy_value
ib_col_copy_value.restype = ib_ulint_t
ib_col_copy_value.argtypes = [ib_tpl_t, ib_ulint_t, c_void_p, ib_ulint_t]

ib_tuple_read_i8 = libinnodb.ib_tuple_read_i8
ib_tuple_read_i8.restype = ib_err_t
ib_tuple_read_i8.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(ib_i8_t)]

ib_tuple_read_u8 = libinnodb.ib_tuple_read_u8
ib_tuple_read_u8.restype = ib_err_t
ib_tuple_read_u8.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(ib_u8_t)]

ib_tuple_read_i16 = libinnodb.ib_tuple_read_i16
ib_tuple_read_i16.restype = ib_err_t
ib_tuple_read_i16.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(ib_i16_t)]

ib_tuple_read_u16 = libinnodb.ib_tuple_read_u16
ib_tuple_read_u16.restype = ib_err_t
ib_tuple_read_u16.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(ib_u16_t)]

ib_tuple_read_i32 = libinnodb.ib_tuple_read_i32
ib_tuple_read_i32.restype = ib_err_t
ib_tuple_read_i32.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(ib_i32_t)]

ib_tuple_read_u32 = libinnodb.ib_tuple_read_u32
ib_tuple_read_u32.restype = ib_err_t
ib_tuple_read_u32.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(ib_u32_t)]

ib_tuple_read_i64 = libinnodb.ib_tuple_read_i64
ib_tuple_read_i64.restype = ib_err_t
ib_tuple_read_i64.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(ib_i64_t)]

ib_tuple_read_u64 = libinnodb.ib_tuple_read_u64
ib_tuple_read_u64.restype = ib_err_t
ib_tuple_read_u64.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(ib_u64_t)]

ib_col_get_value = libinnodb.ib_col_get_value
ib_col_get_value.restype = c_void_p
ib_col_get_value.argtypes = [ib_tpl_t, ib_ulint_t]

ib_col_get_meta = libinnodb.ib_col_get_meta
ib_col_get_meta.restype = ib_ulint_t
ib_col_get_meta.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(ib_col_meta_t)]

ib_tuple_clear = libinnodb.ib_tuple_clear
ib_tuple_clear.restype = ib_tpl_t
ib_tuple_clear.argtypes = [ib_tpl_t]

ib_tuple_get_cluster_key = libinnodb.ib_tuple_get_cluster_key
ib_tuple_get_cluster_key.restype = ib_err_t
ib_tuple_get_cluster_key.argtypes = [ib_crsr_t, POINTER(ib_tpl_t), ib_tpl_t]

ib_tuple_copy = libinnodb.ib_tuple_copy
ib_tuple_copy.restype = ib_err_t
ib_tuple_copy.argtypes = [ib_tpl_t, ib_tpl_t]

ib_sec_search_tuple_create = libinnodb.ib_sec_search_tuple_create
ib_sec_search_tuple_create.restype = ib_tpl_t
ib_sec_search_tuple_create.argtypes = [ib_crsr_t]

ib_sec_read_tuple_create = libinnodb.ib_sec_read_tuple_create
ib_sec_read_tuple_create.restype = ib_tpl_t
ib_sec_read_tuple_create.argtypes = [ib_crsr_t]

ib_clust_search_tuple_create = libinnodb.ib_clust_search_tuple_create
ib_clust_search_tuple_create.restype = ib_tpl_t
ib_clust_search_tuple_create.argtypes = [ib_crsr_t]

ib_clust_read_tuple_create = libinnodb.ib_clust_read_tuple_create
ib_clust_read_tuple_create.restype = ib_tpl_t
ib_clust_read_tuple_create.argtypes = [ib_crsr_t]

ib_tuple_get_n_user_cols = libinnodb.ib_tuple_get_n_user_cols
ib_tuple_get_n_user_cols.restype = ib_ulint_t
ib_tuple_get_n_user_cols.argtypes = [ib_tpl_t]

ib_tuple_get_n_cols = libinnodb.ib_tuple_get_n_cols
ib_tuple_get_n_cols.restype = ib_ulint_t
ib_tuple_get_n_cols.argtypes = [ib_tpl_t]

ib_tuple_delete = libinnodb.ib_tuple_delete
ib_tuple_delete.restype = None
ib_tuple_delete.argtypes = [ib_tpl_t]

ib_cursor_truncate = libinnodb.ib_cursor_truncate
ib_cursor_truncate.restype = ib_err_t
ib_cursor_truncate.argtypes = [POINTER(ib_crsr_t), POINTER(ib_id_t)]

ib_table_truncate = libinnodb.ib_table_truncate
ib_table_truncate.restype = ib_err_t
ib_table_truncate.argtypes = [c_char_p, POINTER(ib_id_t)]

ib_table_get_id = libinnodb.ib_table_get_id
ib_table_get_id.restype = ib_err_t
ib_table_get_id.argtypes = [c_char_p, POINTER(ib_id_t)]

ib_index_get_id = libinnodb.ib_index_get_id
ib_index_get_id.restype = ib_err_t
ib_index_get_id.argtypes = [c_char_p, c_char_p, POINTER(ib_id_t)]

ib_database_create = libinnodb.ib_database_create
ib_database_create.restype = ib_bool_t
ib_database_create.argtypes = [c_char_p]

ib_database_drop = libinnodb.ib_database_drop
ib_database_drop.restype = ib_err_t
ib_database_drop.argtypes = [c_char_p]

ib_cursor_is_positioned = libinnodb.ib_cursor_is_positioned
ib_cursor_is_positioned.restype = ib_bool_t
ib_cursor_is_positioned.argtypes = [ib_crsr_t]

ib_schema_lock_shared = libinnodb.ib_schema_lock_shared
ib_schema_lock_shared.restype = ib_err_t
ib_schema_lock_shared.argtypes = [ib_trx_t]

ib_schema_lock_exclusive = libinnodb.ib_schema_lock_exclusive
ib_schema_lock_exclusive.restype = ib_err_t
ib_schema_lock_exclusive.argtypes = [ib_trx_t]

ib_schema_lock_is_exclusive = libinnodb.ib_schema_lock_is_exclusive
ib_schema_lock_is_exclusive.restype = ib_bool_t
ib_schema_lock_is_exclusive.argtypes = [ib_trx_t]

ib_schema_lock_is_shared = libinnodb.ib_schema_lock_is_shared
ib_schema_lock_is_shared.restype = ib_bool_t
ib_schema_lock_is_shared.argtypes = [ib_trx_t]

ib_schema_unlock = libinnodb.ib_schema_unlock
ib_schema_unlock.restype = ib_err_t
ib_schema_unlock.argtypes = [ib_trx_t]

ib_cursor_lock = libinnodb.ib_cursor_lock
ib_cursor_lock.restype = ib_err_t
ib_cursor_lock.argtypes = [ib_crsr_t, ib_lck_mode_t]

ib_table_lock = libinnodb.ib_table_lock
ib_table_lock.restype = ib_err_t
ib_table_lock.argtypes = [ib_trx_t, ib_id_t, ib_lck_mode_t]

ib_cursor_set_lock_mode = libinnodb.ib_cursor_set_lock_mode
ib_cursor_set_lock_mode.restype = ib_err_t
ib_cursor_set_lock_mode.argtypes = [ib_crsr_t, ib_lck_mode_t]

ib_cursor_set_cluster_access = libinnodb.ib_cursor_set_cluster_access
ib_cursor_set_cluster_access.restype = None
ib_cursor_set_cluster_access.argtypes = [ib_crsr_t]

ib_table_schema_visit = libinnodb.ib_table_schema_visit
ib_table_schema_visit.restype = ib_err_t
ib_table_schema_visit.argtypes = [ib_trx_t, c_char_p,
    POINTER(ib_schema_visitor_t), py_object]

ib_schema_tables_iterate = libinnodb.ib_schema_tables_iterate
ib_schema_tables_iterate.restype = ib_err_t
ib_schema_tables_iterate.argtypes = [ib_trx_t, ib_schema_visitor_table_all_t,
    py_object]

ib_cfg_var_get_type = libinnodb.ib_cfg_var_get_type
ib_cfg_var_get_type.restype = ib_err_t
ib_cfg_var_get_type.argtypes = [c_char_p, POINTER(ib_cfg_type_t)]

_ib_cfg_set = libinnodb.ib_cfg_set
_ib_cfg_set.restype = ib_err_t
def ib_cfg_set_int(name, v):
    return _ib_cfg_set(name, v)

def ib_cfg_set_bool(name, v):
    return _ib_cfg_set(name, v)

def ib_cfg_set_bool_on(name):
    return ib_cfg_set_bool(name, IB_TRUE)

def ib_cfg_set_bool_off(name):
    return ib_cfg_set_bool(name, IB_FALSE)

def ib_cfg_set_text(name, v):
    return _ib_cfg_set(name, v)

def ib_cfg_set_callback(name, v):
    return _ib_cfg_set(name, v)

ib_cfg_get = libinnodb.ib_cfg_get
ib_cfg_get.restype = ib_err_t
ib_cfg_get.argtypes = [c_char_p, c_void_p]

ib_cfg_get_all = libinnodb.ib_cfg_get_all
ib_cfg_get_all.restype = ib_err_t
ib_cfg_get_all.argtypes = [POINTER(POINTER(c_char_p)), POINTER(ib_u32_t)]

ib_savepoint_take = libinnodb.ib_savepoint_take
ib_savepoint_take.restype = None
ib_savepoint_take.argtypes = [ib_trx_t, c_void_p, ib_ulint_t]

ib_savepoint_release = libinnodb.ib_savepoint_release
ib_savepoint_release.restype = ib_err_t
ib_savepoint_release.argtypes = [ib_trx_t, c_void_p, ib_ulint_t]

ib_savepoint_rollback = libinnodb.ib_savepoint_rollback
ib_savepoint_rollback.restype = ib_err_t
ib_savepoint_rollback.argtypes = [ib_trx_t, c_void_p, ib_ulint_t]

ib_tuple_write_i8 = libinnodb.ib_tuple_write_i8
ib_tuple_write_i8.restype = ib_err_t
ib_tuple_write_i8.argtypes = [ib_tpl_t, c_int, ib_i8_t]

ib_tuple_write_i16 = libinnodb.ib_tuple_write_i16
ib_tuple_write_i16.restype = ib_err_t
ib_tuple_write_i16.argtypes = [ib_tpl_t, c_int, ib_i16_t]

ib_tuple_write_i32 = libinnodb.ib_tuple_write_i32
ib_tuple_write_i32.restype = ib_err_t
ib_tuple_write_i32.argtypes = [ib_tpl_t, c_int, ib_i32_t]

ib_tuple_write_i64 = libinnodb.ib_tuple_write_i64
ib_tuple_write_i64.restype = ib_err_t
ib_tuple_write_i64.argtypes = [ib_tpl_t, c_int, ib_i64_t]

ib_tuple_write_u8 = libinnodb.ib_tuple_write_u8
ib_tuple_write_u8.restype = ib_err_t
ib_tuple_write_u8.argtypes = [ib_tpl_t, c_int, ib_u8_t]

ib_tuple_write_u16 = libinnodb.ib_tuple_write_u16
ib_tuple_write_u16.restype = ib_err_t
ib_tuple_write_u16.argtypes = [ib_tpl_t, c_int, ib_u16_t]

ib_tuple_write_u32 = libinnodb.ib_tuple_write_u32
ib_tuple_write_u32.restype = ib_err_t
ib_tuple_write_u32.argtypes = [ib_tpl_t, c_int, ib_u32_t]

ib_tuple_write_u64 = libinnodb.ib_tuple_write_u64
ib_tuple_write_u64.restype = ib_err_t
ib_tuple_write_u64.argtypes = [ib_tpl_t, c_int, ib_u64_t]

ib_cursor_stmt_begin = libinnodb.ib_cursor_stmt_begin
ib_cursor_stmt_begin.restype = None
ib_cursor_stmt_begin.argtypes = [ib_crsr_t]

ib_tuple_write_double = libinnodb.ib_tuple_write_double
ib_tuple_write_double.restype = ib_err_t
ib_tuple_write_double.argtypes = [ib_tpl_t, c_int, c_double]

ib_tuple_read_double = libinnodb.ib_tuple_read_double
ib_tuple_read_double.restype = ib_err_t
ib_tuple_read_double.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(c_double)]

ib_tuple_write_float = libinnodb.ib_tuple_write_float
ib_tuple_write_float.restype = ib_err_t
ib_tuple_write_float.argtypes = [ib_tpl_t, c_int, c_float]

ib_tuple_read_float = libinnodb.ib_tuple_read_float
ib_tuple_read_float.restype = ib_err_t
ib_tuple_read_float.argtypes = [ib_tpl_t, ib_ulint_t, POINTER(c_float)]

#ib_logger_set = libinnodb.ib_logger_set
#ib_logger_set.restype = None
#ib_logger_set.argtypes = [ib_msg_log_t, ib_msg_stream_t]

def ib_logger_set(*atgs, **kw):
    raise NotImplementedError('No support for va_arg')

ib_strerror = libinnodb.ib_strerror
ib_strerror.restype = c_char_p
ib_strerror.argtypes = [ib_err_t]

ib_status_get_i64 = libinnodb.ib_status_get_i64
ib_status_get_i64.restype = ib_err_t
ib_status_get_i64.argtypes = [c_char_p, POINTER(ib_i64_t)]

