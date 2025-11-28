# PROVIDER_MAPPING_TICKET_MVP.yaml
# Provider Mapping — Ticket API (MVP Edition)
# Путь: /PROVIDER_MAPPING_TICKET_MVP.yaml

# Назначение файла:
# Определяет соответствие UQP action → драйвер → метод драйвера.
# Router использует этот файл для выбора обработчика запроса.

ticket.get:
  driver: ticket           # имя драйвера в /src/drivers/
  driver_method: get_ticket
  params:
    - id                   # обязательный параметр действия

ticket.list:
  driver: ticket
  driver_method: list_tickets
  params:
    - project              # фильтр по проекту
