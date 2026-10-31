# shared-agent-template

- Version：0.1.0-candidate
- Last Update：2026-10-31
- Purpose：Shared Agent Template

多個 AI agent 共用文件與操作指南的本機範本。適合願意維護 Markdown、希望減少知識副本漂移的使用者。

目前為初期預覽版，採用 [MIT 授權](LICENSE)。沒有自動同步、常駐服務或憑證管理功能。適用 Python 3.10 以上；腳本只使用標準函式庫。

## 執行環境

以下指令適用 macOS／Linux 的終端機，需要 Python 3.10 以上；先執行 `python3 --version` 確認。Git clone 需要 Git；下載 ZIP 不需要 Git。Windows 原生命令列尚未驗證，請勿直接照貼含 `$HOME` 的指令。

## 下載

```sh
git clone https://github.com/rockism/shared-agent-template.git
cd shared-agent-template
```

也可以在 GitHub 點選 Code → Download ZIP，解壓縮後開啟終端機並切換到專案目錄。

## 快速開始

在解壓縮或 clone 後的專案目錄執行（該目錄應能看到 README.md 與 scripts/）：

```sh
python3 scripts/validate.py template .
python3 scripts/init_workspace.py "$HOME/shared-agent-data-demo"
python3 scripts/validate.py workspace "$HOME/shared-agent-data-demo"
```

初始化只接受尚不存在的目標目錄，不覆寫既有資料。目標目錄不得位於範本內；私人資料與公開範本分開管理。先用 demo 目錄試用，確認後再自行選定正式路徑。後續不需重新初始化。

三個指令應依序顯示 `PASS`、`Created example workspace`、`PASS`。若目標目錄已存在，初始化會拒絕執行；已有資料時直接驗證，想重新試用則選另一個新目錄，不要刪除既有資料。

## 首次接入 agent

先在專案目錄執行 `pwd` 取得範本的絕對路徑，再執行 `python3 -c 'from pathlib import Path; print(Path.home() / "shared-agent-data-demo")'` 取得私人資料路徑。

開啟一個有本機檔案讀取能力的 agent 對話，把下列兩個占位符換成上述路徑，再貼上：

```text
本次只讀測試。
私人資料目錄：<PRIVATE_WORKSPACE>
範本目錄：<TEMPLATE_ROOT>
請讀私人目錄的 README.md、policy.md，依索引讀取專案資料。
請回報專案名稱、目前狀態、來源日期，以及是否為真實資料。
列出實際讀取的檔案路徑；若不能讀取，明確說明，不要猜測。
```

預期答案：專案為「紙風車閱讀清單」、狀態「草稿」、來源日期 `2026-10-31`，且明確指出是虛構教學資料。若 agent 無法存取本機目錄，需先依該平台設定檔案存取，不能視為接入成功。

確認首次讀取後，再選讀 [adapter 指引](adapters/README.md)，把接入文字放到該 agent 的持續性指引。另開新對話重測，才能確認持續性設定有效；本範本不會自動完成這一步。

## WebChat 與 Hermes 桌面接入

### 已完成的驗收

2026-10-31 在 macOS 以獨立應用程式狀態及虛構資料測試，從真實聊天介面送出問題並檢查回答：

| 介面 | 結果 | 已驗證範圍 |
|---|---|---|
| OpenClaw 2026.10.8 本機 WebChat | 通過 | 經獨立 Gateway 讀取專案指標；資料更新後，新對話讀到新狀態與驗收碼 |
| Hermes Electron 桌面，來源提交 `bf0203a794a` | 通過 | 正確工作目錄下自動載入 AGENTS.md；更換指標後，新工作階段讀取新位置 |

Hermes 的自動載入驗收沒有在提問中提供檔案路徑、專案名稱或驗收碼；兩個工作階段的系統提示均包含當輪指標，工具紀錄與畫面回答吻合。此結果補足先前僅在訊息中明確指定 AGENTS.md 路徑的桌面測試。

未測：Telegram／Discord、OpenClaw 原生 macOS App、Codex 桌面、其他作業系統，以及既有對話即時重新載入指標。Hermes 使用來源副本建置，並非所有已發布桌面版本的相容性保證。完整歷程見 [驗證紀錄](docs/validation.md)。

### 共用的專案指標

在 agent 的專案根目錄建立 `AGENTS.md`；已有該檔時先備份，再合併指引，不要覆寫既有規則。將以下占位符換成實際絕對路徑，資料內容仍保留在私人資料目錄：

```text
本專案的共用資料唯一來源：<PRIVATE_WORKSPACE>。
回答專案問題前，先讀 <PRIVATE_WORKSPACE>/README.md 與 <PRIVATE_WORKSPACE>/policy.md，
再依索引讀取所需資料。資料變更時以來源檔案為準，不憑舊對話猜測。
本次驗收僅讀取本專案與指定共用資料，不修改檔案或傳送外部訊息。
若無法讀取，請明確說明。
```

### OpenClaw 本機 WebChat 設定

