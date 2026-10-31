# 候選版驗證紀錄

- Version：0.1.0-candidate
- Last Update：2026-10-31
- Purpose：候選版驗證紀錄

驗證日期：2026-10-31。測試範圍：本機 Python、隔離暫存目錄。

執行方式：

```sh
python3 -B scripts/validate.py template .
python3 -B scripts/test_tools.py
```

檢查範圍包含任意工作目錄與空白路徑初始化、拒絕覆寫、拒絕範本內初始化、必要檔案遺失、manifest 內容變動、未收錄檔案與失效相對連結。

未實測：各 agent 平台入口、其他作業系統、其他 Python 版本。敏感資訊自動檢查僅為有限規則，發布前仍需人工審閱。

## 新使用者下載演練

2026-10-31 從 GitHub 的提交 `60643d44be2a42f486c75fbd3ec00797a41a99d7` 分別以 Git clone 與 ZIP 下載，在兩個隔離目錄執行 README 快速開始。測試使用暫存私人目錄取代家目錄下的 demo 目錄，未更改 HOME 環境變數。

兩條路徑均通過：範本驗證、初始化、私人目錄驗證、中文及空白路徑、從其他工作目錄驗證、修改虛構資料後驗證、備份回復與重複初始化拒絕覆寫。

發現首次 agent 接入指引不足，已補上路徑取得方式、可直接貼上的只讀提示與預期答案。測試僅證明檔案流程可用；未以全新 Codex、Hermes 或 OpenClaw 執行個體驗證平台接入。測試環境為 macOS；其他系統仍未實測。

## 隔離平台接入驗收

日期：2026-10-31。平台：macOS。測試來源：GitHub 提交 ac03229415d4e0196a6d9a9ea1c6cb8f0164039c。

| 平台 | 結果 | 邊界 |
|---|---|---|
| Codex CLI 0.166.0-alpha.5.1 | 兩個獨立對話通過 | 獨立狀態目錄、專案 AGENTS.md、read-only 模式 |
| Hermes 0.22.5 | 兩個獨立對話通過 | 獨立 HERMES_HOME、專案 AGENTS.md、僅啟用 file 工具組 |
| OpenClaw 2026.10.8 | 阻擋，未完成範本讀取 | local CLI 的獨立狀態目錄缺少可啟用的 codex runtime |

每個成功平台第一輪從 AGENTS.md 找到資料目錄，實際讀取 README、policy 和 project，回報虛構專案及專用驗收碼。第二輪由測試程式變更虛構狀態及驗收碼，再啟動全新對話；兩者均讀到新值。沒有把來源檔案內容或驗收碼預先放入查詢提示。

OpenClaw 首次遇到路由認證缺失；在隔離設定明確指定 ChatGPT 路由與 codex runtime 後，回報 owner-plugin-not-activatable。未執行 doctor --fix、Gateway 啟動或重啟，故不能宣稱 OpenClaw 實際接入已通過，也不能由此判定範本內容故障。

隔離方式是應用程式狀態隔離，不是 VM 或完整檔案系統隔離。使用既有登入的受限暫存副本，沒有保留可用的 refresh token，測試後移除全部暫存狀態及登入副本。正式環境六個受追蹤的主要設定／登入檔雜湊未變；測試來源檔也沒有被 agent 修改。此結果不等於全面稽核所有正式環境檔案。

本次驗證 CLI 的專案指引讀取；未驗證桌面 UI、長期排程、聊天渠道或其他作業系統。

## OpenClaw 隔離重測通過

2026-10-31 補齊隔離環境後重測成功，取代前節 OpenClaw 尚未完成的狀態。OpenClaw 與獨立安裝的 @openclaw/codex 插件版本均為 2026.10.8，使用 codex harness、ChatGPT OAuth 登入副本及唯讀工具範圍。

最初阻礙包含隔離目錄沒有安裝 runtime 插件，以及隔離登入副本未成為 OpenClaw 可用的模型認證。補齊插件後，透過該版本 provider-auth SDK 把有效 access token 寫入測試專用帳號儲存區，改用 agent scope；未保存可用 refresh token，也未修改正式認證。這是測試準備方式，不是建議使用者手動搬移正式憑證。

兩次使用不同 session ID 的 local CLI 對話，均透過 AGENTS.md 找到私人資料並讀出虛構專案、來源日期與專用驗收碼。第二輪由測試程式變更狀態與驗收碼，新對話讀到新值。每輪有三次成功 read；另有兩次先誤讀工作區根目錄後自行修正路徑的失敗嘗試，最終結果正確。

測試資料放在 agent workspace 的 data 子目錄，符合 tools.fs.workspaceOnly。未驗證工作區外的檔案存取、Gateway 聊天渠道或桌面 UI。四個受追蹤的正式設定／認證檔雜湊未變；agent 沒有修改測試來源。測試後已刪除隔離狀態、登入副本與安裝快取；未啟動或重啟正式 Gateway。
