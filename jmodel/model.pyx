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


cdef inline size_t skip_whitespace(const char * s, size_t idx):
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


cdef parse_object(char *s, int idx, size_t len):
    pairs = {}
    idx = skip_whitespace(s, idx)
    if s[idx] == '}':
        return {}, idx + 1
    elif s[idx] != '"':
        raise Exception(
            "Expecting property name enclosed in double quotes", s, idx)
    while True:
        idx += 1
        key, idx = scanstring(s, idx, len)
        idx = skip_whitespace(s, idx)
        if s[idx] != ':':
            raise Exception("Expecting ':' delimiter", s, idx)

        idx = skip_whitespace(s, idx + 1)

        try:
            value, idx = scan_once(s, idx, len)
        except StopIteration as err:
            raise Exception("Expecting value", s, err.value)

        pairs[key] = value

        idx = skip_whitespace(s, idx)

        if s[idx] == '}':
            break
        elif s[idx] != ',':
            raise Exception("Expecting ',' delimiter. Found ", s, idx - 1, s[idx])
        idx = skip_whitespace(s, idx + 1)
        if s[idx] != '"':
            raise Exception(
                "Expecting property name enclosed in double quotes", s, idx - 1, s[idx])
    return pairs, idx + 1

cdef parse_array(char * s, int idx, size_t len):
    cdef char nextchar
    values = []
    idx = skip_whitespace(s, idx)
    # Look-ahead for trivial empty array
    if s[idx] == ']':
        return values, idx + 1

    while True:
        try:
            value, idx = scan_once(s, idx, len)
        except StopIteration as err:
            raise Exception("Expecting value", s, err.value) from None
        values.append(value)
        idx = skip_whitespace(s, idx)
        if s[idx] == ']':
            break
        elif s[idx] != ',':
            raise Exception("Expecting ',' delimiter", s, idx - 1)

        idx = skip_whitespace(s, idx+1)

    return values, idx + 1

cdef scan_once(char *s,size_t idx, size_t len):
    cdef char nextchar

    if idx == len:
        raise StopIteration(idx)

    nextchar = s[idx]

    if nextchar == '"':
        return scanstring(s, idx + 1, len)
    elif nextchar == '{':
        return parse_object(s, idx + 1, len)
    elif nextchar == '[':
        return parse_array(s, idx + 1, len)
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

class Model(dict):

    @classmethod
    def loads(cls, s):
        b = s.encode()
        return scan_once(b, 0, len(b))
