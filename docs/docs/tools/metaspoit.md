# Metaspoit

## Module Type

- Auxiliary : 輔助性的模組，像是 scanner
- Encoders  : 用來編碼 payload 的模組，可以 bypass 部分的 antivirus
- Evasion   : 用來 bypass anitvirus 的模組
- Exploits  : 針對各種漏洞的攻擊模組
- NOPs      : 針對各種不同系統 padding 的模組
- Payloads  : 利用 Exploits 攻擊漏洞之後要執行的 code
- Post      : 後滲透用的模組

### Exploits Module Ranking

- Excellent : 不可能會把服務打掛
- Great     : 會自動掃描版本來更新 exploit
- Good      : 只有特定版本的 exploit，但大多數的服務都是這個版本
- Normal    : 只有特定版本的 exploit，且沒有辦法自動檢測版本
- Average   : 攻擊較不可靠或比較難成功
- Low       : 攻擊幾乎不可能成功
- Manual    : 這個攻擊基本上是一個 DoS，或是需要 target 有特別的設定

---
## `msfconsole` Command

- `search [keyword]` : 搜尋和 `keyword` 相關的 module
    - `search type:[module type] [keyword]` : 指定 `module type`
    - `search platform:[platform] [keyword]` : 指定 `platform`
- `use [module]` : 使用指定的 `module`（也就是更改當前 context 成 `module` 的 context）
- `info` : 列出當前 `module` 的相關資訊
- `show options` : 列出有什麼選項可以設定
- `show [module type]` : 列出適用於當前 context 所有 `module type` 的 module
- `set [option] [value]` : 指定 `value` 到 `option`（用 `setg` 可以指定 global 的 `options` 值）
- `unset [option]` : 取消指定給 `option` 的值（用 `unsetg` 來取消所有 global 的 `options` 值）
    - `unset all` : 取消所有指定的值）
- `check` : 檢查 target 是否可以被 exploit（這個指令要看那個 module 有沒有提供）
- `exploit`/`run` : 執行 `module`
    - `exploit -z` : 執行 `module` 且把任何開啟的 session 移到後台
- `back` : 退出 `module` 的 context
- `sessions` : 查看任何存在的 session（不限制於特定 context），每一個 session 都有自己的 ID
    - `sessions -i [session ID]` : 切換到指定的 session


---
## meterpreter Command

- `backgroud` : 把目前的 session 丟到背景執行然後切換到 `msfconsole`（ctrl + z 也可以）