# eprosima-fast-rtps-testing

This repo mostly contains the means to automatically generate the code stubs and examples for the IDL files given in the `src` folder.

## How do I use it?

Prerequisites:

- Docker

Steps:

- Put your IDLs in an appropriate folder inside the `src` folder; e.g.:
    - `src`
        - `HelloWorld`
            - `HelloWorld.idl`
- Run `./build.sh`
- Observe as the `stubs` and `examples` folders become populated with the output (in the same folder structure)
