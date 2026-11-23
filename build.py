"""以 Wiki 條目產生可直接部署的靜態 HTML。"""
import argparse
from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))

wiki = read("wiki/entries.json")
sources = read("sources/index.json")
source_map = {source["id"]: source for source in sources}
group = wiki["group"]
members = wiki["members"]
e = escape

def document(title, body, prefix="", slides=False):
    script = '<script src="assets/slides.js" defer></script>' if slides else ""
    return f"""<!doctype html>
<!-- 由 build.py 產生。 -->
<html lang="zh-Hant">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><link rel="stylesheet" href="{prefix}assets/site.css">{script}</head>
<body>{body}</body></html>
"""

def references(ids):
    return "".join(f'<li><a href="sources.html#{e(key)}">{e(source_map[key]["title"])}</a></li>' for key in ids)

def editorial_list(items, source_path, show_sources=True):
    rows = []
    for heading, description, keys in items:
        citations = ""
        if show_sources:
            links = " · ".join(
                f'<a href="{source_path}#{e(key)}">{e(source_map[key]["title"])}</a>' for key in keys
            )
            citations = f'<span class="entry-sources">{links}</span>'
        rows.append(f'<li><strong>{e(heading)}</strong><p>{e(description)}</p>{citations}</li>')
    return f'<ul class="editorial-list">{"".join(rows)}</ul>'

def track_catalog(source_path):
    categories = []
    for category in group["track_groups"]:
        years = []
        for year, titles in sorted(category["years"].items()):
            songs = "".join(f'<li>{e(title)}</li>' for title in titles)
            years.append(f'<div class="track-year"><h3>{e(year)}</h3><ul>{songs}</ul></div>')
        count = sum(len(titles) for titles in category["years"].values())
        refs = " · ".join(
            f'<a href="{source_path}#{e(key)}">{e(source_map[key]["title"].split("｜", 1)[-1])}</a>'
            for key in category["sources"]
        )
        categories.append(
            f'<details open class="track-category"><summary>{e(category["label"])}'
            f' <span>（{count} 首）</span></summary>{"".join(years)}'
            f'<p class="track-sources">查證來源 {refs}</p></details>'
        )
    return (
        f'<p class="track-scope">資料查閱至 <time datetime="{e(group["tracks_checked"])}">'
        f'{e(group["tracks_checked"])}</time>。{e(group["track_scope"])}</p>'
        f'<div class="track-catalog">{"".join(categories)}</div>'
    )

def photo(member):
    for extension in ("jpg", "png", "webp"):
        path = f'image/{member["id"]}.{extension}'
        if (ROOT / path).is_file():
            return f'<img src="{path}" alt="{e(member["english"])} 個人照">'
    return f'<div class="portrait-placeholder"><strong>{e(member["english"])}</strong><span>個人照待補</span></div>'

def slide(key, label, title, content, destination, accent="#ff9faa", visual=""):
    picture = f'<div class="visual">{visual}</div>' if visual else ""
    layout = "split" if visual else "full"
    return f"""<section class="slide {layout}" id="{key}" data-slide style="--accent:{accent}" aria-labelledby="{key}-title">
<div class="copy"><p class="eyebrow">{label}</p><h1 id="{key}-title" tabindex="-1">{title}</h1>
{content}<a class="text-link" href="{destination}">閱讀 Wiki 條目</a></div>{picture}</section>
"""

