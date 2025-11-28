THREAT_LIST_10.md — обновлённая версия
# THREAT_LIST_10.md
# MVP Threat List — Top 10 Minimal Risks
# Путь: /THREAT_LIST_10.md

## Назначение
Содержит список минимальных угроз MVP-уровня.  
Используется разработчиком для минимальной защиты (sanitizing, deny-правила).

## Что делает
- Определяет минимальный набор рисков.
- Помогает проверять архитектуру и код.
- Указывает, что должно быть закрыто в MVP.

## Список угроз (топ-10)
1. API Key Leakage — ключ украден или перехвачен.
2. Over-permissive Policies — слишком широкие allow.
3. Unsafe Parameters — инъекции через параметры.
4. Injection via Params — попытки SQL/path-инъекций.
5. Provider Misuse — неправильные методы провайдера.
6. Driver Errors — некорректная обработка ответов.
7. Logging Leakage — утечка данных в логах.
8. DoS — спам-запросы от агентов.
9. Weak Input Validation — недостаточный sanitizing.
10. Incorrect Error Handling — раскрытие внутренних ошибок.