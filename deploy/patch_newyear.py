#!/usr/bin/env python3
"""Insert New Year 2027 section (#newyear) into prod index.html. Content from content-v3.json only."""
import json, sys, pathlib

root = pathlib.Path(sys.argv[1])
content = json.loads(pathlib.Path(sys.argv[2]).read_text())
idx = root / "index.html"
html = idx.read_text(encoding="utf-8")
assert 'id="newyear"' not in html, "already patched"

def rub(n):
    return f"{n:,}".replace(",", " ") + " ₽"

CSS = """
/* NEWYEAR 2027 (#newyear) */
.ny{background:var(--yellow)}
.ny .s-h h2{font-size:clamp(34px,4.6vw,64px)}
.ny .s-h .r{color:var(--green-ink)}
.ny-top{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:0;border:2px solid var(--green-ink);background:#fff;margin-bottom:32px}
.ny-img{border-right:2px solid var(--green-ink);background:var(--paper)}
.ny-img img{width:100%;height:100%;object-fit:cover;aspect-ratio:1/1}
.ny-info{padding:36px 36px 32px;display:flex;flex-direction:column;gap:22px}
.ny-dates{display:grid;grid-template-columns:1fr 1fr;border:2px solid var(--green-ink)}
.ny-dates div{padding:16px 18px;background:var(--green-ink);color:#fff}
.ny-dates div+div{border-left:2px solid var(--yellow)}
.ny-dates b{display:block;font-family:"Yeseva One",serif;font-style:italic;font-weight:700;font-size:24px;line-height:1.1;color:var(--yellow)}
.ny-dates span{font-size:12px;letter-spacing:0.14em;text-transform:uppercase;font-weight:700}
.ny-lbl{font-family:"PT Mono",monospace;font-size:11px;font-weight:800;letter-spacing:0.2em;text-transform:uppercase;color:var(--green-dp)}
.ny-prog{display:grid;grid-template-columns:1fr 1fr;gap:10px 24px;margin-top:10px}
.ny-prog li{position:relative;padding-left:22px;font-size:15px;line-height:1.45;font-weight:500}
.ny-prog li::before{content:'✓';position:absolute;left:0;font-weight:800;color:var(--green-dp)}
.ny-stays{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:2px solid var(--green-ink);background:#fff;margin-bottom:32px}
.ny-stay{padding:24px 22px;display:flex;flex-direction:column;gap:8px}
.ny-stay+.ny-stay{border-left:2px solid var(--green-ink)}
.ny-stay h3{font-family:"Yeseva One",serif;font-style:italic;font-weight:700;font-size:22px;line-height:1.15;color:var(--green-ink)}
.ny-stay p{font-size:14px;color:var(--green-dp);font-weight:600;flex:1}
.ny-pv{font-family:"Yeseva One",serif;font-weight:700;font-size:32px;line-height:1;white-space:nowrap;color:var(--green-ink)}
.ny-pv small{display:block;font-family:"Cuprum",sans-serif;font-size:11px;font-weight:800;letter-spacing:0.16em;text-transform:uppercase;color:var(--green-dp);margin-top:6px}
.ny-ex{display:grid;grid-template-columns:1fr 1fr;border:2px solid var(--green-ink);background:#fff}
.ny-ex > div{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:16px 22px;border-bottom:2px solid var(--green-ink)}
.ny-ex > div:nth-child(odd){border-right:2px solid var(--green-ink)}
.ny-ex > div:nth-last-child(-n+2){border-bottom:none}
.ny-ex b{font-family:"Yeseva One",serif;font-style:italic;font-weight:700;font-size:19px;display:block}
.ny-ex span{font-size:13px;color:var(--green-dp);font-weight:600}
.ny-ex strong{font-family:"Yeseva One",serif;font-size:22px;white-space:nowrap}
.ny-note{margin-top:16px;font-size:15px;line-height:1.5;font-weight:500}
.ny-cta{margin-top:28px;display:flex;flex-wrap:wrap;gap:12px;align-items:center}
@media (max-width:1024px){
  .ny-stays{grid-template-columns:repeat(2,minmax(0,1fr))}
  .ny-stay:nth-child(3){border-left:none}
  .ny-stay:nth-child(n+3){border-top:2px solid var(--green-ink)}
}
@media (max-width:760px){
  .ny-top{grid-template-columns:1fr}
  .ny-img{border-right:none;border-bottom:2px solid var(--green-ink)}
  .ny-info{padding:22px 18px}
  .ny-dates{grid-template-columns:1fr}
  .ny-dates div+div{border-left:none;border-top:2px solid var(--yellow)}
  .ny-dates b{font-size:21px}
  .ny-prog{grid-template-columns:1fr}
  .ny-stays{grid-template-columns:1fr}
  .ny-stay+.ny-stay{border-left:none;border-top:2px solid var(--green-ink)}
  .ny-ex{grid-template-columns:1fr}
  .ny-ex > div:nth-child(odd){border-right:none}
  .ny-ex > div:nth-last-child(-n+2){border-bottom:2px solid var(--green-ink)}
  .ny-ex > div:last-child{border-bottom:none}
  .ny-ex > div{padding:14px 16px}
  .ny-cta .btn{width:100%;text-align:center;justify-content:center}
}
"""

