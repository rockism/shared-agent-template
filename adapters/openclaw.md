# Openclaw Adapter

- Version：0.1.0-candidate
- Last Update：2026-10-31
- Purpose：Openclaw Adapter

將下列文字加入你已確認會被該 agent 讀取的專案指引或工作提示；先將占位符換成實際絕對路徑。

```text
共用私人資料位於 <PRIVATE_WORKSPACE>。
先讀該目錄 README.md 與 policy.md，再按任務讀必要來源。
通用流程位於 <TEMPLATE_ROOT>/recipes/，按需讀取。
私人記憶保留來源指標；不要複製易變狀態。
候選資料不是正式事實；不得自行採納或擴大授權。
```

請先在一次新對話中，要求 agent 說明虛構專案、資料來源與日期。確認其實際讀取正確目錄；能找到路徑不等於入口已載入。不需建立 symlink。平台入口設定請依目前安裝版本核對。
