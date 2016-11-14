import inspect

from .fields import Field
from .exceptions import DecodeError

NaN = float('nan')
PosInf = float('inf')
NegInf = float('-inf')

_CONSTANTS = {
    '-Infinity': NegInf,
    'Infinity': PosInf,
    'NaN': NaN,
}


def parse_constant(value):
    _CONSTANTS = {
        '-Infinity': NegInf,
        'Infinity': PosInf,
        'NaN': NaN,
    }
    return _CONSTANTS.get(value)


cdef inline int is_number(char c):
    return c == '-' or c == '0' or c == '1' or c == '2' or\
        c == '3' or c == '4' or c == '5' or c == '6' or\
        c == '7' or c == '8' or c == '9'


cdef inline int is_whitespace(char c):
    return c == ' ' or c == '\t' or c == '\n' or c == '\r'


cdef inline size_t __skip_whitespaces(const char * s, size_t idx):
    while True:
        if not is_whitespace(s[idx]):
            break
        idx+=1
    return idx


cdef scanstring(const char *s, size_t idx, size_t len):

    cdef size_t begin = idx
    cdef size_t next = idx
    cdef char c = 0

    try:
        while True:
            while (s[next] != '"') and (s[next] != '\\'):
                next+=1
            if s[next] == '"':
                break
            # got the following character after the escaped one
            next+=2
        return s[idx:next].decode(), next+1
    except IndexError:
        raise Exception("Unterminated string starting at", s.decode(), next)


cdef scannumber(const char *s, size_t idx, size_t len):

    cdef int float_ = 0
    cdef size_t next = idx

    try:
        while True:
            while is_number(s[next]):
                next+=1

            if s[next] != '.':
                break

            if float_ == 1:
                raise Exception("Invalid number format ", s, idx)

            float_ = 1
            next+=1

        return s[idx:next].decode(), next, float_
    except IndexError:
        raise Exception("Unterminated string starting at", s.decode(), next)


cdef __decode_object(cls, char *s, int idx, size_t len, dict fields_cache={}):

    try:
        fields, fields_required = fields_cache[cls.__name__]
    except KeyError:
        fields = cls.fields()
        fields_required = set([name for name, field in fields if field.required])
        fields_cache[cls.__name__] = (fields, fields_required)

    pairs = {}
    idx = __skip_whitespaces(s, idx)
    if s[idx] == '}':
        return {}, idx + 1
    elif s[idx] != '"':
        raise Exception(
            "Expecting property name enclosed in double quotes", s, idx)
    while True:
        idx += 1
        key, idx = scanstring(s, idx, len)
        idx = __skip_whitespaces(s, idx)
        if s[idx] != ':':
            raise Exception("Expecting ':' delimiter", s, idx)

        idx = __skip_whitespaces(s, idx + 1)

        try:
            value, idx = __scan_once(cls, s, idx, len, fields_cache=fields_cache)
        except StopIteration as err:
            raise Exception("Expecting value", s, err.value)

        pairs[key] = value

        idx = __skip_whitespaces(s, idx)

        if s[idx] == '}':
            break
        elif s[idx] != ',':
            raise Exception("Expecting ',' delimiter. Found ", s, idx - 1, s[idx])
        idx = __skip_whitespaces(s, idx + 1)
        if s[idx] != '"':
            raise Exception(
                "Expecting property name enclosed in double quotes", s, idx - 1, s[idx])
    return pairs, idx + 1

cdef __decode_list(cls, char * s, int idx, size_t len, dict fields_cache={}):
    cdef char nextchar
    values = []
    idx = __skip_whitespaces(s, idx)
    # Look-ahead for trivial empty array
    if s[idx] == ']':
        return values, idx + 1

    while True:
        try:
            value, idx = __scan_once(cls, s, idx, len, fields_cache=fields_cache)
        except StopIteration as err:
            raise Exception("Expecting value", s, err.value) from None
        values.append(value)
        idx = __skip_whitespaces(s, idx)
        if s[idx] == ']':
            break
        elif s[idx] != ',':
            raise Exception("Expecting ',' delimiter", s, idx - 1)

        idx = __skip_whitespaces(s, idx+1)

    return values, idx + 1

cdef __scan_once(cls, char *s,size_t idx, size_t len, dict fields_cache={}):
    cdef char nextchar

    if idx == len:
        raise StopIteration(idx)

    nextchar = s[idx]

    if nextchar == '"':
        return scanstring(s, idx + 1, len)
    elif nextchar == '{':
        return __decode_object(cls, s, idx + 1, len, fields_cache=fields_cache)
    elif nextchar == '[':
        return __decode_list(cls, s, idx + 1, len, fields_cache=fields_cache)
    elif s[idx:idx+4] == b"null":
        return None, idx + 4
    elif s[idx:idx+4] == b"true":
        return True, idx + 4
    elif s[idx:idx+5] == b"false":
        return False, idx + 5
    elif is_number(nextchar):
        value, idx, float_ = scannumber(s, idx, len)
        if float_:
            res = float(value)
        else:
            res = int(value)
        return res, idx
    elif s[idx:idx + 3] == b'NaN':
        return parse_constant('NaN'), idx + 3
    else:
        raise StopIteration(idx)

class Model:

    @classmethod
    def loads(cls, s, many=False):
        """
        Decode the JSON `s` payload and build the model defined by the `cls` parameter.

        :param cls: :class:`jmodel.model.Model` class or derivated one that defines the fields
                     and their types expected.
        :param s: str.
        :param many: bool, default False. Use True to decode a list of `cls` JSON objects.
        :returns :class:`jmodel.model.Model`: An instance of the `cls` given as a parameter.

        :raises :class:`jmodel.exception.DecodeError`: When JSON object is not well formed.
        """
        if not s or len(s) == 0:
            raise DecodeError("Empty buffer", s, 0)

        b = s.encode()

        try:
            idx = __skip_whitespaces(b, 0)
            if many and b[idx:idx+1] == b"[":
                return __decode_list(cls, b, idx+1, len(b))
            elif not many and b[idx:idx+1] == b"{":
                return __decode_object(cls, b, idx+1, len(b))
            else:
                raise DecodeError("Invalid start char", b, idx)
        except IndexError:
            raise DecodeError("Invalid payload", b, idx)

    @classmethod
    def fields(cls):
        """
        Returns a dictionary with the :class:`jmodule.field.Field` derivated instances attached to the
        `cls`.

        :returns dict: key, value as name of the field and its instance.
        """
        return {
            name:instance for name, instance in cls.__dict__.items() if isinstance(instance, Field)}

