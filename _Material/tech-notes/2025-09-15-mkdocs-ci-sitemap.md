# MkDocs CI 與 Sitemap 技術總結（2025-09-15）

目的

- 讓 GitHub Actions 穩定建置 MkDocs，並在無外掛情況下產生 sitemap.xml。
- 避免路徑不一致、外掛相容性、與 YAML 解析等問題。

關鍵決策

- MkDocs 版本：升到 1.6+，不依賴 sitemap 外掛（以建置後腳本產生 sitemap）。
- 建置路徑：在 `mkdocs/` 目錄內執行 build，輸出固定在 `mkdocs/site/`。
- Sitemap 產生：建置完成後以 Python 掃描 HTML，寫入 `sitemap.xml`。
- 解析 `site_url`：用正則讀取 `mkdocs/mkdocs.yml`，避免 PyYAML 與 `!!python/name:` 擴充標籤衝突。
- 資產完整：移除 `extra_javascript` 中不存在的檔案，避免建置找不到資源。

主要修正點

- `.github/workflows/deploy.yml`
  - 安裝：`pip install -r requirements.txt`（MkDocs 1.6+）。
  - 建置：`cd mkdocs && mkdocs build -f mkdocs.yml` → 輸出到 `mkdocs/site/`。
  - 產生 sitemap：以 inline Python 掃描 `mkdocs/site/**/*.html`，寫入 `mkdocs/site/sitemap.xml`。
  - 列出成果並上傳 artifact：以 `mkdocs/site/` 為準，檢查 `mkdocs/site/index.html` 存在。
- `scripts/generate_sitemap.py`
  - 本地同樣邏輯，可對 `mkdocs/site/` 產生 `sitemap.xml`。
- `mkdocs/mkdocs.yml`
  - 刪除不存在的 `assets/judgment-redirect.html`、`assets/fjud-oneclick.js` 引用。

根因與踩雷

- Sitemap 外掛混淆：誤以為內建；實際上 1.6+ 需外掛或自行產生。嘗試的第三方套件名稱不存在，導致安裝失敗。
- 路徑不一致：有時寫入 `site/`、有時寫入 `mkdocs/site/`，檢查與上傳指向不同資料夾，找不到 `index.html`。
- YAML 解析：`mkdocs.yml` 使用 `!!python/name:`（pymdownx），`safe_load` 無法解析 → 以正則改讀 `site_url`。
- Inline 腳本 `__file__`：在 Actions 內沒有檔名可參考，導致路徑推算錯誤。
- Docker entrypoint：`squidfunk/mkdocs-material` 的 entrypoint 是 `mkdocs`，不能直接 `sh -lc`，需改用 `--entrypoint sh` 或在主機執行附加步驟。

現在的正確流程（CI）

- 安裝：`pip install -r requirements.txt && mkdocs --version`
- 建置：
  - `cd mkdocs && mkdocs build -f mkdocs.yml && cd -`
- 產生 sitemap：
  - 掃描 `mkdocs/site/**/*.html` → 產生 `mkdocs/site/sitemap.xml`
- 上傳：`actions/upload-pages-artifact` 指向 `mkdocs/site/`

本地等效指令

- 建置：`(cd mkdocs && mkdocs build -f mkdocs.yml)`
- 產生 sitemap：`python3 scripts/generate_sitemap.py --config mkdocs/mkdocs.yml --site-dir mkdocs/site`
- 預覽（Docker）：`docker compose up -d docs` → <http://127.0.0.1:11413>

GitHub Actions 歷史清理

- 刪除失敗的 runs（不支援 `-y` 版）：
  - `gh run list -R mt019/1141_Tariff -w "Build and Deploy MkDocs" --status failure --limit 1000 --json databaseId --jq '.[].databaseId' | xargs -n1 -I{} gh api -X DELETE repos/mt019/1141_Tariff/actions/runs/{}`
- 依日期刪除：
  - `gh run list -R mt019/1141_Tariff --limit 1000 --json databaseId,createdAt --jq '.[] | select(.createdAt < "2025-09-15T00:00:00Z") | .databaseId' | xargs -n1 -I{} gh api -X DELETE repos/mt019/1141_Tariff/actions/runs/{}`

未來最佳化（可選）

- 在 sitemap 步驟前新增守門：若 `mkdocs/site/*.html` 為 0 則 fail，避免只上傳 `sitemap.xml`。
- 若要升到 MkDocs 2.x 或改變主題外掛，保留「建置後產生 sitemap」策略，可最大限度避免外掛相容性問題。

備註

- 這份 MD 存在 `_Material/` 下，不會被網站收錄或顯示（純內部備忘）。

