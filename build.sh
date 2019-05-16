#!/usr/bin/env bash

TAG=eprosima-fast-rtps-testing-build

docker build -t ${TAG} .
if [[ $? -ne 0 ]]; then
    exit 1
fi

docker run -t --name ${TAG} ${TAG}
if [[ $? -ne 0 ]]; then
    exit 1
fi

for v in stubs examples; do
    rm -fr ${v}
    docker cp ${TAG}:/srv/${v} .
done

docker rm -f ${TAG}
