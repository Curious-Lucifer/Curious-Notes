# Arch Linux Setup

## Install Arch Linux

1. 輸入以下指令
    ```shell
    pacman -Sy
    pacman -Sy archlinux-keyring
    archinstall
    ```
2. Set `Mirrors` -> `Mirror region` to `Taiwan`
3. Set `Disk Configuration` -> `Use a best-effort default partition layout` and select the dist, then choose the filesystem to be `btrfs` (set anyother to default)
4. Change `Hostname`
5. Change `Root password`
6. Select `User account` and `Add a user`
7. Select `Profile` -> `Type` and choose `Server`, then select `sshd`
8. Select `Additional packages` and type `sudo vim`
9. Set `Network configuration` to `Use NetworkManager`
10. Set `Timezone` to `Asia/Taipei`
11. Install


---
## Disable Password For Sudo

1. 輸入以下指令
    ```shell
    sudo rm /etc/sudoers.d/00_curious
    sudo EDITOR=vim visudo
    ```
2. 去掉以下這行的註解
    ```
    %wheel ALL=(ALL:ALL) NOPASSWD: ALL
    ```


---
## Install Zsh + Oh My Zsh + Powerlevel10k

1. Install `zsh` & `git`
    ```shell
    sudo pacman -Sy && sudo pacman -Syu
    sudo pacman -Sy zsh git
    ```
2. Install `Oh My Zsh`
    ```shell
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```
3. Install theme `PowerLevel10k`
    ```shell
    git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k
    ```
4. Install plugin `zsh-autosuggestions`
    ```shell
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    ```
5. Install plugin `zsh-syntax-highlighting`
    ```shell
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
    ```
6. Modify `~/.zshrc`
    ```
    ZSH_THEME="powerlevel10k/powerlevel10k"
    ```
    ```
    plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
    ```
7. Load new `.zshrc`
    ```shell
    source ~/.zshrc
    ```


---
## Packages Installation

```shell
sudo pacman -Syu python python-pipx gcc gdb git ruby make gawk bison libseccomp tmux wget binutils nasm openssl

pipx install pwntools
```

Add `export PATH=/home/curious/.local/bin:$PATH` to `.zshrc`

```shell
git clone https://github.com/pwndbg/pwndbg ~/pwndbg && \
cd ~/pwndbg && \
./setup.sh

git clone https://github.com/scwuaptx/Pwngdb.git ~/Pwngdb && \
cat ~/Pwngdb/.gdbinit >> ~/.gdbinit && \
sed -i "s/source ~\/peda\/peda.py//g" ~/.gdbinit

gem install seccomp-tools one_gadget
```

Add `export PATH=/home/curious/.local/share/gem/ruby/3.0.0/bin:$PATH` to `.zshrc`


---
## Reference
- [Ubuntu 安裝 Zsh + Oh My Zsh + Powerlevel10k](https://www.kwchang0831.dev/dev-env/ubuntu/oh-my-zsh)