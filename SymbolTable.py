class SymbolTable:
    symbols = {}

    @staticmethod
    def getter(identifier) -> int:
        if identifier in SymbolTable.symbols:
            return SymbolTable.symbols[identifier]
        raise NameError(f"name '{identifier}' is not defined")

    @staticmethod
    def setter(identifier, value) -> None:
        if identifier not in SymbolTable.symbols:
            raise NameError(f"name '{identifier}' don't exist")
        SymbolTable.symbols[identifier] = value
        return

    @staticmethod
    def create(identifier) -> None:
        if identifier in SymbolTable.symbols:
            raise NameError(f"name '{identifier}' already exist")
        SymbolTable.symbols[identifier] = 0
