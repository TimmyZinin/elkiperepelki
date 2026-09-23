#!/usr/bin/env python3
"""Insert a horizontal scroll-snap gallery (photos + 2 videos) into the existing #newyear section.

Usage: patch_newyear_gallery.py <site_root>
Touches only index.html: CSS appended before the first </style>, markup inserted
inside #newyear right before its final CTA (.ny-cta), tiny inline script inside the gallery.
Media: img/newyear/gallery/ (webp 1280 + -sm 640, mp4 H.264 720p + poster webp).
"""
import sys, pathlib

root = pathlib.Path(sys.argv[1])
idx = root / "index.html"
html = idx.read_text(encoding="utf-8")
assert 'id="newyear"' in html, "no #newyear section"
assert 'id="ny-gallery"' not in html, "already patched"

G = "img/newyear/gallery/"
# (id, orientation, alt)
PHOTOS = [
    ("1756964", "v", "Хоровод вокруг ёлки на заснеженной поляне базы Ёлкино-Перепёлкино"),
    ("1756971", "v", "Гости в новогодних колпаках в горячем банном чане под гирляндами"),
    ("1756956", "v", "Гармонист и артисты в народных костюмах на новогоднем гулянии"),
    ("1756957", "v", "Дети и взрослые у ёлки с гирляндами на новогоднем празднике"),
    ("1756959", "v", "Деревянный домик в снегу с тёплым светом в окнах"),
    ("1756968", "v", "Ёлка с разноцветной гирляндой у дома-терема вечером"),
    ("1756960", "v", "Бег в мешках на снегу — новогодние забавы для взрослых"),
    ("1756966", "h", "Двухэтажный деревянный дом в снегу на опушке соснового бора"),
    ("1756967", "v", "Красный шар на ёлке на фоне дома-терема"),
    ("1756961", "v", "Народные игры на снегу — эстафета для гостей"),
    ("1756965", "v", "Новогодние шары и гирлянда на заснеженных еловых ветках"),
    ("1756970", "h", "Домик с полукруглой крышей в заснеженном лесу под голубым небом"),
    ("1756969", "v", "Украшенная ёлка с огнями у одноэтажного дома ночью"),
    ("1756958", "v", "Качели между соснами в зимнем лесу"),
]
VIDEOS = [
    ("1756962", "Видео: новогодние игры на снегу, гости в костюмах-кигуруми"),
    ("1756963", "Видео: новогоднее гуляние с гармонистом, хороводом и самоваром"),
]

def photo(pid, o, alt):
    w, h = (1280, 960) if o == "h" else (960, 1280)
    return (
        f'<figure class="nyg-it nyg-{o}"><a href="{G}ny-{pid}.webp" target="_blank" rel="noopener">'
        f'<img src="{G}ny-{pid}-sm.webp" srcset="{G}ny-{pid}-sm.webp {480 if o == "v" else 640}w, {G}ny-{pid}.webp {w}w" '
        f'sizes="(max-width:760px) 78vw, 360px" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{alt}"></a></figure>'
    )

def video(vid, label):
    return (
        f'<figure class="nyg-it nyg-vid"><video controls muted playsinline preload="none" width="720" height="1280" '
        f'poster="{G}ny-{vid}-poster.webp" aria-label="{label}"><source src="{G}ny-{vid}.mp4" type="video/mp4"></video></figure>'
    )

items = [photo(*p) for p in PHOTOS]
items.insert(2, video(*VIDEOS[0]))
items.insert(8, video(*VIDEOS[1]))

CSS = """
/* NEWYEAR GALLERY (#ny-gallery) */
.nyg{margin-top:32px}
.nyg-hd{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:10px}
.nyg-nav{display:flex;gap:8px}
.nyg-btn{width:48px;height:48px;border:2px solid var(--green-ink);background:#fff;color:var(--green-ink);font:800 22px/1 "Cuprum",sans-serif;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;transition:transform .15s,box-shadow .15s}
.nyg-btn:hover{transform:translate(-2px,-2px);box-shadow:4px 4px 0 var(--green-ink)}
.nyg-btn:disabled{opacity:.35;cursor:default;transform:none;box-shadow:none}
.nyg-track{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain;padding:0 0 12px;margin:0;list-style:none;scrollbar-width:thin;scrollbar-color:var(--green-ink) transparent}
.nyg-track::-webkit-scrollbar{height:6px}
.nyg-track::-webkit-scrollbar-thumb{background:var(--green-ink)}
.nyg-it{flex:0 0 auto;height:440px;margin:0;scroll-snap-align:start;border:2px solid var(--green-ink);background:var(--paper);overflow:hidden}
.nyg-it a{display:block;height:100%}
.nyg-it img,.nyg-it video{display:block;height:100%;width:100%;object-fit:cover;background:var(--green-ink)}
.nyg-v{aspect-ratio:3/4}
.nyg-vid{aspect-ratio:9/16}
.nyg-h{aspect-ratio:4/3}
@media (max-width:760px){
  .nyg-hd{align-items:center}
  .nyg-btn{width:42px;height:42px;font-size:20px}
  .nyg-it{height:min(420px,62vh)}
}
"""

track = "".join(items)
SECTION = f"""
    <div class="nyg" id="ny-gallery">
      <div class="nyg-hd">
        <div class="ny-lbl">Как у нас встречают Новый год · фото и видео</div>
        <div class="nyg-nav"><button type="button" class="nyg-btn" data-dir="-1" aria-label="Предыдущие фото">←</button><button type="button" class="nyg-btn" data-dir="1" aria-label="Следующие фото">→</button></div>
      </div>
      <div class="nyg-track" tabindex="0" aria-label="Галерея новогоднего праздника в Ёлкино-Перепёлкино">{track}</div>
      <script>(function(){{var g=document.getElementById('ny-gallery');if(!g)return;var t=g.querySelector('.nyg-track'),b=g.querySelectorAll('.nyg-btn');function u(){{b[0].disabled=t.scrollLeft<=4;b[1].disabled=t.scrollLeft+t.clientWidth>=t.scrollWidth-4}}b.forEach(function(x){{x.addEventListener('click',function(){{t.scrollBy({{left:+x.dataset.dir*Math.max(t.clientWidth*0.8,240),behavior:'smooth'}})}})}});t.addEventListener('scroll',u,{{passive:true}});window.addEventListener('resize',u);u()}})();</script>
    </div>
"""

i = html.index("</style>")
html = html[:i] + CSS + html[i:]

s = html.index('id="newyear"')
e = html.index("<!-- TRUST -->", s)
marker = '\n    <div class="ny-cta">'
k = html.index(marker, s)
assert k < e, "ny-cta not inside #newyear"
html = html[:k] + SECTION.rstrip("\n") + html[k:]

idx.write_text(html, encoding="utf-8")
print("patched", len(html))
