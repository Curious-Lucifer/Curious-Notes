# Script Setup

## Directory Structure

```
.
├── autoload
├── connect
└── connect_autocomplete
```


---
## Files
### autoload

```shell
export PATH=/Users/curious/code/script:$PATH

source /Users/curious/code/script/connect_autocomplete
```


### connect

```shell
#!/bin/zsh

typeset -A SSH_DATA

SSH_DATA=(
    # Exmaple
    ubuntu-22-x64 "curious@111.111.111.111"
    ubutnu-22-arm "curious@222.222.222.222"
)
MAJOR_KEY="ubuntu-22-x64"


#########


HELP_INFO="Usage : connect ["
for key in ${(k)SSH_DATA}; do
    HELP_INFO="${HELP_INFO}${key}/"
done
HELP_INFO="${HELP_INFO%/}] [send/recv] [source] [target]"


if [[ $# == 0 ]]; then
    exec ssh $SSH_DATA[$MAJOR_KEY]
fi

if [[ $# == 1 ]]; then
    if [[ -v SSH_DATA[$1] ]]; then
        exec ssh $SSH_DATA[$1]
    elif [[ $1 == "info" ]]; then
        for key in ${(k)SSH_DATA}; do
            echo "${key} : ${SSH_DATA[$key]}"
        done
    elif [[ $1 == "list" ]]; then
        echo "${(k)SSH_DATA} info help"
        exit 0
    elif [[ $1 == "help" ]]; then
        echo $HELP_INFO
        exit 0
    else
        echo $HELP_INFO
        exit 0
    fi
fi

if [[ $# == 2 ]] && [[ $1 == "check" ]]; then
    if [[ -v SSH_DATA[$2] ]]; then
        exit 0
    else
        exit -1
    fi
fi

if [[ $# == 4 ]]; then
    if [[ ! -v SSH_DATA[$1] ]]; then
        echo $HELP_INFO
        exit 0
    fi

    if [[ $2 == "send" ]]; then
        remote_location=$(echo $4 | sed "s|$HOME|~|g")
        exec scp -r $3 $SSH_DATA[$1]:$remote_location
    elif [[ $2 == "recv" ]]; then
        remote_location=$(echo $3 | sed "s|$HOME|~|g")
        exec scp -r $SSH_DATA[$1]:$remote_location $4
    else
        echo $HELP_INFO;
        exit 0
    fi
fi
```


### connect_autocomplete

```shell
_connect_autocomplete() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts=`connect list`

    if [[ ${prev} == "connect" ]]; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    if [[ ${COMP_CWORD} == 2 ]]; then
        connect check $prev
        if [ $? -eq 0 ]; then
            COMPREPLY=( $(compgen -W "send recv" -- ${cur}) )
            return 0
        fi
    fi
}

complete -F _connect_autocomplete connect
```


---
## Installation

```shell
source ./autoload
```