def generate():
    group_url = "wiki/group.html"
    group_photo = '<img src="image/twice.jpg" alt="TWICE 團體合照">'
    milestones = [(f"{year}｜{title}", note, keys) for year, title, note, *keys in group["milestones"]]
    routes = [(title, f"{songs}。{note}", keys) for title, songs, note, *keys in group["routes"]]
    deck_milestones = editorial_list(milestones, "wiki/sources.html", show_sources=False)
    group_facts = '<dl class="facts"><div><dt>團體人數</dt><dd>9 位</dd></div><div><dt>韓國出道</dt><dd>2015 年</dd></div><div><dt>日本出道</dt><dd>2017 年</dd></div></dl>'
    group_intro = (f'<p class="lead">{e(group["description"])}</p>{group_facts}'
                   '<p>從韓國團體主打、日本發行到英文單曲，TWICE 也透過小分隊和個人作品呈現不同的演唱組合。</p>'
                   '<a class="primary" href="#debut">開始簡報</a>')
    lineup = "".join(
        f'<li><a href="#{m["id"]}" style="--swatch:{m["hex"]}">{e(m["english"])}</a></li>' for m in members
    )
    slides = [
        slide("intro", "團體介紹", "認識<br>TWICE", group_intro, group_url, visual=group_photo),
        slide("debut", "團體沿革", "出道與主打歌",
              f'<p class="lead">{e(group["debut"])}</p><details><summary>展開團體發展年表</summary>{deck_milestones}</details>'
              + track_catalog("wiki/sources.html"), group_url, "#ffb48f"),
    ]
    entries = {}
    group_members = []
    for member in members:
        key = member["id"]
        name = e(member["name"])
        english = e(member["english"])
        color = e(member["color"])
        hex_code = member["hex"]
        url = f"wiki/{key}.html"
        facts = f'<dl class="facts"><div><dt>生日</dt><dd><time datetime="{member["birthday"]}">{member["birthday"]}</time></dd></div><div><dt>應援色</dt><dd><i class="swatch"></i>{color}</dd></div></dl>'
        title = english if name == english else f'{name}<span>{english}</span>'
        listen = f'<p class="listen"><b>入門試聽</b> {e(member["listen"])}</p>'
        detail = f'<p class="lead">{e(member["detail"])}</p>'
        highlight = member.get("highlight")
        if highlight:
            detail += f'<p class="member-highlight"><strong>作品亮點</strong> {e(highlight)}</p>'
        works = [(f"{year}｜{work}", note, keys) for year, work, note, *keys in member["works"]]
        solo = member["anniversary_solo"]
        solo_note = f'<p><strong>十週年獨唱</strong> 〈{e(solo)}〉，收錄於《TEN: The Story Goes On》。</p>'
        slide_works = editorial_list(works, "wiki/sources.html", show_sources=False)
        more = f'<details><summary>展開作品與創作紀錄</summary>{slide_works}</details>'
        listening = f'{listen}<p>{e(member["listening_note"])}</p>'
        slides.append(slide(key, "成員介紹", title, facts + detail + solo_note + listening + more, url, hex_code, photo(member)))
        related = ""
        if key in {"momo", "sana", "mina"}:
            related = '<p>小分隊關聯 ' + "、".join(
                f'<a href="{other["id"]}.html">{e(other["english"])}</a>'
                for other in members if other["id"] in {"momo", "sana", "mina"} and other["id"] != key
            ) + '</p>'
        entries[f"wiki/{key}.html"] = wiki_page(
            member["english"],
            f'<article style="--accent:{hex_code}"><h1>{title}</h1>{facts}{detail}'
            f'<h2>代表作品與創作紀錄</h2>{editorial_list(works, "sources.html")}{solo_note}'
            '<p><a href="sources.html#ten">十週年專輯曲目來源</a></p>'
            f'<h2>聆聽指南</h2>{listening}{related}'
            f'<p><a href="group.html">TWICE 團體條目</a> · <a href="../index.html#{key}">對應簡報頁</a></p>'
            f'<h2>資料來源</h2><ul>{references(member["sources"])}</ul></article>',
        )
        group_members.append(f'<li><a href="{key}.html">{english}</a></li>')
    misamo = ', '.join(f'<a href="{key}.html">{key.upper()}</a>' for key in ("momo", "sana", "mina"))
    entries[group_url] = wiki_page(
        "TWICE 團體", f'<article><h1>TWICE 團體</h1><p>{e(group["description"])}</p><h2>出道與作品</h2>'
        f'<p>{e(group["debut"])}</p><h2>團體發展年表</h2>{editorial_list(milestones, "sources.html")}'
        f'<h2>團體主打歌</h2>{track_catalog("sources.html")}<h2>小分隊 MISAMO</h2>'
        f'<p>由 {misamo} 組成。可從《Masterpiece》的〈Do not touch〉聽起，再聽《HAUTE COUTURE》各成員在不同版本裡的獨唱，最後接到第一張日本正規專輯《PLAY》。</p>'
        '<p><a href="sources.html#misamo">Masterpiece</a> · <a href="sources.html#haute-couture">HAUTE COUTURE</a> · '
        '<a href="sources.html#play">PLAY</a></p>'
        f'<h2>三條入門聆聽路線</h2>{editorial_list(routes, "sources.html")}'
        f'<h2>九位成員</h2><ul>{"".join(group_members)}</ul><p><a href="../index.html#intro">團體簡報</a> · '
        f'<a href="../index.html#debut">出道簡報</a> · <a href="../index.html#recap">回顧簡報</a></p>'
        f'<h2>資料來源</h2><ul>{references(group["sources"])}</ul></article>',
    )
    entries["wiki/index.html"] = wiki_page(
        "TWICE LLM Wiki", '<h1>TWICE LLM Wiki</h1><p class="lead">從出道背景、入門作品與個人活動認識 TWICE。</p>'
        f'<h2>團體</h2><p><a href="group.html">TWICE 團體條目</a></p><h2>成員</h2><ul class="wiki-lineup">{"".join(group_members)}</ul>'
        '<h2>查證與維護</h2><ul><li><a href="sources.html">來源索引</a></li>'
        '<li><a href="../workflow.jpg">工作流程</a></li><li><a href="../qa-report.md">檢查報告與維護紀錄</a></li></ul>',
    )
    records = []
    for source in sources:
        link = f'<p><a href="{e(source["url"])}">查看原始來源</a></p>' if source["url"] else ""
        records.append(f'<article id="{e(source["id"])}"><h2>{e(source["title"])}</h2>'
                       f'<p>{e(source["summary"])}</p><small>查閱日期 {e(source["checked"])}</small>{link}</article>')
    entries["wiki/sources.html"] = wiki_page("資料來源", '<h1>資料來源</h1>' + "".join(records))

    recap = ('<p class="lead">九位成員，2015 年在韓國出道。認識成員後，可以用下面三條路線比較不同時期與演唱組合。</p>'
             f'<ul class="lineup">{lineup}</ul>{editorial_list(routes, "wiki/sources.html", show_sources=False)}'
             '<details><summary>小測驗：MISAMO 由哪三位成員組成？</summary><p>MOMO、SANA、MINA。</p></details>'
             '<details><summary>小測驗：《TEN》共有幾首成員獨唱？</summary><p>九首，每位成員各一首。專輯另有團體主打〈ME+YOU〉。</p></details>')
    slides.append(slide("recap", "重點回顧", "你記得哪一位？", recap, group_url))
    options = "".join(f'<option value="{key}">{e(label)}</option>' for key, label in
                      [("intro", "團體介紹"), ("debut", "出道與主打歌"), *[(m["id"], m["english"]) for m in members], ("recap", "重點回顧")])
    header = '<header class="top"><a class="brand" href="#intro">TWICE<span>.</span></a><nav aria-label="專案導覽"><a href="wiki/index.html">Wiki</a><a href="workflow.jpg">工作流程</a></nav></header>'
    controls = f'''<footer class="controls" hidden><button type="button" id="previous">上一頁</button>
<label class="jump"><span class="sr-only">跳到投影片</span><select id="jump">{options}</select></label>
<span id="counter" aria-live="polite"></span><button type="button" id="next">下一頁</button></footer>'''
    entries["index.html"] = document("認識 TWICE｜入門簡報", header + '<main class="deck">' + "".join(slides) + '</main>' + controls, slides=True)
    return entries

def wiki_page(title, content):
    header = '<header class="top"><a class="brand" href="index.html">TWICE Wiki</a><nav aria-label="專案導覽"><a href="../index.html">簡報</a><a href="sources.html">來源</a></nav></header>'
    return document(f"{title}｜TWICE Wiki", header + f'<main class="reading">{content}</main>', "../")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="檢查 HTML 是否與 Wiki 資料一致")
    check = parser.parse_args().check
    stale = []
    for name, html in generate().items():
        path = ROOT / name
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != html:
                stale.append(name)
        else:
            path.write_text(html, encoding="utf-8")
    if stale:
        parser.exit(1, "HTML 需要重新產生： " + ", ".join(stale) + "\n")
    print("HTML 與 Wiki 一致" if check else "已產生簡報與 Wiki HTML")

if __name__ == "__main__":
    main()

