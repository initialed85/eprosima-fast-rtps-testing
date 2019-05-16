#!/usr/bin/env bash

ARCH=$1

if [[ "${1}" == "" ]]; then
    echo "error: must pass architecture as first argument (e.g. x86_64 or armv7l)"

    exit 1
fi

TAG=eprosima-fast-rtps-testing-build-${ARCH}

docker build -t ${TAG} -f arch_${ARCH}/Dockerfile .
if [[ $? -ne 0 ]]; then
    exit 1
fi

docker run -i -t --name ${TAG} ${TAG}
if [[ $? -ne 0 ]]; then
    exit 1
fi

for v in stubs examples install; do
    rm -fr ${ARCH}/${v}
    docker cp ${TAG}:/srv/${v} arch_${ARCH}/
done

docker rm -f ${TAG}
