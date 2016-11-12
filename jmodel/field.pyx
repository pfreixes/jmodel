cdef class Field:

    cdef public int required

    def __init__(self, required=True):
        self.required = required
