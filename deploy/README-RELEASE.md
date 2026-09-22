# Релизный патч noindex — elkiperepelki.ru · подготовлен 22.09.2026 (Kimi)

**СТАТУС: ЖДЁТ ТИМА. Не выкладывать без прямого слова Тима — это релиз сайта в поиск.**

## Что внутри

- `release_noindex_patch.py` — скрипт, который на свежем FTP-зеркале прода:
  1. снимает `noindex,nofollow` (robots/googlebot/yandex) со всех 116 страниц;
  2. заменяет `https://elki-f.185-202-239-165.sslip.io` → `https://elkiperepelki.ru` в canonical/og:url/og:image (113 файлов);
  3. пишет открытый `robots.txt` + `Sitemap: https://elkiperepelki.ru/sitemap.xml`;
  4. закрывает noindex служебное: `vendomat.html`, `plan/plan.html`, `plan/scene3d.html` (`baza/` уже под noindex);
  5. добавляет счётчик Яндекс.Метрики 95602086 на все страницы.
- Прогон на копии зеркала 22.09: изменено 119 файлов, снято 341 меток noindex, исправлено 113 canonical, метрика на 119 страницах, noindex остался только на `baza/` и 3 служебных. Ошибок нет.

## Порядок при слове Тима «релиз»

1. Свежее зеркало прода: `lftp` (креды `~/.secrets/sweb.env`, docroot `/elkiperepelki_ru/public_html/`, `set ftp:ssl-allow no`).
2. Бэкап на сервере: переименовать изменяемые файлы в `*.bak-20260922` (скрипт ниже это делает не сам — сначала бэкап!).
3. `python3 release_noindex_patch.py --root <зеркало>`.
4. Залить изменённые файлы + `robots.txt` по FTP.
5. Проверка: `curl -s https://elkiperepelki.ru/ | grep -c noindex` → 0; `curl -s https://elkiperepelki.ru/robots.txt` → открыт; canonical → `https://elkiperepelki.ru/`; `curl -sI https://elkiperepelki.ru/derevyannyj-dom/` → 301.
6. Подать `sitemap.xml` в Яндекс.Вебмастер (доступов у агента нет — Тим/Миша) и Google Search Console.
7. Откат при ошибке: вернуть `*.bak-20260922` файлы по FTP, `robots.txt` закрытый из бэкапа.

## Заметки

- Доступов к Яндекс.Вебмастеру/GSC в проекте нет — статус индексации после релиза смотреть там вручную.
- Метрика 95602086 на новом сайте отсутствует (на старом WP была) — после релиза счётчик заработает сам, данные пойдут в существующий кабинет.
- `plan/index.html` («План базы») остаётся в индексе — осмысленная страница; `plan/plan.html` — сирота-дубль, закрыта noindex.
