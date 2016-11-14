class DecodeError(Exception):
    """
    Exception raised when is decoded an invalid JSON object. Human readable
    message can be found in the `msg` attribute, meanwhile the character
    where the error was occurred can be found through the `offset` attribute.
    """
    def __init__(self, msg, s, offset):
        self.msg = msg
        self.s = s
        self.offset = offset

    def __str__(self):
        return "{}\n `{}`\n..^..".format(
                self.msg,
                self.s[self.offset-3:self.offset+13])
