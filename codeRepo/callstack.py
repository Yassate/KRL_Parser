import enum
from kuka_datatypes import E6Pos, E6Axis


class ARType(enum.Enum):
    GLOBAL = 'GLOBAL'
    MODULE = 'MODULE'
    ROUTINE = 'ROUTINE'
    FUNCTION = 'FUNCTION'


class ActivationRecord:
    def __init__(self, name=None, type_=None, nesting_level=0, enclosing_ar=None):
        self.name = name
        self.type_ = type_
        self.nesting_level = nesting_level
        self.members = {}
        self._access_link = enclosing_ar

    def __setitem__(self, input_var_name, value):
        input_var_name = input_var_name.lower()
        var_name, indices = self._split_var_name(input_var_name)

        if var_name in self.members:
            if indices:
                current_variable = self.members[var_name]
                indices_count = len(indices)
                for i in range(0, indices_count - 1):
                    current_variable = current_variable[indices[i]]
                current_variable[indices[indices_count - 1]] = value
            else:
                self.members[var_name] = value
        else:
            self.set_global_var(var_name, value)
            return

    def __getitem__(self, input_var_name):
        input_var_name = input_var_name.lower()
        var_name, indices = self._split_var_name(input_var_name)
        current_value = self.members[var_name] if var_name in self.members else self.get_global_var(var_name)
        if indices:
            call_option = len(indices) - 1
            value = [
                lambda index: current_value[index[0]],
                lambda index: current_value[index[0]][index[1]],
                lambda index: current_value[index[0]][index[1]][index[2]]]
            current_value = value[call_option](indices)
        return current_value

    # noinspection PyMethodMayBeStatic
    def _split_var_name(self, input_var_name: str):
        if input_var_name.endswith(']'):
            splitted = input_var_name[:-1].split('[')
            var_name, indices = splitted[0], list(map(int, splitted[1].split(',')))
        else:
            var_name, indices = input_var_name, None
        return var_name, indices

    def get_global_var(self, key):
        key = key.lower()
        return self.members[key] if self.type_ == ARType.GLOBAL else self._access_link[key]

    # TODO >> Add existence check
    def set_global_var(self, key, value):
        key = key.lower()
        if self.type_ == ARType.GLOBAL:
            self.members[key] = value
        else:
            self._access_link[key] = value

    def initialize_var(self, var_name, value):
        var_name = var_name.lower()
        self.members[var_name] = value

    def get(self, key):
        return self.members.get(key)

    def __str__(self):
        lines = [
            '{level}: {type} {name}'.format(
                level=self.nesting_level,
                type=self.type_.value,
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
        global_record = ActivationRecord(name=scope_name, type_=ARType.GLOBAL, nesting_level=1, enclosing_ar=None)
        self.push(global_record)
        self._add_system_variables()

    def push(self, ar):
        self._records.append(ar)

    def pop(self):
        return self._records.pop()

    def peek(self):
        return self._records[-1]

    def _add_system_variables(self):
        global_record = self.peek()
        global_record.initialize_var("$in", bytearray(8192+1))
        global_record.initialize_var("$out", bytearray(8192+1))
        global_record.initialize_var("$axis_act", E6Axis([0, -90, 90, 0, 0, 0]))
        global_record.initialize_var("$pos_act", E6Pos.from_tuples(xyz=(0, 0, 0), abc=(0, 0, 0), S=0, T=0))

    def __str__(self):
        s = '\n'.join(repr(ar) for ar in reversed(self._records))
        s = f'CALL STACK\n{s}\n'
        return s

    def __repr__(self):
        return self.__str__()
