import os
import pickle


def with_dump(dump_name):
    def wrap(function):
        def wrapped_function(*args):
            if os.path.isfile(dump_name):
                with open(dump_name, "rb") as file:
                    return pickle.load(file)
            else:
                result = function(*args)

                with open(dump_name, "wb") as file:
                    pickle.dump(result, file)

                return result

        return wrapped_function

    return wrap
