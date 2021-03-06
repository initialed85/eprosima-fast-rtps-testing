FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    git default-jdk-headless gradle build-essential cmake python3 \
    g++-arm-linux-gnueabihf g++-4.8-arm-linux-gnueabihf g++-5-arm-linux-gnueabihf \
    gcc-arm-linux-gnueabihf gcc-4.8-arm-linux-gnueabihf gcc-5-arm-linux-gnueabihf \
    binutils-arm-linux-gnueabihf libc6-dev-armhf-cross

WORKDIR /srv/

RUN git clone https://github.com/eProsima/Fast-RTPS

WORKDIR /srv/Fast-RTPS

# eProsima Fast-RTPS v1.7.2
RUN git checkout a8691a40be6b8460b01edde36ad8563170a3a35a

RUN mkdir -p /srv/Fast-RTPS/build

WORKDIR /srv/Fast-RTPS/build

COPY arch_armv7l/res/toolchain.cmake /srv/toolchain.cmake

RUN mkdir -p /srv/install/

RUN cmake -DTHIRDPARTY=ON -DBUILD_JAVA=ON \
    -DCMAKE_TOOLCHAIN_FILE=/srv/toolchain.cmake \
    -DCMAKE_INSTALL_PREFIX=/srv/install/ \
    ..

RUN make

RUN make install

RUN ldconfig

WORKDIR /srv/

RUN mkdir -p /srv/stubs

RUN mkdir -p /srv/examples

COPY res/build_all.py /srv/build_all.py

COPY src /srv/src

CMD ["python3", "build_all.py"]
