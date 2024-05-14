# Pwnbox Setup

## Directory Structure
```
.
├── Dockerfile
├── data
│   └── 
├── script
│   ├── dbg
│   └── gdb_script
└── snippet
```


---
## Files
### Dokcerfile
```Dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=en_US.UTF-8

RUN apt update && \
    apt upgrade -yq && \
    apt install -yq gcc gdb git ruby-dev gcc-multilib g++-multilib vim-gtk3 fish make gawk bison libseccomp-dev tmux wget locales binutils nasm python3-pip libssl-dev glibc-source && \
    locale-gen en_US.UTF-8

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade pwntools

# compile glibc-2.35
RUN cd /usr/src/glibc && \
    tar xvf glibc-2.35.tar.xz && \
    mkdir glibc_dbg && \
    cd glibc_dbg && \
    ../glibc-2.35/configure --prefix $PWD --enable-debug && \
    make -j4

# install pwndbg
RUN git clone https://github.com/pwndbg/pwndbg ~/pwndbg && \
    cd ~/pwndbg && \
    ./setup.sh

# install pwngdb
RUN git clone https://github.com/scwuaptx/Pwngdb.git ~/Pwngdb && \
    cat ~/Pwngdb/.gdbinit >> ~/.gdbinit && \
    sed -i "s/source ~\/peda\/peda.py//g" ~/.gdbinit

RUN gem install seccomp-tools one_gadget
RUN echo "set-option -g default-shell /bin/fish" > /root/.tmux.conf

RUN mkdir /data /script
COPY ./script /script
RUN chmod +x /script/dbg
RUN ln -s /script/dbg /usr/bin/dbg

WORKDIR /data

ENV PWNBOX=True

CMD ["/bin/fish"]
```

### dbg
```shell
#!/bin/bash

if [[ $# != 1 ]]; then
    echo "Usage : dbg <binary>";
    exit 0;
fi

exec gdb $1 -x /script/gdb_script
```

### gdb_script
```
set exec-wrapper env LD_PRELOAD=/usr/src/glibc/glibc_dbg/libc.so
```

### snippet
```shell
#!/bin/bash

VERSION="22.04";
WORKDIR="$(dirname "$0")";

if [[ $# == 0 ]]; then
    echo "========= VERSION : $VERSION =========";
    echo "Usage:";
    echo "Build environment:  ./snippet build";
    echo "Up pwnbox daemon:   ./snippet up";
    echo "Start pwnbox:       ./snippet start";
    echo "Get shell:          ./snippet shell";
    echo "Stop pwnbox daemon: ./snippet stop";
    echo "Save pwnbox image:  ./snippet save";
    exit 0
fi

if [[ $1 == "build" ]]; then
    if [ -e "pwnbox:$VERSION.tar" ]; then
        docker load --input pwnbox:$VERSION.tar;
    else
        docker build -t pwnbox:$VERSION .;
    fi
elif [[ $1 == "up" ]]; then
    docker run -it -d --name pwnbox_$VERSION -v $WORKDIR/data:/data --cap-add=SYS_PTRACE pwnbox:$VERSION;
elif [[ $1 == "start" ]]; then
    docker start pwnbox_$VERSION;
elif [[ $1 == "shell" ]]; then
    exec docker exec -it pwnbox_$VERSION fish;
elif [[ $1 == "stop" ]]; then
    docker stop pwnbox_$VERSION;
elif [[ $1 == "save" ]]; then
    docker save -o pwnbox:$VERSION.tar pwnbox:$VERSION
fi
```