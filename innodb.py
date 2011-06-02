import ctypes
import libinnodb

class InnoDBError(Exception):
    def __init__(self, error_code):
        self._error_code = error_code
        super(InnoDBError, self).__init__('%s (%s)',
            libinnodb.db_err(error_code), error_code)

    def getErrorCode(self):
        return self._error_code

def api_version():
    """Return a 3-tupple with InnoDB lib API version."""
    vernum = libinnodb.ib_api_version()
    return (vernum >> 32, (vernum >> 16) & 0xffff, vernum & 0xffff)

trx_begin = libinnodb.ib_trx_begin
table_schema_delete = libinnodb.ib_table_schema_delete
clust_read_tuple_create = libinnodb.ib_clust_read_tuple_create
clust_search_tuple_create = libinnodb.ib_clust_search_tuple_create
sec_read_tuple_create = libinnodb.ib_sec_read_tuple_create
sec_search_tuple_create = libinnodb.ib_sec_search_tuple_create
tuple_clear = libinnodb.ib_tuple_clear
tuple_delete = libinnodb.ib_tuple_delete
tuple_get_n_cols = libinnodb.ib_tuple_get_n_cols
col_get_value = libinnodb.ib_col_get_value
def database_create(name):
    if not libinnodb.ib_database_create(name):
        raise InnoDBError(libinnodb.DB_ERROR)

cfg_set_int = libinnodb.ib_cfg_set_int
cfg_set_bool_on = libinnodb.ib_cfg_set_bool_on
cfg_set_bool_off = libinnodb.ib_cfg_set_bool_off
cfg_set_text = libinnodb.ib_cfg_set_text
cfg_set_callback = libinnodb.ib_cfg_set_callback

def col_get_meta(tpl, i):
    meta = libinnodb.ib_col_meta_t()
    res = libinnodb.ib_col_get_meta(tpl, i, ctypes.byref(meta))
    return res, meta

def new_wrapper(func):
    def wrapped(*args, **kw):
        res = func(*args, **kw).value
        if res != DB_SUCCESS:
            raise InnoDBError(res)
    return wrapped

ib_err_t = libinnodb.ib_err_t
DB_SUCCESS = libinnodb.DB_SUCCESS
_global_dict = globals()
for func_name in dir(libinnodb):
    if not func_name.startswith('ib_'):
        continue
    dest_func_name = func_name[3:]
    if dest_func_name in _global_dict:
        continue
    func = getattr(libinnodb, func_name)
    if getattr(func, 'restype', None) is not ib_err_t:
        continue
    _global_dict[dest_func_name] = new_wrapper(func)

_wrapped_tuple_read_float = tuple_read_float
def tuple_read_float(tpl, i):
    v = ctypes.c_float()
    _wrapped_tuple_read_float(tpl, i, ctypes.byref(v))
    return v.value

_wrapped_tuple_read_double = tuple_read_double
def tuple_read_double(tpl, i):
    v = ctypes.c_double()
    _wrapped_tuple_read_double(tpl, i, ctypes.byref(v))
    return v.value

_wrapped_tuple_read_u8 = tuple_read_u8
def tuple_read_u8(tpl, i):
    v = libinnodb.ib_u8_t()
    _wrapped_tuple_read_u8(tpl, i, ctypes.byref(v))
    return v.value

_wrapped_tuple_read_i8 = tuple_read_i8
def tuple_read_i8(tpl, i):
    v = libinnodb.ib_i8_t()
    _wrapped_tuple_read_i8(tpl, i, ctypes.byref(v))
    return v.value

_wrapped_tuple_read_u16 = tuple_read_u16
def tuple_read_u16(tpl, i):
    v = libinnodb.ib_u16_t()
    _wrapped_tuple_read_u16(tpl, i, ctypes.byref(v))
    return v.value

_wrapped_tuple_read_i16 = tuple_read_i16
def tuple_read_i16(tpl, i):
    v = libinnodb.ib_i16_t()
    _wrapped_tuple_read_i16(tpl, i, ctypes.byref(v))
    return v.value

_wrapped_tuple_read_u32 = tuple_read_u32
def tuple_read_u32(tpl, i):
    v = libinnodb.ib_u32_t()
    _wrapped_tuple_read_u32(tpl, i, ctypes.byref(v))
    return v.value

