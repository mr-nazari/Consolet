import sys
from typing import Any

"""
# For Example

python file.py startproject --name hello-world

@command({
    'startproject': {
        '|default|': 10,
        '|no|': None,
        '|type|': int,
        '|this|: None,
        '--name': None,
        'info': {
            '--version': None,
            '--description': None,
        }
    },
    'say-hello': None
})
"""

# Special Words
NOT_FOUND_WORD = '|no|'
TYPE_WORD = '|type|'
THIS_ARG_WORD = '|this|'


class CommandParser:
    def __init__(
            self,
            argv: list,
            config: dict,
            if_not_found: Any,
            value_type: Any,
            parent: Any = None,
            is_use_parent_options: bool = False,
            results=None
    ):
        self.argv = argv
        self.config = config

        self.if_not_found = if_not_found
        self.value_type = value_type
        self.is_use_parent_options = is_use_parent_options

        self.parent = parent

        self.results = results

    def parse_to_dict(self, is_save_results: bool = True):
        results = dict()

        if self.is_use_parent_options:
            self.if_not_found, self.value_type = self.config.get(NOT_FOUND_WORD, self.if_not_found), \
                                                 self.config.get(TYPE_WORD, self.value_type)

        if self.parent is not None:
            try:
                # TODO: detect range of parameters
                parent_index = self.argv.index(self.parent)
                self.argv = self.argv[parent_index + 1:]
            except:
                return

        for key, value in self.config.items():
            if type(value) is dict:
                results[key] = CommandParser(self.argv, value, self.if_not_found, self.value_type,
                                             parent=key,
                                             is_use_parent_options=self.is_use_parent_options).parse_to_dict()
            elif key not in [NOT_FOUND_WORD, TYPE_WORD, THIS_ARG_WORD]:
                if key in self.argv:
                    try:
                        param_value = self.argv[self.argv.index(key) + 1]
                        if param_value not in self.config.keys():
                            results[key] = self.value_type(
                                self.argv[self.argv.index(key) + 1]
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
                    TYPE_WORD: lambda: globals().__setitem__(self.value_type, value)
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


def command(config: dict, is_save_results: bool = False, if_not_found=False, value_type=str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            argv = sys.argv[1:]
            command_ = CommandParser(argv, config, if_not_found, value_type)
            if is_save_results:
                command_.parse_to_dict(is_save_results)
            return func(command_, *args, **kwargs)

        return wrapper

    return decorator
