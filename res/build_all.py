import os
import shlex
import subprocess

_IDL_PATH = '/srv/src'
_STUBS_PATH = '/srv/stubs'
_EXAMPLES_PATH = '/srv/examples'


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


class FastRTPSGenError(Exception):
    pass


for idl_folder in os.listdir(_IDL_PATH):
    print('-- Handling {} IDL folder\n'.format(repr(idl_folder)))
    for idl_file in os.listdir(os.path.join(_IDL_PATH, idl_folder)):
        if os.path.splitext(idl_file)[-1].lower() != '.idl':
            continue

        print('---- Handling {} IDL file\n'.format(repr(idl_file)))

        idl_path = os.path.join(_IDL_PATH, idl_folder, idl_file)

        tasks = [
            ('stubs', _STUBS_PATH, 'fastrtpsgen -d {} {}'),
            ('examples', _EXAMPLES_PATH, 'fastrtpsgen -d {} -example CMake {}'),
        ]

        for name, path_prefix, cmd_template in tasks:
            print('------ Generating {}\n'.format(name))

            path = os.path.join(path_prefix, idl_folder)

            os.mkdir(path)

            out, err, ret = _execute(
                cmd_template.format(
                    path,
                    idl_path,
                )
            )

            print('STDOUT:\n{}\n\nSTDERR:\n{}\n\nRETURN: {}\n'.format(
                out,
                err,
                ret
            ))

            if ret == 0:
                continue

            raise FastRTPSGenError(
                'attempt to execute fastrtpsgen returned {}; see printed output'.format(
                    ret,
                )
            )
