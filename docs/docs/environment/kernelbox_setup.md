# Kernelbox Setup

## Directory Structure
```
.
├── dev
│   └──
├── fs
│   ├── etc
│   │   └── passwd
│   └── init
├── snippet
└── src
    └── Makefile
```


---
## Files
### passwd
```
root:x:0:0:root:/root:/bin/sh
curious:x:1000:1000:curious:/home/curious:/bin/sh
```

### init
```shell
#!/bin/sh

mount -t proc none /proc
mount -t sysfs none /sys
mount -t 9p -o trans=virtio,version=9p2000.L,nosuid hostshare /home/curious
sysctl -w kernel.perf_event_paranoid=1

cd /home/curious
/bin/sh

poweroff -f
```

### snippet
```shell
#!/bin/bash -e


export KERNEL_VERSION=6.8
export BUSYBOX_VERSION=1.36.1
export WORKDIR="$(dirname "$0")"


extend_swap() {
    echo "[+] Extending swap partition..."
    sudo swapoff -a
    sudo fallocate -l 16G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
}


install_dependencies() {
    echo "[+] Checking / Installing dependencies..."
    sudo apt update
    sudo apt install -qy bc make gcc flex bison libncurses-dev libelf-dev libssl-dev cpio build-essential qemu-system-x86
}


build_linux_kernel() {
    echo "[+] Downloading kernel..."
    wget -qc https://mirrors.edge.kernel.org/pub/linux/kernel/v6.x/linux-$KERNEL_VERSION.tar.gz
    tar xzf linux-$KERNEL_VERSION.tar.gz

    echo "[+] Building kernel..."
    pushd linux-$KERNEL_VERSION
    make defconfig
    echo "CONFIG_NET_9P=y" >> .config
    echo "CONFIG_NET_9P_DEBUG=n" >> .config
    echo "CONFIG_9P_FS=y" >> .config
    echo "CONFIG_9P_FS_POSIX_ACL=y" >> .config
    echo "CONFIG_9P_FS_SECURITY=y" >> .config
    echo "CONFIG_NET_9P_VIRTIO=y" >> .config
    echo "CONFIG_VIRTIO_PCI=y" >> .config
    echo "CONFIG_VIRTIO_BLK=y" >> .config
    echo "CONFIG_VIRTIO_BLK_SCSI=y" >> .config
    echo "CONFIG_VIRTIO_NET=y" >> .config
    echo "CONFIG_VIRTIO_CONSOLE=y" >> .config
    echo "CONFIG_HW_RANDOM_VIRTIO=y" >> .config
    echo "CONFIG_DRM_VIRTIO_GPU=y" >> .config
    echo "CONFIG_VIRTIO_PCI_LEGACY=y" >> .config
    echo "CONFIG_VIRTIO_BALLOON=y" >> .config
    echo "CONFIG_VIRTIO_INPUT=y" >> .config
    echo "CONFIG_CRYPTO_DEV_VIRTIO=y" >> .config
    echo "CONFIG_BALLOON_COMPACTION=y" >> .config
    echo "CONFIG_PCI=y" >> .config
    echo "CONFIG_PCI_HOST_GENERIC=y" >> .config
    echo "CONFIG_GDB_SCRIPTS=y" >> .config
    echo "CONFIG_DEBUG_INFO=y" >> .config
    echo "CONFIG_DEBUG_INFO_REDUCED=n" >> .config
    echo "CONFIG_DEBUG_INFO_SPLIT=n" >> .config
    echo "CONFIG_DEBUG_FS=y" >> .config
    echo "CONFIG_DEBUG_INFO_DWARF4=y" >> .config
    echo "CONFIG_DEBUG_INFO_BTF=y" >> .config
    echo "CONFIG_FRAME_POINTER=y" >> .config
    echo "CONFIG_DEBUG_INFO_COMPRESSED_NONE=y" >> .config
    echo "CONFIG_DEBUG_INFO_COMPRESSED_ZLIB=n" >> .config

    sed -i 'N;s/WARN("missing symbol table");\n\t\treturn -1;/\n\t\treturn 0;\n\t\t\/\/ A missing symbol table is actually possible if its an empty .o file.  This can happen for thunk_64.o./g' tools/objtool/elf.c

    sed -i 's/unsigned long __force_order/\/\/ unsigned long __force_order/g' arch/x86/boot/compressed/pgtable_64.c

    make -j`nproc` bzImage
    make -j`nproc` modules
    popd
}


build_busybox () {
    echo "[+] Downloading BusyBox..."
    wget -qc https://busybox.net/downloads/busybox-$BUSYBOX_VERSION.tar.bz2
    tar xjf busybox-$BUSYBOX_VERSION.tar.bz2

    echo "[+] Building BusyBox..."
    pushd busybox-$BUSYBOX_VERSION
    make defconfig
    sed -i 's/# CONFIG_STATIC is not set/CONFIG_STATIC=y/g' .config
    make -j`nproc`
    make install
    popd
}


build_filesystem() {
    echo "[+] Building filesystem..."
    pushd fs
    mkdir -p bin sbin etc proc sys usr/bin usr/sbin root home/curious
    chmod +x init
    popd
    cp -a busybox-$BUSYBOX_VERSION/_install/* fs
}


build_rootfs() {
    pushd fs
    find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz
    popd
}


menu() {
    echo "========= KERNELBOX : $KERNEL_VERSION =========";
    echo "Usage : ";
    echo "Extend swap partition : ./snippet extend";
    echo "Build kernelbox :       ./snippet build";
    echo "Start kernelbox :       ./snippet start";
    echo "Build Linux kernel :    ./snippet linux";
    echo "Build BusyBox :         ./snippet busybox";
    echo "Build filesystem :      ./snippet filesystem";
    echo "Build rootfs :          ./snippet rootfs";
}



if [[ $# == 0 ]]; then
    menu
    exit 0
fi


if [[ $1 == "extend" ]]; then
    extend_swap
elif [[ $1 == "build" ]]; then
    install_dependencies
    pushd $WORKDIR
    if ! [ -e linux-$KERNEL_VERSION ]; then
        build_linux_kernel
    fi
    if ! [ -e busybox-$BUSYBOX_VERSION ]; then
        build_busybox
    fi
    build_filesystem
    popd
elif [[ $1 == "start" ]]; then
    cd $WORKDIR
    build_rootfs
    echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
    exec /usr/bin/qemu-system-x86_64 \
        -kernel linux-$KERNEL_VERSION/arch/x86/boot/bzImage \
        -initrd initramfs.cpio.gz \
        -fsdev local,security_model=passthrough,id=fsdev0,path=. \
        -device virtio-9p-pci,id=fs0,fsdev=fsdev0,mount_tag=hostshare \
        -nographic \
        -monitor none \
        -s \
        -append "console=ttyS0 nokaslr"
elif [[ $1 == "linux" ]]; then
    pushd $WORKDIR
    build_linux_kernel
    popd
elif [[ $1 == "busybox" ]]; then
    pushd $WORKDIR
    build_busybox
    popd
elif [[ $1 == "filesystem" ]]; then
    pushd $WORKDIR
    build_filesystem
    popd
elif [[ $1 == "rootfs" ]]; then
    pushd $WORKDIR
    build_rootfs
    popd
fi
```

### Makefile
```Makefile
obj-m = test.o
KERNEL_VERSION=6.8

all: 
	make -C ../linux-$(KERNEL_VERSION) M=$(PWD) modules

clean: 
	make -C ../linux-$(KERNEL_VERSION) M=$(PWD) clean
```

---
## Reference
- [Ubuntu 18.04 Swap Partition Extension](https://blog.csdn.net/AlexWang30/article/details/90341172)
