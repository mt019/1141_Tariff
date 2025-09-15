# 1141 關稅法專題研究

> MkDocs + Material 驅動的課程筆記網站，含 Jupyter 輔助與自動部署。

- 線上網站：<https://mt019.github.io/1141_Tariff/>
- 技術重點：Material 主題、Jupyter 轉換、Sitemap/RSS/Canonical、GitHub Pages 部署

---

## 快速開始（TL;DR）

- Docker（推薦）：
  - 啟動文件站台：`docker compose up -d docs` → 開 `http://127.0.0.1:11413`
  - 更新環境後重建：`docker compose build docs`
  - 停止：`docker compose down`

- Python（本機環境）：
  - 安裝：`pip install -r requirements.txt`
  - 開發預覽：`mkdocs serve -f mkdocs/mkdocs.yml -a 127.0.0.1:11413`
  - 編譯輸出：`mkdocs build -f mkdocs/mkdocs.yml`

---

## 內容撰寫規範（Front Matter）

每篇重點頁面建議補齊 YAML Front Matter，提升 SEO 與 RSS 資訊品質：

```yaml
---
title: 關稅估價（CVA）概要
description: 本頁整理 WTO CVA 與關稅法估價條文的對應與適用順序
date: 2024-09-08
updated: 2024-09-12
keywords: [關稅估價, CVA, 關稅法]
---
```

- title/description：用於 `<title>` 與 Open Graph/SEO 摘要
- date/updated：供 RSS 使用（亦可由 Git 推算）
- keywords：可覆蓋全站預設關鍵字（見 `mkdocs/overrides/main.html`）

---

## SEO 與收錄

本專案已啟用：
- Sitemap：MkDocs 內建 `sitemap` 外掛，輸出 `sitemap.xml`
- RSS：`mkdocs-rss-plugin` 輸出 `feed.xml`
- Canonical/Keywords/OG：在 `mkdocs/overrides/main.html` 注入常見 SEO 標籤
- robots.txt：允許索引並指向 sitemap（`mkdocs/My_Notes/robots.txt`）

檢查清單：
- `mkdocs/mkdocs.yml` 設定正確的 `site_url`
- 發佈後檢查：`/sitemap.xml`、`/feed.xml`、首頁無 `noindex`
- Search Console：建立屬性 → 提交 `https://<user>.github.io/<repo>/sitemap.xml`，並對首頁與重點頁「要求編入索引」

---

## 本地開發（進階）

- 常用指令（Docker）：
  - 追日誌：`docker compose logs -f docs`
  - 重新建站：`docker compose build docs && docker compose up -d docs`

- 常用指令（Python）：
  - 安裝：`pip install -r requirements.txt`
  - 預覽：`mkdocs serve -f mkdocs/mkdocs.yml -a 127.0.0.1:11413`

---

## Jupyter（快速開啟 URL）

- 服務埠：`127.0.0.1:11414`
- 一鍵腳本：`bash scripts/jupyter_url.sh` → 輸出可直接開啟的 URL
- 不用腳本：`docker compose up -d jupyter && echo "http://127.0.0.1:11414/lab"`
- 目前為本地開發方便，預設不啟用 token/password；若啟用，腳本會印出含 token 的 URL

---

## 筆記修正工具（Markdown 助手）

- `notebooks/md-fix.ipynb`：
  - 將 `第…條`/`第…項` 中文數字轉阿拉伯數字
  - 補齊清單前必要空行，避免 Markdown 解析問題
  - 支援遞迴處理與目錄樹輸出

- CLI 版本：
  - `python3 fix_cn_ordinals.py -v mkdocs/My_Notes`（試跑：加 `--dry-run`）
  - 批次包裝：`bash fix_cn_ordinals_all.sh`

小技巧（Docker）：為讓 Notebook 看得到整個專案，於 `jupyter` 服務掛載 `- ./:/home/jovyan/work`。

---

## 專案結構

```text
.
├─ docker-compose.yml           # 服務：docs (MkDocs), jupyter
├─ README.md
├─ scripts/
│  └─ jupyter_url.sh            # 一鍵啟動 Jupyter 並輸出 URL
├─ fix_cn_ordinals.py           # CLI：第…條/項 轉換
├─ fix_cn_ordinals_all.sh       # 批次執行轉換
├─ notebooks/
│  └─ md-fix.ipynb              # 一鍵修正 Notebook 版本
├─ mkdocs/
│  ├─ mkdocs.yml                # MkDocs 設定（Material/SEO/RSS 等）
│  ├─ Dockerfile                # 建置含外掛的環境
│  └─ My_Notes/                 # 站內內容（docs_dir）
│     ├─ index.md
│     ├─ assets/                # JS/CSS/輔助
│     └─ 01課程筆記/…          # 課程筆記 Markdown
├─ _Material/                   # 課程教材（PDF 等）
└─ .github/
   └─ workflows/
      └─ deploy.yml             # GitHub Pages 部署
```

備註
- MkDocs 入口為 `mkdocs/mkdocs.yml`，其中 `docs_dir: My_Notes`
- Sitemap/RSS/robots/canonical 已就緒；請務必設定正確 `site_url`
- Notebook 修正工具支援遞迴與目錄樹顯示，以利檢查掛載是否正確

---

## CI 部署（GitHub Pages）

- Workflow：`.github/workflows/deploy.yml`
  - 取完整 git 歷史（供 RSS 取用）
  - 安裝 MkDocs + 外掛並以 `mkdocs/mkdocs.yml` 建站
  - 部署至 Pages（Repo Settings → Pages → Source = GitHub Actions）

- 上線後檢查：
  - `https://<user>.github.io/<repo>/sitemap.xml`
  - `https://<user>.github.io/<repo>/feed.xml`

---

## 疑難排解

- `/sitemap.xml` 或 `/feed.xml` 404：
  - 確認 `mkdocs/mkdocs.yml` 已啟用 `sitemap`、`rss`，且 `site_url` 正確
  - 重建環境：`docker compose build docs`
  - 若無 commit 歷史，RSS 日期可能缺乏；可加上 `date:` 或先建立至少一次提交

- 首頁或全站未被索引：
  - 檢查是否有 `noindex` 標頭/標籤（`curl -I` 檢查）
  - 於 Search Console 手動「要求編入索引」並等待數日至數週
