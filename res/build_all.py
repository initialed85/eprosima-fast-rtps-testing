import os
import shlex
import subprocess

_BASE_PATH = '/srv'
_IDL_PATH = '{}/src'.format(_BASE_PATH)
_STUBS_PATH = '{}/stubs'.format(_BASE_PATH)
_EXAMPLES_PATH = '{}/examples'.format(_BASE_PATH)
_FASTRTPSGEN_PATH = '{}/install/bin/fastrtpsgen'.format(_BASE_PATH)


def _execute(cmd):
    p = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = p.communicate()

    return (
        stdout.decode('utf-8').strip() if stdout is not None else '',
        stderr.decode('utf-8').strip() if stderr is not None else '',
        p.returncode if p.returncode is not None else -1
    )


def _print_execute_output(some_out, some_err, some_ret):
    names_and_variables = [
        ('STDOUT', some_out),
        ('STDERR', some_err),
        ('RETURN', some_ret),
    ]

    parts = []

    for name, variable in names_and_variables:
        if variable is None or (isinstance(variable, str) and variable.strip() == ''):
            continue

        parts += ['{}: {}'.format(
            name,
            '\n{}'.format(variable.strip()) if isinstance(variable, str) else variable
        )]

    print('\n\n'.join(parts))


class FastRTPSGenError(Exception):
    pass


class CMakeError(Exception):
    pass


class MakeError(Exception):
    pass


for idl_folder in os.listdir(_IDL_PATH):
    print('-- Handling {} IDL folder\n'.format(repr(idl_folder)))
    for idl_file in os.listdir(os.path.join(_IDL_PATH, idl_folder)):
        if os.path.splitext(idl_file)[-1].lower() != '.idl':
            continue

        print('---- Handling {} IDL file\n'.format(repr(idl_file)))

        idl_path = os.path.join(_IDL_PATH, idl_folder, idl_file)

        tasks = [
            ('stubs', _STUBS_PATH, '{} -d {} {}'),
            ('examples', _EXAMPLES_PATH, '{} -d {} -example CMake {}'),
        ]

        for name, path_prefix, cmd_template in tasks:
            print('------ Generating code for {}\n'.format(name))

            path = os.path.join(path_prefix, idl_folder)

            os.mkdir(path)

            out, err, ret = _execute(
                cmd_template.format(
                    _FASTRTPSGEN_PATH,
                    path,
                    idl_path,
                )
            )

            _print_execute_output(out, err, ret)

            if ret == 0:
                continue

            raise FastRTPSGenError(
                'attempt to execute fastrtpsgen returned {}; see printed output'.format(
                    ret,
                )
            )

for name in os.listdir(_EXAMPLES_PATH):
    print('------ Building examples for {}\n'.format(name))

    build_dir = os.path.join(_EXAMPLES_PATH, name, 'build')

    os.mkdir(build_dir)

    os.chdir(build_dir)

    out, err, ret = _execute(
        'cmake -DCMAKE_TOOLCHAIN_FILE=/srv/toolchain.cmake -DCMAKE_PREFIX_PATH=/srv/install ..'
    )

    _print_execute_output(out, err, ret)

    if ret != 0:
        raise CMakeError(
            'attempt to execute cmake returned {}; see printed output'.format(
                ret,
            )
        )

    out, err, ret = _execute(
        'make'
    )

    _print_execute_output(out, err, ret)

    if ret != 0:
        raise MakeError(
            'attempt to execute make returned {}; see printed output'.format(
                ret,
            )
        )

os.chdir(_BASE_PATH)
