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
tuple_clear = libinnodb.ib_tuple_clear
tuple_delete = libinnodb.ib_tuple_delete
tuple_get_n_cols = libinnodb.ib_tuple_get_n_cols
col_get_value = libinnodb.ib_col_get_value
sec_search_tuple_create = libinnodb.ib_sec_search_tuple_create
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

