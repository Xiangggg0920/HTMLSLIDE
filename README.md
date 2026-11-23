# 認識 TWICE｜LLM Wiki 與教學簡報

這個繁體中文專案讓第一次接觸 TWICE 的讀者認識團體出道背景、九位成員與入門作品。第 2 頁保留出道背景，並依發行類別與年份列出 48 首團體主打與單曲。12 頁簡報由 Wiki 條目產生，每頁都可以回到對應的條目與原始來源。

| 交付內容 | 入口 |
| --- | --- |
| 教學 HTML 簡報 | [index.html](index.html) |
| LLM Wiki | [總索引](wiki/index.html) · [團體條目](wiki/group.html) |
| 資料來源 | [查閱來源與收錄筆記](wiki/sources.html) |
| 工作流程圖 | [從收錄資料到逐頁與整份檢查](workflow.jpg) |
| 實際執行、檢查與反思 | [檢查報告](qa-report.md) |
| 後續維護與部署 | [AGENTS.md](AGENTS.md) |

## 開啟與操作

在瀏覽器開啟最外層的 `index.html`。可點選上一頁、下一頁或下拉選單，也可用左右方向鍵翻頁，Home / End 跳到首尾。網址的片段可直接連到指定頁，例如 `index.html#tzuyu`。

## LLM Wiki 如何運作

本專案參考 [Karpathy 的 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。來源層 `sources/index.json` 保留官方原始網址、查閱日期及收錄筆記。知識層 `wiki/entries.json` 維護團體與九位成員的結構化條目，再生成瀏覽用 Wiki 與簡報。中文 `AGENTS.md` 描述資料格式、更新工作和檢查方式。實際查核記錄在 `qa-report.md`。

照片包含使用者提供的團照及六張成員照。定延、多賢、彩瑛的照片取自 [JYP 官方成員頁](https://twice.jype.com/profile)。成員頁配色依使用者提供的對照表，色碼為網頁用近似值。

## 更新與 GitHub Pages

修改來源或 Wiki 後，在專案根目錄執行 `python build.py`，再執行 `python build.py --check`。Python 只用於更新生成檔，瀏覽與部署都可直接使用現成的 HTML。

自行上傳時，保留根目錄的 `index.html`、`.nojekyll` 及各資料夾。在 GitHub 儲存庫的 **Settings → Pages** 選擇 **Deploy from a branch**，指定上傳的分支與 **/ (root)** 後儲存。GitHub Pages 產生網址後，可用根網址開啟簡報，或加上 `wiki/index.html` 開啟 Wiki。[GitHub Pages 官方步驟](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
