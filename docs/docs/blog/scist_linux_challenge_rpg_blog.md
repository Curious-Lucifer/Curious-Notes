# SCIST Linux Challenge RPG Blog

這篇會寫一些關於怎麼使用 SCIST Linux Challenge RPG 、簡單的架構介紹和要怎麼自己 build Image，Writeup 的部分可以到 [這裡](/writeup/scist_linux_challenge_rpg_writeup/) 去看。

## 安裝說明
1. 首先需要創建一個放 SCIST Linux Challenge RPG 相關檔案的資料夾，並移動到這個資料夾
    ```shell
    mkdir ~/SCIST_Linux_Challenge
    cd ~/SCIST_Linux_Challenge_RPG
    ```
2. 下載 `snippet` 這個 bash script 來安裝 Docker、pull SCIST Linux Challenge RPG 的 Docker Image 和下載 `docker-compose.yml`
    ```shell
    wget https://linux.ctf.scist.org/files/8aa6b2be1483d870d50b4695c62d82cd/snippet
    chmod +x snippet
    ./snippet install
    ```
3. 如果是第一次安裝 Docker 的話，`snippet` 會把當前使用者加入到 `docker` 的群組，需要使用者重新登入或重新啟動來讓這個設定生效


---
## 使用說明
1. 首先需要移動到放 SCIST Linux Challenge RPG 相關檔案的資料夾
    ```shell
    cd ~/SCIST_Linux_Challenge
    ```
2. 開始挑戰（會把 Lab 開起來並進入 Lab，使用者會切換成 `treasure_hunter`。如果 Lab 已經開啟則會直接進入 Lab）
    ```shell
    ./snippet start
    ```
3. 離開挑戰（可以透過看使用者是不是 `treasure_hunter` 來確認是不是在 Lab 內）
    ```shell
    exit
    ```
4. 關閉挑戰（需要離開 Lab 之後才能關閉挑戰）
    ```shell
    ./snippet stop
    ```
5. 取得說明
    ```shell
    ./snippet
    ```

> 注意事項：
> - 如果不小心刪到 Lab 內的東西，可以離開挑戰 -> 關閉挑戰 -> 開始挑戰，這樣 Lab 的環境就就會還原了
> - 因為開始挑戰之後會開啟三個 Docker Container，所以在電腦（或虛擬機）關機前一定要記得關閉挑戰（而關閉挑戰前需要先離開挑戰）
> - Lab 中 `treasure_hunter` 的密碼是 `password`


---
## 架構介紹

### 總攬
SCIST Linux Challenge RPG 會在使用者的電腦下載以下的檔案和 Docker Image

- 檔案
    - `snippet`
    - `docker-compose.yml`
- Docker Image
    - `curiouslucifer/scist_linux_challenge_rpg:$version-challenge_box`
    - `curiouslucifer/scist_linux_challenge_rpg:$version-ssh_service`
    - `curiouslucifer/scist_linux_challenge_rpg:$version-web_service`

### `snippet`
`snippet` 有以下的執行方式

- `snippet`：印出所有執行方式，並加上一點解釋
- `snippet install`：如果使用者的電腦沒有下載 Docker 的話，幫使用者下載 Docker 並把當前使用者加入 `docker` 的群組（需要重新登入/重新啟動來 active 這個設定）。如果當前資料夾沒有 `docker-compose.yml` 這個檔案的話，`snippet` 會下載這個檔案並把三個 Lab 需要的 Docker Image pull 下來
- `snippet start`：把當前資料夾的 `docker-compose.yml` 設定的 Lab 跑起來，然後進入 `challenge_box` 這個 container
- `snippet stop`：把當前資料夾 `docker-compose.yml` 設定的 Lab 關閉
- `snippet remove`：把 SCIST Linux Challenge RPG 所有檔案和 Docker Image 刪掉，同時刪除 `~/SCIST_Linux_Challenge`

### `docker-compose.yml`
`docker-compose.yml` 設定了以 `curiouslucifer/scist_linux_challenge_rpg:$version-challenge_box`、`curiouslucifer/scist_linux_challenge_rpg:$version-ssh_service`、`curiouslucifer/scist_linux_challenge_rpg:$version-web_service` 這三個 Image 為 base 跑起來的 Container，並關閉它們的 logging driver。

主要使用 Docker Compose 把 Image 跑起來是因為 Compose 會自動設定 Network，讓三個 Container 可以直接用 Container name 來 access 其他 Container。

### Docker Image
- `challenge_box`：使用者開始挑戰後就會進入到這個 Image 跑起來的 Container，基本指令執行相關的挑戰都寫在這個 Image 
- `ssh_service`：這個 Image 寫有 ssh 和 bypass shell 相關的挑戰，使用者在 `challenge_box` 中可以透過 `ssh <username>@ssh_service` 連進這個 Image 跑起來的 Container
- `web_service`：這個 Image 寫有 web 相關的挑戰，使用者在 `challenge_box` 中可以瘦過 `http://web_service` 訪問到這個 Image 跑起來 Container 的服務

> 這三個 Image 都有支持 amd64 和 arm64 架構


---
## Build Docker Image From Source

1. 首先先把原始碼 clone 下來
    ```shell
    git clone https://github.com/scist-tw/SCIST_Linux_Challenge_RPG.git
    ```
2. 接著進入 SCIST Linux Challenge RPG 的資料夾
    ```shell
    cd ~/SCIST_Linux_Challenge_RPG
    ```
3. 執行以下程式碼把三個 Image build 起來
    ```shell
    ./build_image.sh
    ```

> 相關的 `Dockerfile` 分別在 `Challenge_Box/Dockerfile`、`SSH_Service/Dockerfile` 和 `Web_Service/Dockerfile`，基本上就是先用一個 stage 把 ELF 編譯起來，然後再用一格 stage 把所有檔案放到對的位置
> 
> 原始碼中的 `push_image.sh` 和 `manage_manifest.sh` 分別是用來推到我自己的 Docker Hub 中和建立同時支援 amd64 和 arm64 的 Image 並 push 到 Docker Hub 的。而 `challenge` 這個資料夾下放著所有 SCIST Linux Challenge RPG 的題目敘述和 flag。


---
## 相關連結
- CTFd：[https://linux.ctf.scist.org](https://linux.ctf.scist.org)
- Github：[https://github.com/scist-tw/SCIST_Linux_Challenge_RPG/tree/master](https://github.com/scist-tw/SCIST_Linux_Challenge_RPG/tree/master)
- Docker Hub：[https://hub.docker.com/r/curiouslucifer/scist_linux_challenge_rpg](https://hub.docker.com/r/curiouslucifer/scist_linux_challenge_rpg)

