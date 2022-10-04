from typing import Tuple


class Argumenter:
    @staticmethod
    def check_arguments(arguments: list, keys: list) -> Tuple[str, bool]:
        missing_arguments = []
        for argument in arguments:
            if argument not in keys:
                missing_arguments.append(argument)

        if len(missing_arguments) > 0:
            return f'Missing call parameters, the following fields are missing: {",".join(missing_arguments)}', False
        else:
            return 'OK', True


argumenter = Argumenter()
