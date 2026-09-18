[EN](README.md) | RU

# IDEA code links

Открытие локального файла на нужной строке в IntelliJ IDEA из браузера.

## Где использовать

Jira, Confluence, Test IT, Allure TestOps: вставьте ссылку на код в описание или поле ссылки. Если `jetbrains://` запрещен, используйте [ссылку на демо](https://hawkab.github.io/idea-code-links/#css-class).

## Пример

Открыть `.code-link` в `styles.css`, строка 15:

```text
jetbrains://idea/navigate/reference?project=idea-code-links&path=styles.css:15:1
```

`project` - имя локального проекта; `path` - путь относительно него. Последние числа - строка и колонка. Это переход по координатам, а не поиск CSS-селектора.

## Установка

```bash
git clone https://github.com/hawkab/idea-code-links.git
```

1. Откройте `idea-code-links` как проект в IDEA.
2. Откройте [демо](https://hawkab.github.io/idea-code-links/) и нажмите **Open .code-link**. Разрешите браузеру открыть IDEA, если он спросит.
3. Если работает, настройка не нужна. Иначе установите или запустите JetBrains Toolbox и повторите.

Только если в Linux переход все еще не работает: установите Python 3 и `xdg-utils`, затем выполните из репозитория, указав путь к IDEA:

```bash
python3 scripts/install-linux.py /path/to/idea/bin/idea
```

Команда регистрирует обработчик для текущего пользователя и передает ссылки навигации прямо в IDEA. При изменении пути к IDEA повторите установку.
