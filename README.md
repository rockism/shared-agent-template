# shared-agent-template

- Version：0.1.0-candidate
- Last Update：2026-10-31
- Purpose：Shared Agent Template

多個 AI agent 共用文件與操作指南的本機範本。適合願意維護 Markdown、希望減少知識副本漂移的使用者。

目前為初期預覽版，採用 [MIT 授權](LICENSE)。沒有自動同步、常駐服務或憑證管理功能。適用 Python 3.10 以上；腳本只使用標準函式庫。

## 下載

```sh
git clone https://github.com/rockism/shared-agent-template.git
cd shared-agent-template
```

也可以在 GitHub 點選 Code → Download ZIP，解壓縮後開啟終端機並切換到專案目錄。

## 快速開始

在此專案目錄執行：

```sh
python3 scripts/validate.py template .
python3 scripts/init_workspace.py "$HOME/shared-agent-data-demo"
python3 scripts/validate.py workspace "$HOME/shared-agent-data-demo"
```

初始化只接受尚不存在的目標目錄，不覆寫既有資料。目標目錄不得位於範本內；私人資料與公開範本分開管理。先用 demo 目錄試用，確認後再自行選定正式路徑。後續不需重新初始化。

選讀 [adapter 指引](adapters/README.md)，把私人工作目錄的絕對路徑填入自己的 agent 入口。請 agent 讀取私人目錄的 README，請它說明範例專案狀態與來源日期，確認讀到檔案後才開始使用。此步驟需在各平台實測。

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
