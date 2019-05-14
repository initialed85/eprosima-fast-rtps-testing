#!/usr/bin/env bash

TAG=eprosima-fast-rtps-testing-build

docker build -t ${TAG} .

docker run -t --name ${TAG} ${TAG}

for v in stubs examples; do
    rm -fr ${v}
    docker cp ${TAG}:/srv/${v} .
done

docker rm -f ${TAG}
