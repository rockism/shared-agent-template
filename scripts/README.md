# 工具說明

- Version：0.1.0-candidate
- Last Update：2026-10-31
- Purpose：工具說明

`init_workspace.py DEST`：以虛構樣本建立尚不存在、位於範本外的私人目錄，拒絕覆寫。建立前會驗證範本。

`validate.py template ROOT`：檢查 manifest 白名單與雜湊、必要檔案、metadata、相對連結、symlink 與有限的高風險標記。

`validate.py workspace ROOT`：檢查私人目錄的必要檔案、metadata 與相對連結，不輸出檔案內容。

`test_tools.py`：在暫存目錄測試初始化、重複初始化、任意工作目錄執行，以及驗證失敗案例。
