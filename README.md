# solikogames.com

Official website of Soliko Games. Static HTML published with GitHub Pages; the two pages are generated locally from one template and two text files (`python build.py`).

A one-page studio card in the Soliko brandbook v1.0 (Nunito, brand palette, flat fills).
No contact details on purpose.

## Как править тексты

1. Откройте `texts/ru.txt` (русская версия) или `texts/en.txt` (английская).
2. Меняйте текст справа от `=`. Ключ слева не трогайте. Один текст — одна строка.
3. Соберите страницы и проверьте локально:

   ```bash
   python build.py
   python -m http.server 8080
   ```

4. Закоммитьте и запушьте вместе: `texts/*.txt` и собранные `index.html`, `ru/index.html`.

`build.py` сам скажет, если в тексте опечатка в ключе, ключ повторяется или какого-то текста не хватает.
`python build.py --check` проверяет, что страницы собраны из текущих текстов (удобно перед push).

Вёрстка общая для обоих языков — `src/page.html`. Тексты страницы 404 правятся прямо в `404.html`.

## Файлы

```
texts/en.txt      English texts
texts/ru.txt      Russian texts
src/page.html     Shared page template ({{key}} marks)
build.py          Builds index.html and ru/index.html from the template and texts
index.html        English page (generated)
ru/index.html     Russian page (generated)
404.html          Not-found page (GitHub Pages serves it automatically)
assets/site.css   Styles (side menu, header slider, sections, footer)
assets/site.js    Header slider: two phrases, autoplay every 5 s
assets/brand/     Logo for dark backgrounds and social preview (og.jpg), from the brandbook files
assets/img/       Header photos from Unsplash (Unsplash License): hero-studio, hero-players
favicon-*.png     Site icons; apple-touch-icon.png
CNAME             Custom domain for GitHub Pages (solikogames.com)
.nojekyll         Serve files as they are, without Jekyll
robots.txt, sitemap.xml
```

## Local preview

```bash
python -m http.server 8080
```

Open http://localhost:8080.

## Publish

1. Repository `<org>/<org>.github.io`, public, branch `main`.
2. Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)`.
3. Settings → Pages → Custom domain → `solikogames.com`, then Enforce HTTPS once it unlocks.

Every push to `main` updates the site in about a minute.

## DNS (Squarespace)

Delete the "Squarespace Defaults" record group first, then add:

| Host | Type | Data |
|---|---|---|
| `@` | A | `185.199.108.153` |
| `@` | A | `185.199.109.153` |
| `@` | A | `185.199.110.153` |
| `@` | A | `185.199.111.153` |
| `www` | CNAME | `<org>.github.io` |
| `_github-pages-challenge-<org>` | TXT | the code from the organisation's Settings → Pages → Add a domain |

---

© 2026 SOLIKO GAMES LLC. All rights reserved.
