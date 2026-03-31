# ADRs (Architecture Decision Records)

Registro **imutável** de decisões técnicas que **mudam o curso do projeto** (ex.: banco de dados, provedor de modelo, fronteira entre serviços, padrão de API estável).

**Quando usar**

- A decisão ainda fará diferença daqui a meses.
- Há alternativas reais e trade-offs a lembrar.

**Quando não usar**

- Detalhe de implementação que pode mudar na próxima sprint.
- Experimentos ainda em spike — documente no spike primeiro; promova a ADR só quando a decisão for “de verdade”.

**Formato padrão:** `ADR-0001-nome-da-decisao.md`

Cada ADR deve ser **curto** e conter:

- Contexto
- Decisão
- Alternativas consideradas
- Prós e contras (ou consequências)
- Data

Em times mínimos, ADRs existem para **não reabrir a mesma discussão** e para dar contexto a colaboradores humanos ou **agentes de IA** que entrem depois.
