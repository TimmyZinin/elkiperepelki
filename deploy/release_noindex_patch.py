#!/usr/bin/env python3
"""
РЕЛИЗНЫЙ ПАТЧ elkiperepelki.ru — снятие noindex. ТОЛЬКО ПО СЛОВУ ТИМА.

Что делает (на свежем зеркале прода по FTP):
1. Убирает <meta name="robots|googlebot|yandex" content="noindex,nofollow"> из всех HTML.
2. Заменяет https://elki-f.185-202-239-165.sslip.io → https://elkiperepelki.ru
   (canonical, og:url, og:image и прочие абсолютные ссылки на тестовый хост).
3. robots.txt → открытая версия + строка Sitemap.
4. Служебные страницы (vendomat.html, plan/plan.html, plan/scene3d.html) получают noindex.
5. Добавляет счётчик Яндекс.Метрики (id 95602086) на все страницы.

Запуск:  python3 release_noindex_patch.py --root <путь-к-зеркалу>
Откат:  залить обратно .bak-файлы (см. README-RELEASE.md).
"""
import argparse, os, re, sys

NOINDEX_RE = re.compile(r'\n?\s*<meta name="(?:robots|googlebot|yandex)" content="noindex,nofollow"\s*/?>')
SSLIP = "https://elki-f.185-202-239-165.sslip.io"
PROD = "https://elkiperepelki.ru"
SERVICE_NOINDEX = {"vendomat.html", "404.html", os.path.join("plan", "plan.html"), os.path.join("plan", "scene3d.html")}

ROBOTS = """User-agent: *
Allow: /
Disallow: /baza/
Disallow: /vendomat.html
Disallow: /plan/scene3d.html

User-agent: YandexBot
Allow: /
Disallow: /baza/

User-agent: Googlebot
Allow: /
Disallow: /baza/

Sitemap: https://elkiperepelki.ru/sitemap.xml
"""

METRIKA = """<script>
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0];
k.async=1;k.src=r;a.parentNode.insertBefore(k,a)})
(window,document,'script','https://mc.yandex.ru/metrika/tag.js','ym');
ym(95602086,'init',{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:false});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/95602086" style="position:absolute;left:-9999px" alt=""></div></noscript>
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    root = args.root
    touched, noindex_removed, sslip_fixed, metrika_added, svc_noindexed = [], 0, 0, 0, 0
    for dp, dns, fs in os.walk(root):
        dns[:] = [d for d in dns if not d.startswith(".")]
        for f in fs:
            if not f.endswith(".html"): continue
            fp = os.path.join(dp, f)
            rel = os.path.relpath(fp, root)
            s = open(fp, encoding="utf-8").read()
            orig = s
            s, n = NOINDEX_RE.subn("", s)
            noindex_removed += n
            if SSLIP in s:
                s = s.replace(SSLIP, PROD); sslip_fixed += 1
            if rel in SERVICE_NOINDEX and 'name="robots"' not in s:
                s = s.replace("<head>", '<head>\n<meta name="robots" content="noindex,nofollow">', 1)
                svc_noindexed += 1
            if "mc.yandex.ru/metrika" not in s:
                if "</body>" in s:
                    s = s.replace("</body>", METRIKA + "</body>", 1)
                else:
                    s += METRIKA
                metrika_added += 1
            if s != orig:
                open(fp, "w", encoding="utf-8").write(s)
                touched.append(rel)
    open(os.path.join(root, "robots.txt"), "w", encoding="utf-8").write(ROBOTS)
    print(f"файлов изменено: {len(touched)}; noindex-меток снято: {noindex_removed}; "
          f"canonical/og исправлено: {sslip_fixed}; метрика добавлена: {metrika_added}; "
          f"служебных закрыто noindex: {svc_noindexed}")
    # контроль: noindex остался только на служебных и baza
    left = []
    for dp, dns, fs in os.walk(root):
        for f in fs:
            if f.endswith(".html"):
                fp = os.path.join(dp, f)
                if 'content="noindex' in open(fp, encoding="utf-8").read():
                    left.append(os.path.relpath(fp, root))
    print("noindex остался на:", sorted(left))

if __name__ == "__main__":
    main()
