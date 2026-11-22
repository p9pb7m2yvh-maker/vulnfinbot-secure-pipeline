# Mini-VulnFinBot — secure CI/CD pipeline

Учебный проект: простой финансовый помощник на Flask (mock-ИИ) и CI/CD в GitHub Actions
с проверками безопасности.

## Технологии
Python 3.12, Flask, pytest, gunicorn, Docker, GitHub Actions, Bandit, Semgrep, pip-audit, Trivy, OWASP ZAP.

## Архитектура
- `app/__init__.py` — создание приложения, заголовки безопасности, обработчики ошибок
- `app/routes.py` — эндпоинты `/health` и `/api/chat`, валидация, mock-ИИ, проверка вывода
- `tests/` — unit-тесты и тесты AI-безопасности
- `security/` — правила Semgrep и скрипт отчёта AI-тестов
- `.github/workflows/security-pipeline.yml` — pipeline

## Установка и запуск
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py                   # http://localhost:5000
```
Проверка: `curl http://localhost:5000/health`

Пример чата:
```bash
curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" \
  -d '{"message": "How can I manage my monthly budget?"}'
```

## Запуск тестов
```bash
pytest -v
```

## Docker
```bash
docker build -t vulnfinbot:latest .
docker run --rm -p 5000:5000 vulnfinbot:latest
```

## Pipeline
При push и pull request в `main` выполняются: тесты → Bandit → Semgrep → pip-audit →
сборка Docker → Trivy → запуск контейнера → OWASP ZAP → AI-тесты → загрузка отчётов
(artifact `vulnfinbot-security-reports`). Сканеры идут с `continue-on-error`, чтобы
отчёты загружались даже при находках.

## Отчёты
GitHub → вкладка **Actions** → нужный запуск → раздел **Artifacts** → `vulnfinbot-security-reports`.

## Безопасность приложения
Валидация JSON и типов, лимит 500 символов, ошибки без stack trace, в логах только длина
сообщения, заголовки безопасности, запуск Docker не от root, белый список инструментов,
проверка ответа бота.

## Ограничение
ИИ здесь mock. Тесты проверяют защиту на уровне приложения, но не доказывают устойчивость
настоящей LLM к prompt injection.

## Найденные уязвимости и рекомендации
Заполняется по результатам реальных отчётов (см. технический отчёт).
