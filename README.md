# Ссылки на код в IntelliJ IDEA

[Демо](https://hawkab.github.io/idea-code-links/) открывает локальный `styles.css` и объявление `.code-link` в IntelliJ IDEA.

Страница состоит из `index.html` и `styles.css`. JavaScript и сборка не нужны. Скрипты в `scripts/` настраивают обработчик ссылок в Linux.

## Быстрый старт

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/hawkab/idea-code-links.git
   ```

2. Откройте папку `idea-code-links` как проект в IDEA. Сохраните это имя проекта: оно используется в ссылках.
3. Настройте обработчик одним из способов ниже.
4. Откройте [демо](https://hawkab.github.io/idea-code-links/) и нажмите «Открыть .code-link». Разрешите браузеру запуск внешнего приложения, если он спросит.

GitHub Pages хранит страницу, а IDEA открывает файл из вашей локальной копии. Ссылка не скачивает репозиторий и не переключает Git-ветку. Для проверки проект должен быть открыт; запуск закрытого проекта не проверен.

## Обработчик ссылок

### Штатный вариант

Установите и запустите JetBrains Toolbox. В IDEA выберите файл и выполните **Copy Path/Reference → Toolbox URL**. Проверьте полученную ссылку в браузере. Сохраните дополнительные параметры, если IDEA их добавляет.

Если это работает, локальный обработчик из репозитория не нужен. Этот способ применим и на Windows/macOS; приведённый ниже установщик рассчитан только на Linux.

### Linux: прямой вызов IDEA

На машине, где проверялся пример, `jetbrains://` был зарегистрирован на `jetbrainsd.desktop`, но демон отвечал `Nowhere to forward the URI`. Передача того же URL исполняемому файлу IDEA открывала исходник.

Обход: отдельный обработчик передаёт `jetbrains://idea/navigate/...` непосредственно IDEA. Остальные ссылки `jetbrains://` передаются JetBrains Daemon, если он найден. Установщик меняет ассоциацию протокола только для текущего пользователя.

Требуются Python 3, `xdg-utils` и установленная IntelliJ IDEA. Из корня репозитория:

```bash
python3 scripts/install-linux.py /полный/путь/к/idea/bin/idea
```

Передайте путь к исполняемому файлу вашей установки. Найти его можно в свойствах ярлыка IDEA, в поле `Exec`. После обновления или переноса IDE повторите установку с новым путём.

Установщик создаёт:

| Файл | Назначение |
| --- | --- |
| `~/.local/share/idea-code-links/handle-url.py` | Передача URL в IDEA или JetBrains Daemon |
| `~/.local/share/applications/idea-code-links.desktop` | Регистрация приложения |
| `~/.config/idea-code-links/config.json` | Пути к IDEA и демону |
| `~/.config/idea-code-links/previous-handler.txt` | Предыдущая ассоциация протокола |

При заданных `XDG_DATA_HOME` и `XDG_CONFIG_HOME` используются эти каталоги.

Проверка:

```bash
xdg-mime query default x-scheme-handler/jetbrains
xdg-open 'jetbrains://idea/navigate/reference?project=idea-code-links&path=styles.css:1:1'
```

Первая команда должна вернуть `idea-code-links.desktop`. Вторая передаёт запрос IDEA. В браузере при выборе приложения укажите **IntelliJ IDEA Code Links**. Если браузер запомнил старое приложение, сбросьте выбор для протокола или снова выберите новый обработчик.

Чтобы вернуть предыдущую ассоциацию:

```bash
previous=$(cat "${XDG_CONFIG_HOME:-$HOME/.config}/idea-code-links/previous-handler.txt")
if [ -n "$previous" ]; then
  xdg-mime default "$previous" x-scheme-handler/jetbrains
fi
```

Чтобы явно вернуть штатный демон, если он установлен:

```bash
xdg-mime default jetbrainsd.desktop x-scheme-handler/jetbrains
```

## Формат ссылки

```text
jetbrains://idea/navigate/reference?project=idea-code-links&path=styles.css:1:1
```

- `project` — имя локального проекта.
- `path` — путь к файлу относительно проекта.
- `:1:1` — строка и колонка, начиная с 1; их можно опустить.

`.code-link` объявлен в первой строке `styles.css`. Это переход к координатам CSS-класса, а не поиск селектора по имени. Если перенести объявление, обновите номер строки в ссылках. Java-параметр `fqn=пакет.Класс#метод` в CSS-примере не используется.

В HTML символ `&` записывается как `&amp;`:

```html
<a href="jetbrains://idea/navigate/reference?project=idea-code-links&amp;path=styles.css:1:1">Открыть .code-link</a>
```

В поле URL учётной системы вставляется обычный `&`, без HTML-экранирования.

## Jira, Confluence, Test IT и Allure TestOps

Для всех четырёх систем можно использовать HTTPS-ссылку на нужный пример:

```text
https://hawkab.github.io/idea-code-links/#css-class
```

Пользователь открывает страницу и нажимает «Открыть .code-link». На его компьютере нужны локальный проект и обработчик протокола. Никакой JavaScript в учётную систему вставлять не требуется.

| Система | Куда вставить HTTPS-ссылку |
| --- | --- |
| Jira | Откройте редактирование описания или комментария, выделите «Открыть CSS в IDEA» и выберите вставку ссылки в редакторе. Вставьте URL и сохраните. |
| Confluence | В редакторе страницы выделите текст, нажмите `Ctrl+K` (`Cmd+K` на macOS), вставьте URL и опубликуйте страницу. |
| Test IT | В редакторе тест-кейса добавьте ссылку в описание через панель редактора либо в раздел «Ссылки». Вставьте URL и сохраните. |
| Allure TestOps | В тест-кейсе откройте раздел Links / «Ссылки», добавьте обычную ссылку с именем «CSS в IDEA» и URL страницы. Сохраните. |

Названия кнопок зависят от версии системы. Если редактор принимает `jetbrains://`, можно вставить прямую ссылку вместо HTTPS и убрать промежуточный переход. После сохранения проверьте её кликом: поддержка нестандартной схемы не гарантируется, особенно в Cloud-редакторах. При блокировке используйте HTTPS-вариант выше; настройка обработчика ОС не меняет фильтрацию ссылок сервером.

Для Jira с включённым wiki-renderer:

```text
[CSS в IDEA|https://hawkab.github.io/idea-code-links/#css-class]
```

Для Markdown-редактора:

```markdown
[CSS в IDEA](https://hawkab.github.io/idea-code-links/#css-class)
```

Эти инструкции описывают вставку обычных ссылок. Работа прямого `jetbrains://` в конкретных экземплярах Jira, Confluence, Test IT и TestOps не проверялась.

## Локальный просмотр и GitHub Pages

Откройте `index.html` в браузере или запустите из корня:

```bash
python3 -m http.server 8000
```

На GitHub: **Settings → Pages → Deploy from a branch → main → /(root) → Save**. После успешного развёртывания адрес появится в настройках Pages. Файл `.nojekyll` отключает обработку Jekyll.

## Документация

- [IntelliJ IDEA: Toolbox URL](https://www.jetbrains.com/help/idea/project-tool-window.html)
- [Параметры обработчика navigate](https://github.com/JetBrains/intellij-community/blob/master/platform/lang-impl/src/com/intellij/navigation/JBProtocolNavigateCommand.kt)
- [Jira: ссылки и Markdown](https://support.atlassian.com/jira-software-cloud/docs/markdown-and-keyboard-shortcuts/)
- [Confluence: вставка ссылок](https://support.atlassian.com/confluence-cloud/docs/insert-and-manage-links-on-your-pages/)
- [Test IT: редактор тест-кейса](https://docs.testit.software/user-guide/sections/create-work-items.html)
- [Allure TestOps: Links](https://docs.qameta.io/use-testops/test-management/links-issues-and-relations/)
- [GitHub Pages: публикация из ветки](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
