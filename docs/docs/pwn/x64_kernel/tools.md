# Tools

`initramfs.cpio.gz` -> file system

```shell
gzip -cd initramfs.cpio.gz | cpio -idmv
```

file system -> `initramfs.cpio.gz`

```shell
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz
```

