# TWICE LLM Wiki 維護指引

## 專案目標

維護繁體中文 TWICE 入門知識庫及教學 HTML 簡報。首次觀看者應能說出團體人數與出道背景，並透過成員頁認識九位成員與入門作品。

## 檔案與資料格式

- `sources/index.json` 是收錄層。每筆保存唯一的 `id`、`title`、原始 `url`、`summary` 及查閱日期 `checked`（YYYY-MM-DD）。使用者提供的離線資料可以省略網址內容，並在摘要描述來源。
- `wiki/entries.json` 是知識層。團體資料放在 `group`，成員放在 `members`。增修主打歌時，在 `group.track_groups` 維護發行類別、年份、原始曲名和來源 ID，並同步更新收錄範圍與查閱日期。每位成員使用固定的英文小寫 `id`，並記錄中英文藝名、生日、應援色名與色碼、入門介紹、試聽曲和來源 ID。
- `build.py` 產生根目錄 `index.html` 與 `wiki/*.html`。更新時修改資料或生成模板。畫面樣式與導覽行為分別放在 `assets/site.css`、`assets/slides.js`。
- `image/` 以全小寫的成員 ID 和副檔名命名個人照，例如 `jeongyeon.jpg`。團照使用 `twice.jpg`。更換照片時先核對人名與素材出處，再檢查桌面和窄螢幕的裁切。部署前用 `git ls-files -- image` 核對檔名大小寫與 HTML 引用完全一致。
- `workflow.jpg` 保存流程圖。依實際執行結果，將日期、變更、檢查與反思追加到 `qa-report.md`。

## 新增內容

成員頁的 `highlight` 記錄作品亮點，`works` 以年份、作品、說明、來源 ID 的順序維護作品紀錄。`anniversary_solo` 保存十週年專輯的獨唱曲名，`listening_note` 提供聆聽角度。團體條目的 `milestones` 和 `routes` 保存年表與聆聽路線，也各自附來源 ID。

1. 先閱讀 Wiki 索引及對應條目，找出需要新增或修正的事實。查閱官方成員頁、唱片資料或發行公告，並將可核對的內容收錄到來源層。
2. 更新團體或成員條目並填上來源 ID。日期或作品名稱有出入時，先查原始頁面再更新。應援色以本專案附表為準。
3. 以 Wiki 為依據完成一頁，執行 `python build.py` 並開啟該頁。立即核對事實、來源、照片、顏色、桌面與手機版面。資料有誤回 Wiki，版面或導覽有誤回模板或資產，修完重查。
4. 所有頁面完成後，從封面走到回顧頁，檢查首尾邊界、鍵盤、選單、直接網址及 Wiki 往返。執行 `python build.py --check`，確認輸出與資料一致，再把實際結果寫入檢查報告。

## 手動部署

保留相對路徑、根目錄 `index.html` 和 `.nojekyll`。上傳生成的 HTML 及資產後，在 GitHub Pages 使用部署分支的 `/(root)`。目前由專案所有者執行上傳。網站上線後，開啟根網址、Wiki 和至少一個投影片深層連結確認部署。
