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
