class SymbolTable:
    def __init__(self) -> None:
        self.reserved = {"while", "if", "Int", "String", "println", "readline"}
        self.symbols = {}

    def create(self, identifier, type):
        if identifier in self.symbols:
            raise NameError(f"name '{identifier}' already exist")
        if type == "INT":
            self.symbols[identifier] = (int, 0)
            return
        if type == "STR":
            self.symbols[identifier] = (str, "")
            return
        raise NameError(f"type '{type}' doesn't exist")

    def getter(self, identifier) -> int:
        if identifier in self.symbols:
            return self.symbols[identifier]
        raise NameError(f"name '{identifier}' is not defined")

    def setter(self, identifier, value) -> None:
        if self.symbols[identifier][0] != value[0]:
            raise TypeError(f"variable type diff from '{value[0]}'")
        self.symbols[identifier] = (
            self.symbols[identifier][0],
            value[1],
        )