_wrapped_tuple_read_i32 = tuple_read_i32
def tuple_read_i32(tpl, i):
    v = libinnodb.ib_i32_t()
    _wrapped_tuple_read_i32(tpl, i, ctypes.byref(v))
    return v.value

_wrapped_tuple_read_u64 = tuple_read_u64
def tuple_read_u64(tpl, i):
    v = libinnodb.ib_u64_t()
    _wrapped_tuple_read_u64(tpl, i, ctypes.byref(v))
    return v.value

_wrapped_tuple_read_i64 = tuple_read_i64
def tuple_read_i64(tpl, i):
    v = libinnodb.ib_i64_t()
    _wrapped_tuple_read_i64(tpl, i, ctypes.byref(v))
    return v.value

# WIP: python-ish classes
# This *will* change a lot. Don't rely on its current form.
# TODO: thread-safe
# TODO: cstring-safe

def _checkName(name):
    if '/' in name or '\0' in name or \
            len(name) > libinnodb.IB_MAX_TABLE_NAME_LEN:
        raise ValueError('Invalid name: %r' % (name, ))

_is_initialised = False
_is_started = False

class InnoDB(object):
    def __init__(self):
        global _is_initialised
        if not _is_initialised:
            init()
            _is_initialised = True

    def startup(self, version='antelope'):
        global _is_started
        startup(version)
        _is_started = True

    def shutdown(self, mode=libinnodb.IB_SHUTDOWN_NORMAL):
        global _is_started
        shutdown(mode)
        _is_started = False

    def __getitem__(self, name):
        _checkName(name)
        return Database(name)

class Database(object):
    """
    Represents a database.

    This class doesn't do much, it merely saves user from having to specify
    database name over and over.
    """
    def __init__(self, name):
        self._name = name

    def create(self):
        """
        Creates database if it doesn't exist.
        """
        database_create(self._name)

    def drop(sef):
        """
        Delete current database (and all contained tables).
        """
        database_drop(self._name)
        # TODO: notify table insances of their removal ?

    def __getitem__(self, name):
        _checkName(name)
        return Table('%s/%s' % (self._name, name))

class Table(object):
    def __init__(self, name):
        self._name = name

    def drop(self, transaction):
        table_drop(transaction._txn_id, self._name)

    def truncate(self):
        table_id = libinnodb.ib_id_t()
        table_truncate(self._name, ctypes.byref(table_id))
        # TODO: notify cursor instances of table truncation ?

    def open(self, transaction):
        return TableCursor(self._name, transaction)

    def newSchema(self, fmt=libinnodb.IB_TBL_COMPACT, page_size=0,
            column_list=()):
        sch = TableSchema(self._name, fmt, page_size)
        for column_args in column_list:
            sch.addColumn(*column_args)
        return sch

class Transaction(object):
    _txn_id = None

    def __init__(self, level):
        self._level = level

    def begin(self):
        txn_id = trx_begin(self._level)
        if not txn_id:
            raise ValueError('Could not begin transaction')
        self._txn_id = txn_id

    def start(self):
        trx_start(self._txn_id, self._level)

    def getState(self):
        if self._txn_id is None:
            raise ValueError('Transaction already released.')
        return libinnodb.ib_trx_state(self._txn_id)

    def release(self):
        trx_release(self._txn_id)
        self._txn_id = None

    def commit(self):
        trx_commit(self._txn_id)
        self._txn_id = None

    def rollback(self):
        trx_rollback(self._txn_id)
        self._txn_id = None

    def lockSchema(self, exclusive=False):
        if exclusive:
            schema_lock_exclusive(self._txn_id)
        else:
            schema_lock_shared(self._txn_id)

    def __del__(self):
        if _is_started and self._txn_id is not None:
            if self.getState() == libinnodb.IB_TRX_NOT_STARTED:
                self.release()
            else:
                self.rollback()

