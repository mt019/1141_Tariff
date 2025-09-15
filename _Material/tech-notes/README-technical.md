# 站台開發與部署手冊（Internal）

說明：此為本 repo 的技術版 README，集中維護開發、部署、SEO、CI 的細節；不顯示在對外網站，僅供維護者參考。

---

## TL;DR

- Docker（推薦）：
- 
  - 啟動：`docker compose up -d docs` → 開 `http://127.0.0.1:11413`
  - 重建：`docker compose build docs`
  - 停止：`docker compose down`

- Python（本機）：
- 
  - 安裝：`pip install -r requirements.txt`
  - 預覽：`mkdocs serve -f mkdocs/mkdocs.yml -a 127.0.0.1:11413`
  - 編譯：`mkdocs build -f mkdocs/mkdocs.yml`

---

## 內容撰寫規範（Front Matter）

在重點頁面補齊 YAML Front Matter，可改善 SEO 與 RSS：

```yaml
---
title: 關稅估價（CVA）概要
description: 本頁整理 WTO CVA 與關稅法估價條文的對應與適用順序
date: 2024-09-08
updated: 2024-09-12
keywords: [關稅估價, CVA, 關稅法]
---
```

- title/description：對應 `<title>` 與摘要
- date/updated：供 RSS 與新鮮度訊號
- keywords：會與全站 `extra.keywords` 合併去重

---

## SEO 與收錄

- Canonical/OG/Twitter/keywords/robots：`mkdocs/overrides/main.html` 已注入
- RSS：`mkdocs-rss-plugin` 產生 `rss.xml`
- Sitemap：建置後在 CI 以 Python 產生 `sitemap.xml`
- robots.txt：`mkdocs/My_Notes/robots.txt` 指向 sitemap
- Search Console：於 `mkdocs/mkdocs.yml: extra.google_site_verification` 放驗證 token

檢查要點：

- `mkdocs/mkdocs.yml` 設正確 `site_url`
- 發佈後確認 `/sitemap.xml`、`/rss.xml` 存在

延伸說明：見 `_Material/tech-notes/2025-09-15-mkdocs-ci-sitemap.md`。

---

## 本地開發

- Docker 常用：
- 
  - 日誌：`docker compose logs -f docs`
  - 重建：`docker compose build docs && docker compose up -d docs`

- Python 常用：
- 
  - 安裝：`pip install -r requirements.txt`
  - 預覽：`mkdocs serve -f mkdocs/mkdocs.yml -a 127.0.0.1:11413`

---

## Jupyter（輔助）

- 服務埠：`127.0.0.1:11414`
- 一鍵：`bash scripts/jupyter_url.sh`
- 直接啟動：`docker compose up -d jupyter && echo "http://127.0.0.1:11414/lab"`

---

## Markdown/Notebook 助手

- `notebooks/md-fix.ipynb`：中文數字轉換、清單空行修補
- CLI：`python3 fix_cn_ordinals.py -v mkdocs/My_Notes`（試跑加 `--dry-run`）

---

## 專案結構

```text
.
├─ docker-compose.yml           # 服務：docs (MkDocs), jupyter
├─ README.md                    # 對外（課程）說明
├─ _Material/tech-notes/        # 技術文件（本檔所在）
├─ scripts/
├─ notebooks/
├─ mkdocs/
│  ├─ mkdocs.yml                # 站台設定
│  ├─ overrides/main.html       # SEO/OG/robots/RSS 等 head 模板
│  └─ My_Notes/                 # 內容（docs_dir）
└─ .github/workflows/deploy.yml # Pages 部署工作流
```

備註：`docs_dir` 設為 `My_Notes`，入口為 `mkdocs/mkdocs.yml`。

---

## CI（GitHub Pages）

- Workflow：`.github/workflows/deploy.yml`
  - 安裝需求 → `mkdocs build`
  - 產生 `sitemap.xml`
  - 上傳 `mkdocs/site/` 至 Pages

上線檢查：

- `https://<user>.github.io/<repo>/sitemap.xml`
- `https://<user>.github.io/<repo>/rss.xml`

---

## 疑難排解

- `sitemap.xml`/`rss.xml` 404：檢查建置是否成功、`site_url` 是否正確
- 未被索引：檢查是否 `noindex`，於 Search Console 要求編入索引

