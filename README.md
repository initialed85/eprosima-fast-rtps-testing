# eprosima-fast-rtps-testing

This repo contains the means to handle the following steps related to eProsima's Fast-RTPS (DDS):

- build eProsima's Fast-RTPS
    - support for `x86_84` and `armv7l` 
- for each IDL file in each folder inside `src`:
    - generate code stubs
    - generate examples
    - build examples
 
## How do I use it?

Prerequisites:

- Docker

Steps:

- Put your IDLs in an appropriate folder inside the `src` folder; e.g.:
    - `src`
        - `HelloWorld`
            - `HelloWorld.idl`
- Run `./build_x86_64.sh` or `./build_armv7l.sh`
- Observe as the `examples`, `stubs` and `install` folder under the relevant architecture folder become populated

## Then what?

- Employ the stubs in your project; or
- Build the examples and have a tinker; or
- Run the examples (if your architecture matches the one you built)
