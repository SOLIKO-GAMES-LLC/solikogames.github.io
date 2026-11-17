"""Собирает страницы сайта из шаблона и файлов с текстами.

    python build.py           собрать index.html и ru/index.html
    python build.py --check   только проверить, что страницы собраны из текущих текстов (ничего не пишет)

Шаблон: src/page.html, метки вида {{ключ}}.
Тексты: texts/en.txt и texts/ru.txt, строки вида "ключ = текст".
Нужен только Python 3.8+, без сторонних библиотек.
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "src" / "page.html"

# Не тексты, а настройки страницы: подставляются в шаблон как есть.
PAGES = [
    {
        "texts": "texts/en.txt",
        "out": "index.html",
        "config": {
            "lang": "en",
            "root": "",
            "url": "https://solikogames.com/",
            "other_lang": "ru",
            "other_href": "ru/",
        },
    },
    {
        "texts": "texts/ru.txt",
        "out": "ru/index.html",
        "config": {
            "lang": "ru",
            "root": "../",
            "url": "https://solikogames.com/ru/",
            "other_lang": "en",
            "other_href": "../",
        },
    },
]

KEY = re.compile(r"^[a-z0-9_]+$")
MARK = re.compile(r"\{\{\s*([a-z0-9_]+)\s*\}\}")


def read_texts(path):
    """Читает файл "ключ = текст". Возвращает (словарь, список ошибок)."""
    texts, errors = {}, []
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    for no, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            errors.append(f"{path.name}:{no}: нет знака «=»: {line[:60]}")
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if not KEY.match(key):
            errors.append(f"{path.name}:{no}: странный ключ «{key}» (только латиница, цифры и _)")
        elif key in texts:
            errors.append(f"{path.name}:{no}: ключ «{key}» уже был выше")
        elif not value:
            errors.append(f"{path.name}:{no}: пустой текст у ключа «{key}»")
        else:
            texts[key] = value
    return texts, errors


def render(template, texts, config, name):
    used, missing = set(), []

    def fill(match):
        key = match.group(1)
        if key in config:
            return config[key]
        if key in texts:
            used.add(key)
            return html.escape(texts[key], quote=True)
        missing.append(key)
        return match.group(0)

    result = MARK.sub(fill, template)
    errors = [f"{name}: нет текста для «{key}»" for key in sorted(set(missing))]
    warnings = [f"{name}: ключ «{key}» не используется в шаблоне" for key in sorted(set(texts) - used)]
    return result, errors, warnings


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    check = "--check" in sys.argv[1:]
    template = TEMPLATE.read_text(encoding="utf-8")
    errors, warnings, outputs = [], [], []

    for page in PAGES:
        texts_path = ROOT / page["texts"]
        texts, errs = read_texts(texts_path)
        errors += errs
        result, errs, warns = render(template, texts, page["config"], texts_path.name)
        errors += errs
        warnings += warns
        outputs.append((ROOT / page["out"], result))

    for w in warnings:
        print("Внимание:", w)
    if errors:
        for e in errors:
            print("Ошибка:", e)
        print("Страницы не собраны: исправьте ошибки выше.")
        return 1

    if check:
        stale = [p for p, text in outputs if not p.exists() or p.read_text(encoding="utf-8") != text]
        for p in stale:
            print("Устарела:", p.relative_to(ROOT).as_posix(), "— запустите python build.py")
        if not stale:
            print("Всё актуально.")
        return 1 if stale else 0

    for path, text in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old == text:
            print("Без изменений:", path.relative_to(ROOT).as_posix())
            continue
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("Собрана:", path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
