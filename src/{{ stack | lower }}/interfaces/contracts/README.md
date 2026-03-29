# contracts/

Esta pasta contém os **contratos** da aplicação (definições formais de interfaces externas).

### Exemplos de arquivos comuns:
- `openapi.yaml` ou `openapi.json` → Especificação completa da API REST
- `events.json` ou `asyncapi.yaml` → Contratos de eventos/assíncronos
- `*.proto` → Definições gRPC/Protobuf
- `schemas/` → JSON Schemas reutilizáveis

### Por que ter uma pasta contracts?
- Serve como **fonte única da verdade** para integrações (frontend, outros serviços, LLMs, etc.).
- Facilita gerar código automaticamente (client SDKs, stubs, validações).
- Mantém separado da implementação concreta (em `api.py`, `webhooks.py`, etc.).

### Recomendação para solo/2 devs:
- Comece simples: um único `openapi.yaml` é suficiente na maioria dos casos.
- Mantenha o contrato atualizado junto com as mudanças no código.
- Após um spike de integração, mova ou crie o contrato aqui.

Exemplo básico de estrutura:

contracts/
├── openapi.yaml
├── schemas/
│   └── user.yaml
└── README.md