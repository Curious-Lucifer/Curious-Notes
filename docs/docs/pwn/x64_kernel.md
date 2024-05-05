# x64 Kernel

## 5.4 Module Example

### Simple Module

```c
#include <linux/module.h>
#include <linux/kernel.h>

MODULE_LICENSE("GPL");

int init_module(void) {
    printk(KERN_ALERT "Module Loaded\n");
    return 0;
}

void cleanup_module(void) {
    printk(KERN_ALERT "Module Removed\n");
}
```


### Devcice File

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");

static int major_number;


static int device_open(struct inode *inode, struct file *filp) {
    printk(KERN_ALERT "Device Opened\n");
    return 0;
}

static int device_release(struct inode *inode, struct file *filp) {
    printk(KERN_ALERT "Device Closed\n");
    return 0;
}

static ssize_t device_read(struct file *filp, char *buf, size_t len, loff_t *offset) {
    char *msg = "Hello World!\n";
    size_t msg_len = strlen(msg);
    return msg_len - copy_to_user(buf, msg, (len > msg_len) ? msg_len : len);
}

static ssize_t device_write(struct file *filp, const char *buf, size_t len, loff_t *offset) {
    char msg[0x10] = {0};
    copy_from_user(msg, buf, (len > 0xf) ? 0xf : len);
    printk(KERN_ALERT "Input : %s", msg);
    return (len > 0xf) ? 0xf : len;
}

static struct file_operations fops = {
    .read = device_read, 
    .write = device_write, 
    .open = device_open, 
    .release = device_release
};


int init_module(void) {
    major_number = register_chrdev(0, "dev-test", &fops);

    if (major_number < 0) {
        printk(KERN_ALERT "Registering char device failed with %d\n", major_number);
		return major_number;
    }

    printk(KERN_INFO "Run : 'mknod /dev/dev-test c %d 0'.\n", major_number);
    return 0;
}

void cleanup_module(void) {
    unregister_chrdev(major_number, "dev-test");
}
```


### Proc File

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/proc_fs.h>

MODULE_LICENSE("GPL");


static int device_open(struct inode *inode, struct file *filp) {
    printk(KERN_ALERT "Device Opened\n");
    return 0;
}

static int device_release(struct inode *inode, struct file *filp) {
    printk(KERN_ALERT "Device Closed\n");
    return 0;
}

static ssize_t device_read(struct file *filp, char *buf, size_t len, loff_t *offset) {
    char *msg = "Hello World!\n";
    size_t msg_len = strlen(msg);
    return msg_len - copy_to_user(buf, msg, (len > msg_len) ? msg_len : len);
}

static ssize_t device_write(struct file *filp, const char *buf, size_t len, loff_t *offset) {
    char msg[0x10] = {0};
    copy_from_user(msg, buf, (len > 0xf) ? 0xf : len);
    printk(KERN_ALERT "Input : %s", msg);
    return (len > 0xf) ? 0xf : len;
}

static struct file_operations fops = {
    .read = device_read, 
    .write = device_write, 
    .open = device_open, 
    .release = device_release
};

struct proc_dir_entry *proc_entry = NULL;


int init_module(void) {
    proc_entry = proc_create("proc-test", 0666, NULL, &fops);
    printk(KERN_ALERT "/proc/proc-test Created\n");
    return 0;
}

void cleanup_module(void) {
    if (proc_entry) proc_remove(proc_entry);
    printk("/proc/proc-test Removed\n");
}
```


### Get Root Access

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/proc_fs.h>
#include <linux/cred.h>

#define PWN _IO('P', 0)

MODULE_LICENSE("GPL");


static int device_open(struct inode *inode, struct file *filp) {
    printk(KERN_ALERT "Device Opened\n");
    return 0;
}

static int device_release(struct inode *inode, struct file *filp) {
    printk(KERN_ALERT "Device Closed\n");
    return 0;
}

static ssize_t device_read(struct file *filp, char *buf, size_t len, loff_t *offset) {
    return -EINVAL;
}

static ssize_t device_write(struct file *filp, const char *buf, size_t len, loff_t *offset) {
    return -EINVAL;
}

static long device_ioctl(struct file *filp, unsigned int ioctl_num, unsigned long ioctl_param) {
    printk(KERN_ALERT "ioctl Call : %d", ioctl_num);
    if (ioctl_num == PWN) {
        printk(KERN_ALERT "Granting root access");
        commit_creds(prepare_kernel_cred(NULL));
    }
    return 0;
}

static struct file_operations fops = {
    .read = device_read, 
    .write = device_write, 
    .unlocked_ioctl = device_ioctl,
    .open = device_open, 
    .release = device_release
};

struct proc_dir_entry *proc_entry = NULL;


int init_module(void) {
    proc_entry = proc_create("get-root", 0666, NULL, &fops);
    return 0;
}

void cleanup_module(void) {
    if (proc_entry) proc_remove(proc_entry);
}
```


### Seccopme Escape (For Current Process)

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/proc_fs.h>
#include <linux/cred.h>

#define PWN _IO('P', 0)

MODULE_LICENSE("GPL");


static int device_open(struct inode *inode, struct file *filp) {
    printk(KERN_ALERT "Device Opened\n");
    return 0;
}

static int device_release(struct inode *inode, struct file *filp) {
    printk(KERN_ALERT "Device Closed\n");
    return 0;
}

static ssize_t device_read(struct file *filp, char *buf, size_t len, loff_t *offset) {
    return -EINVAL;
}

static ssize_t device_write(struct file *filp, const char *buf, size_t len, loff_t *offset) {
    return -EINVAL;
}

static long device_ioctl(struct file *filp, unsigned int ioctl_num, unsigned long ioctl_param) {
    printk(KERN_ALERT "ioctl Call : %d", ioctl_num);
    if (ioctl_num == PWN) {
        printk(KERN_ALERT "Escaping seccomp");
        current->thread_info.flags &= ~_TIF_SECCOMP;
    }
    return 0;
}

static struct file_operations fops = {
    .read = device_read, 
    .write = device_write, 
    .unlocked_ioctl = device_ioctl,
    .open = device_open, 
    .release = device_release
};

struct proc_dir_entry *proc_entry = NULL;


int init_module(void) {
    proc_entry = proc_create("escape-seccomp", 0666, NULL, &fops);
    return 0;
}

void cleanup_module(void) {
    if (proc_entry) proc_remove(proc_entry);
}
```


---
## Cheat Sheet

### Get Physical Address From Virtual Address
> This is just for address that directly mapped or allocated via `kmalloc`

```c
#include <linux/mm.h>

phys_addr_t virt_to_phys(volatile void *address);
```


### Read/Write Data from Physical Address

```c
#include <linux/io.h>

// Use `ioremap` to get a temporary virtual address that maps to `phys_address`, 4 means the size that we can access (it will align to 0x1000)
void *temp_virt_address = ioremap(phys_address, 4);

// Read/Write to temp_vrit_address

iounmap(temp_virt_addr);
```


### Get CR3

```c
// This is the virtual address maps to the physical address that CR3 point to
current->mm->pgd;
```

---
## Mitigations

### SMEP

Prevents kernel execute code from userspace.

### SMAP

Prevents kernel access userspace memory unless the AC flag in the RFLAGS register is set. use `stac` to set and `clac` to unset the AC flag.


---
## Reference

- [Kernel Security Introduction](https://www.youtube.com/watch?v=j0I2AakUAxk&list=PL-ymxv0nOtqowTpJEW4XTiGQYx6iwa6og)