先確認獨立測試環境的模型登入及 runtime 可用；本次使用 `@openclaw/codex` 2026.10.8。範本不提供模型登入或 Gateway 認證。以下是需合併到測試設定的欄位摘要，不是完整可直接取代的設定檔：

- `agents.defaults.workspace` 與所用 agent 的 `workspace` 指向含 AGENTS.md 的測試專案。
- 啟用 `tools.fs.workspaceOnly` 時，私人資料必須位於允許的工作區內；可將初始化目標選為該專案下尚不存在的 `data` 目錄。範本儲存庫仍與私人資料分開。
- Gateway 使用 `mode: local`、`bind: loopback`、獨立連接埠及 `auth.mode: token`；產生測試專用權杖，不使用公開範例字串作為權杖。
- 所有測試指令均使用獨立的 `OPENCLAW_STATE_DIR`、`OPENCLAW_CONFIG_PATH`；codex runtime 另使用獨立 `CODEX_HOME`。登入應依該版本支援的方式完成，不要把憑證寫進範本或 AGENTS.md。

設定與登入完成後，在已套用上述測試環境變數的終端機以前景程序啟動，例如：

```sh
openclaw gateway run --port 29789 --bind loopback
```

請先確認連接埠未使用，並與其他 Gateway 基底連接埠保留至少 120 的間隔。用獨立瀏覽器設定檔開啟 `http://127.0.0.1:29789/`，在 Gateway 密鑰欄輸入測試權杖，連線後於 WebChat 提問。不要使用正式瀏覽器登入狀態，也不要執行服務安裝、正式 Gateway 重啟或 `--force`。

### Hermes 桌面自動載入設定

關鍵是「工作階段實際目錄」指向含 AGENTS.md 的專案。本次同時設定下列三處，沒有證明其中任一處單獨就足夠：

1. 獨立 `HERMES_HOME/config.yaml` 中的工作目錄（合併欄位，不取代模型等設定）：

   ```yaml
   terminal:
     cwd: "<PROJECT_ROOT>"
   ```

2. 獨立 Electron userData 下的 `project-dir.json`：

   ```json
   { "dir": "<PROJECT_ROOT>" }
   ```

3. 啟動測試桌面時設定 `HERMES_DESKTOP_CWD=<PROJECT_ROOT>`。

隔離時另指定不同的 `HERMES_HOME`、`HERMES_DESKTOP_USER_DATA_DIR` 與 `HERMES_DESKTOP_APP_NAME`。本次也使用獨立 HOME、CODEX_HOME、來源建置副本，並以 `HERMES_DESKTOP_HERMES_ROOT` 指向該副本；單改 HERMES_HOME 不足以隔離 Electron 狀態。這些是已驗收來源版本的設定方式，其他版本請先核對是否支援。

設定完成後確認桌面顯示正確專案目錄，再建立新工作階段。原生資料夾選擇器的點選流程未實測；本次直接準備隔離設定檔，並比對工作階段資料庫的 cwd。共用資料可在專案目錄外，但仍須符合你設定的檔案存取範圍。

### 自行重測與收尾

在虛構資料的 `knowledge/project.md` 加入測試用隨機驗收碼後，從介面詢問：

```text
請回報本專案的名稱、目前狀態、驗收碼，以及你使用的資料來源。
僅查詢，不修改任何檔案。
```

不要在提問中附上路徑或答案。確認第一輪讀取正確後，由你修改測試資料的狀態與驗收碼，再開全新對話。要驗證指標更新，可保留舊資料，將 AGENTS.md 改指向另一份測試資料後重測；新回答應來自新位置。

本次隔離屬應用程式狀態隔離，不是虛擬機或完整檔案系統沙箱，模型推論仍會連線。測試後關閉測試程序，移除測試登入、瀏覽器設定檔及暫存狀態。受追蹤的正式設定／登入檔雜湊比對未變，不代表已稽核整台電腦的所有檔案。

## 填入自己的資料

只修改私人目錄裡的 `policy.md` 與 `knowledge/project.md`，保留文件 metadata，更新來源與查證日期，再執行 workspace 驗證。範本內的 `examples/` 保持虛構資料。具體備份及回復步驟見 [維護說明](docs/maintenance.md)。

## 收錄內容

| 位置 | 用途 |
|---|---|
| [examples/workspace/](examples/workspace/README.md) | 虛構私人工作目錄樣本 |
| [adapters/](adapters/README.md) | Codex、Hermes、OpenClaw 的接入指引 |
| [recipes/](recipes/README.md) | 維護、交接與候選審閱 |
| [scripts/](scripts/README.md) | 初始化與驗證 |
| [docs/design.md](docs/design.md) | 資料邊界與來源時效 |
| [docs/maintenance.md](docs/maintenance.md) | 更新、備份與回復 |
| [docs/release-review.md](docs/release-review.md) | 發布前審閱清單 |

通用範本可更新；使用者的資料保留在獨立目錄。請勿把私人目錄上傳作為範例。驗證成功只代表工具列出的檢查通過，不保證內容沒有敏感資訊，也不證明 agent 遵守文件規則。
