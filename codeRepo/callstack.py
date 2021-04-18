import enum


class ARType(enum.Enum):
    GLOBAL = 'GLOBAL'
    MODULE = 'MODULE'
    ROUTINE = 'ROUTINE'
    FUNCTION = 'FUNCTION'


class ActivationRecord:
    def __init__(self, name, type, nesting_level, enclosing_ar):
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.members = {}
        self._access_link = enclosing_ar

    def __setitem__(self, key, value):
        if key in self.members:
            self.members[key] = value
        elif self.type != ARType.GLOBAL:
            self.set_global_var(key, value)

    def __getitem__(self, key):
        if key in self.members:
            return self.members[key]
        else:
            return self.get_global_var(key)

    def get_global_var(self, key):
        return self.members[key] if self.type == ARType.GLOBAL else self._access_link.get_global_var(key)

    def set_global_var(self, key, value):
        if self.type == ARType.GLOBAL:
            self.members[key] = value
        else:
            self._access_link.set_global_var(key, value)

    def initialize_var(self, var_name, value):
        self.members[var_name] = value


    def get(self, key):
        return self.members.get(key)

    def __str__(self):
        lines = [
            '{level}: {type} {name}'.format(
                level=self.nesting_level,
                type=self.type.value,
                name=self.name,
            )
        ]
        for name, val in self.members.items():
            lines.append(f'   {name:<20}: {val}')

        s = '\n'.join(lines)
        return s

    def __repr__(self):
        return self.__str__()


class Callstack:
    def __init__(self):
        self._records = []
        scope_name = "GLOBAL"
        self.global_record = ActivationRecord(name=scope_name, type=ARType.GLOBAL, nesting_level=1, enclosing_ar=None)
        self._add_system_variables()
        self.push(self.global_record)

    def push(self, ar):
        self._records.append(ar)

    def pop(self):
        return self._records.pop()

    def peek(self):
        return self._records[-1]

    def peek_global(self):
        return self.global_record

    def _add_system_variables(self):
        self.global_record.initialize_var("$IN", bytearray(8192+1))
        self.global_record.initialize_var("$OUT", bytearray(8192+1))

    def __str__(self):
        s = '\n'.join(repr(ar) for ar in reversed(self._records))
        s = f'CALL STACK\n{s}\n'
        return s

    def __repr__(self):
        return self.__str__()