class TableSchema(object):
    def __init__(self, name, fmt=libinnodb.IB_TBL_COMPACT, page_size=0):
        self._schema = schema = libinnodb.ib_tbl_sch_t()
        self._index_list = []
        table_schema_create(name, ctypes.byref(schema), fmt, page_size)

    def create(self, transaction):
        table_id = libinnodb.ib_id_t()
        table_create(transaction._txn_id, self._schema, ctypes.byref(table_id))

    def addColumn(self, name, col_type, length,
            attributes=libinnodb.IB_COL_NONE, client=0):
        table_schema_add_col(self._schema, name, col_type, attributes, client,
            length)

    def newIndex(self, name, column_list=(), clustered=False):
        index_schema_id = libinnodb.ib_idx_sch_t()
        table_schema_add_index(self._schema, name,
            ctypes.byref(index_schema_id))
        self._index_list.append(index_schema_id)
        index_schema = IndexSchema(index_schema_id)
        for column_args in column_list:
            index_schema.addColumn(*column_args)
        if clustered:
            index_schema.setClustered()
        return index_schema

    def __del__(self):
        if _is_started and self._schema:
            table_schema_delete(self._schema)

class IndexSchema(object):
    def __init__(self, index_schema_id):
        self._schema = index_schema_id

    def addColumn(self, name, prefix=0):
        index_schema_add_col(self._schema, name, prefix)

    def setClustered(self):
        index_schema_set_clustered(self._schema)

class BaseCursor(object):
    def __init__(self):
        raise NotImplementedError()

    def getReadTuple(self):
        raise NotImplementedError()

    def getSearchTuple(self):
        raise NotImplementedError()

    def lockTable(self, mode):
        cursor_lock(self._cursor, mode)

    def setLockMode(self, mode):
        cursor_set_lock_mode(self._cursor, mode)

    def read(self, tpl):
        cursor_read_row(self._cursor, tpl._tuple)
        tpl._update()

    def goFirst(self):
        cursor_first(self._cursor)

    def goNext(self):
        cursor_next(self._cursor)

    def goPrev(self):
        cursor_prev(self._cursor)

    def goLast(self):
        cursor_last(self._cursor)

    def goTo(self, tpl, search_mode=libinnodb.IB_CUR_GE):
        res = ctypes.c_int()
        cursor_moveto(self._cursor, tpl._tuple, search_mode, ctypes.byref(res))
        return res.value

    def _iter(self, tpl, go):
        while True:
            try:
                self.read(tpl)
            except InnoDBError, exc:
                if exc.getErrorCode() in (
                            libinnodb.DB_END_OF_INDEX,
                            libinnodb.DB_RECORD_NOT_FOUND,
                        ):
                    break
                raise
            yield tpl
            tpl.clear()
            try:
                go()
            except InnoDBError, exc:
                if exc.getErrorCode() in (
                            libinnodb.DB_END_OF_INDEX,
                            libinnodb.DB_RECORD_NOT_FOUND,
                        ):
                    break
                raise

    def iterForward(self):
        return self._iter(self.getReadTuple(), self.goNext)

    def iterBackward(self):
        return self._iter(self.getReadTuple(), self.goPrev)

    def isPositioned(self):
        return bool(cursor_is_positioned(self._cursor))

    def reset(self):
        cursor_reset(self._cursor)

    def close(self):
        cursor_close(self._cursor)

    def __del__(self):
        if _is_started and self._cursor:
            self.close()

class TableCursor(BaseCursor):
    def __init__(self, table, transaction):
        self._table = table
        self._cursor = cursor = libinnodb.ib_crsr_t()
        cursor_open_table(table, transaction._txn_id,
            ctypes.byref(cursor))

    def getReadTuple(self):
        return ClusterReadTuple(self._cursor)

    def getSearchTuple(self):
        return ClusterSearchTuple(self._cursor)

    def insert(self, tpl):
        cursor_insert_row(self._cursor, tpl._tuple)

    def insertRows(self, row_list):
        tpl = self.getReadTuple()
        for row in row_list:
            for column_number, value in enumerate(row):
                tpl[column_number] = value
            self.insert(tpl)
            tpl.clear()

    def update(self, old, new):
        cursor_update_row(self._cursor, old._tuple, new._tuple)

    def delete(self):
        cursor_delete_row(self._cursor)

_read_int = {
    (1, libinnodb.IB_COL_UNSIGNED): tuple_read_u8,
    (1, libinnodb.IB_COL_NONE): tuple_read_i8,
    (2, libinnodb.IB_COL_UNSIGNED): tuple_read_u16,
    (2, libinnodb.IB_COL_NONE): tuple_read_i16,
    (4, libinnodb.IB_COL_UNSIGNED): tuple_read_u32,
    (4, libinnodb.IB_COL_NONE): tuple_read_i32,
    (8, libinnodb.IB_COL_UNSIGNED): tuple_read_u64,
    (8, libinnodb.IB_COL_NONE): tuple_read_i64,
}

