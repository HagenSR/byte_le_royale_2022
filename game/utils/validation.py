import re

from game.config import ALLOWED_MODULES


def verify_code(filename, already_string=False):
    contents = None

    if already_string:
        contents = filename
    else:
        with open(filename, 'r') as f:
            contents = f.read()

    contents = contents.split('\n')

    illegal_imports = list()
    uses_open = False

    for line in contents:
        line = re.split('[ ;]', line)

        while 'from' in line or 'import' in line or 'open' in line:
            # Check for illegal keywords
            if 'from' in line:
                module = line[line.index('from') + 1]
                if module not in ALLOWED_MODULES:
                    illegal_imports.append(module)

                line.remove('from')
                line.remove('import')
            elif 'import' in line:
                module = line[line.index('import') + 1]
                if module not in ALLOWED_MODULES:
                    illegal_imports.append(module)

                line.remove('import')
            if 'open' in line:
                uses_open = True

                line.remove('open')

    return illegal_imports, uses_open


def verify_num_clients(clients, set_clients, min_clients, max_clients):
    res = None
    # Verify correct number of clients
    if set_clients is not None and len(clients) != set_clients:
        res = ValueError("Number of clients is not the set value.\n"
                         "Number of clients: " +
                         str(len(clients)) +
                         "  |  Set number: " +
                         str(set_clients))
    elif min_clients is not None and len(clients) < min_clients:
        res = ValueError("Number of clients is less than the minimum required.\n"
                         "Number of clients: " + str(len(clients)) + "  |  Minimum: " + str(min_clients))
    elif max_clients is not None and len(clients) > max_clients:
        res = ValueError("Number of clients exceeds the maximum allowed.\n"
                         "Number of clients: " +
                         str(len(clients)) +
                         "  |  Maximum: " +
                         str(max_clients))

    return res