c = content
import re
m = re.search(r'id="prices">.*?(<svg viewBox="0 0 100 100" width="56".*?</svg>)', html, re.S)
SUN = m.group(1)
dates = "".join(
    f'<div><span>Заезд {i+1} · {o["days"]} суток</span><b>{o["label"].replace("–", " – ")}</b></div>'
    for i, o in enumerate(c["arrival_options"])
)
prog = "".join(f"<li>{p}</li>" for p in c["program"])
stays = "".join(
    f'<div class="ny-stay"><h3>{s["title"]}</h3><p>{s["detail"]}</p>'
    f'<div class="ny-pv">{rub(s["price"])}<small>за {c["duration"]}</small></div></div>'
    for s in c["stays"]
)
extras = "".join(
    f'<div><div><b>{e["title"]}</b><span>{e["detail"]}</span></div><strong>{rub(e["price"])}</strong></div>'
    for e in c["extras"]
)

SECTION = f"""
<!-- NEWYEAR 2027 -->
<section class="s ny" id="newyear">
  <div class="s-in">
    <div class="s-h">
      <div class="num" style="display:flex;align-items:center">{SUN}</div>
      <h2>{c["title"].split(" — ")[0]} —<br/><em class="y">Новый год 2027</em></h2>
      <div class="r">Бронирование новогоднего отдыха открыто. Выберите свой вариант размещения на {c["duration"]}.</div>
    </div>
    <div class="ny-top">
      <div class="ny-img"><img src="img/newyear/newyear-2027-700.webp" srcset="img/newyear/newyear-2027-700.webp 700w, img/newyear/newyear-2027.webp 1100w" sizes="(max-width:760px) 100vw, 640px" width="1100" height="1100" loading="lazy" decoding="async" alt="Новый год 2027 в Ёлкино-Перепёлкино: домик в снегу, праздник у ёлки и гости в банном чане"></div>
      <div class="ny-info">
        <div>
          <div class="ny-lbl">{c["dates_note"]}</div>
          <div class="ny-dates" style="margin-top:10px">{dates}</div>
        </div>
        <div>
          <div class="ny-lbl">Включено в стоимость · Новогодняя программа</div>
          <ul class="ny-prog">{prog}</ul>
        </div>
        <div style="margin-top:auto"><a class="btn btn--lg" href="#contact">{c["cta"]} →</a></div>
      </div>
    </div>
    <div class="ny-lbl" style="margin-bottom:10px">Размещение на {c["duration"]} · стоимость новогоднего заезда</div>
    <div class="ny-stays">{stays}</div>
    <div class="ny-lbl" style="margin-bottom:10px">Дополнительные услуги · оплачиваются отдельно</div>
    <div class="ny-ex">{extras}</div>
    <p class="ny-note">{c["tubs_description"]} {c["unpriced_extras"]}</p>
    <div class="ny-cta">
      <a class="btn btn--lg" href="#contact">{c["cta"]} →</a>
    </div>
  </div>
</section>
"""

marker_css = "</style>"
i = html.index(marker_css)
html = html[:i] + CSS + html[i:]

marker_sec = "\n<!-- TRUST -->"
assert html.count(marker_sec) == 1
html = html.replace(marker_sec, SECTION + marker_sec)

idx.write_text(html, encoding="utf-8")
print("patched", len(html))
