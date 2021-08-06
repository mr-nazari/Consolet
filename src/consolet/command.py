import sys
from typing import Any

# Special Words
NOT_FOUND_WORD = '|no|'
TYPE_WORD = '|type|'
SELF_ARG_WORD = '|self|'


class CommandParser:
    def __init__(
            self,
            argv: list,
            config: dict,
            if_not_found: Any,
            value_type: Any,
            self_arg: Any = None,
            parent: Any = None,
            is_use_parent_options: bool = False,
            results=None
    ):
        self.argv = argv
        self.config = config

        self.if_not_found = if_not_found
        self.value_type = value_type
        self.self_arg = self_arg
        self.is_use_parent_options = is_use_parent_options

        self.parent = parent

        self.results = results

    def parse_to_dict(self, is_save_results: bool = True):
        results = dict()

        if self.is_use_parent_options:
            self.if_not_found, self.value_type, self.self_arg = self.config.get(NOT_FOUND_WORD, self.if_not_found), \
                                                                self.config.get(TYPE_WORD, self.value_type), \
                                                                self.config.get(SELF_ARG_WORD, self.self_arg)

        self_arg_value = None
        if self.parent is not None:
            try:
                # TODO: detect range of parameters
                parent_index = self.argv.index(self.parent)
                self_arg_value = self.argv[parent_index + 1]
                self.argv = self.argv[parent_index + 1:]
            except:
                return
        else:
            try:
                self_arg_value = self.argv[0]
            except IndexError:
                pass

        if self_arg_value is not None:
            if self_arg_value not in self.config.keys():
                results[SELF_ARG_WORD] = self.value_type(self_arg_value)
            else:
                results[SELF_ARG_WORD] = self.self_arg

        for key, value in self.config.items():
            if type(value) is dict:
                results[key] = CommandParser(self.argv, value, self.if_not_found, self.value_type, self.self_arg,
                                             parent=key,
                                             is_use_parent_options=self.is_use_parent_options).parse_to_dict()
            elif key not in [NOT_FOUND_WORD, TYPE_WORD, SELF_ARG_WORD]:
                if key in self.argv:
                    try:
                        param_value = self.argv[self.argv.index(key) + 1]
                        if param_value not in self.config.keys():
                            results[key] = self.value_type(
                                param_value
                            )
                        else:
                            results[key] = value
                    except:
                        results[key] = value
                else:
                    results[key] = self.if_not_found
            else:
                {
                    NOT_FOUND_WORD: lambda: globals().__setitem__(self.if_not_found, value),
                    TYPE_WORD: lambda: globals().__setitem__(self.value_type, value),
                    SELF_ARG_WORD: lambda: globals().__setitem__(self.self_arg, value)
                }.get(key)()

        if is_save_results:
            self.results = results
        return results

    def get_item(self, *args, is_run_func: bool = False, func_args=None):
        if func_args is None:
            func_args = []
        try:
            res = self.results
            for i in args:
                res = res[i]
            if is_run_func:
                return res(*func_args)
            return res
        except:
            return None


def command(config: dict, is_save_results: bool = False, if_not_found: Any = False, value_type: Any = str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            argv = sys.argv[1:]
            command_ = CommandParser(argv, config, if_not_found, value_type)
            if is_save_results:
                command_.parse_to_dict(is_save_results)
            return func(command_, *args, **kwargs)

        return wrapper

    return decorator
