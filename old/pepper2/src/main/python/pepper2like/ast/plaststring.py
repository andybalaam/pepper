from pepper2like.type_check import type_check


class plAstString:
    def __init__(self, value):
        type_check(str, value)
        self.value = value
