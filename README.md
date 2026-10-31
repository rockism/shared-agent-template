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