_write_int = {
    (1, libinnodb.IB_COL_UNSIGNED): tuple_write_u8,
    (1, libinnodb.IB_COL_NONE): tuple_write_i8,
    (2, libinnodb.IB_COL_UNSIGNED): tuple_write_u16,
    (2, libinnodb.IB_COL_NONE): tuple_write_i16,
    (4, libinnodb.IB_COL_UNSIGNED): tuple_write_u32,
    (4, libinnodb.IB_COL_NONE): tuple_write_i32,
    (8, libinnodb.IB_COL_UNSIGNED): tuple_write_u64,
    (8, libinnodb.IB_COL_NONE): tuple_write_i64,
}

class BaseTuple(object):
    _tuple = None

    def __init__(self, tpl):
        if not tpl:
            raise ValueError('Could not instanciate tuple')
        self._tuple = tpl
        self._update()

    def _update(self):
        self._col_data_list = col_data_list = []
        col_data_append = col_data_list.append
        for index in xrange(libinnodb.ib_tuple_get_n_cols(self._tuple)):
            data_len, col_meta = col_get_meta(self._tuple, index)
            if col_meta.type == libinnodb.IB_SYS:
                continue
            col_data_append((index, data_len, col_meta))
        self._len = len(col_data_list)

    def clear(self):
        new_tuple = tuple_clear(self._tuple)
        if not new_tuple:
            raise ValueError('Out of memory ?')
        self._tuple = new_tuple

    def copy(self, src):
        tuple_copy(self._tuple, src._tuple)

    def __getitem__(self, index):
        index, data_len, col_meta = self._col_data_list[index]
        col_type = col_meta.type
        if data_len == libinnodb.IB_SQL_NULL:
            result = None
        elif col_type == libinnodb.IB_INT:
            result = _read_int[col_meta.type_len,
                col_meta.attr & libinnodb.IB_COL_UNSIGNED](
                self._tuple, index)
        elif col_type == libinnodb.IB_FLOAT:
            result = tuple_read_float(self._tuple, index)
        elif col_type == libinnodb.IB_DOUBLE:
            result = innodb.tuple_read_double(self._tuple, index)
        elif col_type in (libinnodb.IB_CHAR, libinnodb.IB_BLOB,
                libinnodb.IB_DECIMAL, libinnodb.IB_VARCHAR):
            result = ctypes.string_at(col_get_value(
                self._tuple, index), data_len)
        else:
            raise NotImplementedError(repr(col_type))
        return result

    def __setitem__(self, index, value):
        index, data_len, col_meta = self._col_data_list[index]
        col_type = col_meta.type
        if value is None:
            col_set_value(self._tuple, index, None, IB_SQL_NULL)
        elif col_type == libinnodb.IB_INT:
            _write_int[col_meta.type_len,
                col_meta.attr & libinnodb.IB_COL_UNSIGNED](
                self._tuple, index, value)
        elif col_type == libinnodb.IB_FLOAT:
            tuple_write_float(self._tuple, index, value)
        elif col_type == libinnodb.IB_DOUBLE:
            innodb.tuple_value_double(self._tuple, index, value)
        elif col_type in (libinnodb.IB_CHAR, libinnodb.IB_BLOB,
                libinnodb.IB_DECIMAL, libinnodb.IB_VARCHAR):
            col_set_value(self._tuple, index, value, len(value))
        else:
            raise NotImplementedError(repr(col_type))
        self._update()

    def __len__(self):
        return self._len

    def __del__(self):
        if _is_started and self._tuple:
            libinnodb.ib_tuple_delete(self._tuple)

class ClusterReadTuple(BaseTuple):
    def __init__(self, cursor):
        super(ClusterReadTuple, self).__init__(
            clust_read_tuple_create(cursor))

class ClusterSearchTuple(BaseTuple):
    def __init__(self, cursor):
        super(ClusterSearchTuple, self).__init__(
            clust_search_tuple_create(cursor))

class SecondaryReadTuple(BaseTuple):
    def __init__(self, cursor):
        super(SecondaryReadTuple, self).__init__(
            sec_read_tuple_create(cursor))

class SecondarySearchTuple(BaseTuple):
    def __init__(self, cursor):
        super(SecondarySearchTuple, self).__init__(
            sec_search_tuple_create(cursor))

