MVP/
│
├── README_MVP.md
├── PROMPT_MVP.md
├── UQP_PROTOCOL_MVP.md
├── POLICY_DSL_MVP.md
├── DECISION_RULES_MVP.md
├── PROVIDER_MAPPING_TICKET_MVP.yaml
├── THREAT_LIST_10.md
│
├── src/
│   ├── api/
│   │   └── gateway.py
│   ├── router/
│   │   └── router.py
│   ├── drivers/
│   │   └── ticket_driver.py
│   ├── security/
│   │   ├── apikey.py
│   │   └── sanitizer.py
│   ├── policy/
│   │   └── policy_engine.py
│   ├── decision/
│   │   └── decision_engine.py
│   ├── logging/
│   │   ├── audit_log.py
│   │   ├── driver_log.py
│   │   └── error_log.py
│   └── normalizer/
│       └── ticket_normalizer.py
│
├── tests/
│   ├── test_uqp.py
│   ├── test_policy.py
│   ├── test_router.py
│   └── test_driver.py
│
└── examples/
    └── agent_request.json
