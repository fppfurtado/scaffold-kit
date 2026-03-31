# scaffold-kit

Repositório do **template Copier** pensado para **projetos solo ou com até 2 desenvolvedores** que começam com ideias e requisitos ainda vagos ou incompletos.

## Espírito e Intenções

Este template foi criado com o objetivo de **reduzir a sobrecarga cognitiva** nas fases iniciais de desenvolvimento, permitindo que o foco esteja na **descoberta e validação de ideias**, em vez de configurar estrutura complexa desde o primeiro dia.

### Motivações principais

- Facilitar o início rápido de novos projetos quando os requisitos não estão claros.
- Fornecer uma metodologia leve, organizada e intuitiva.
- Separar claramente código experimental (spikes) do código de produção.
- Permitir que a arquitetura evolua gradualmente conforme o projeto ganha clareza.
- Ser útil tanto para humanos quanto para **agentes de IA** que auxiliem na manutenção futura.

### Pressupostos utilizados na elaboração deste template

- A maioria dos projetos começa com requisitos nebulosos.
- Experimentação rápida (spikes) é mais valiosa que planejamento detalhado no início.
- Documentação excessiva precoce gera procrastinação.
- Times pequenos (solo ou 2 devs) precisam de clareza visual e poucas decisões iniciais.
- O modelo de domínio evolui com os aprendizados dos spikes.
- Contratos técnicos (OpenAPI etc.) só devem ser criados quando realmente necessários.
- A arquitetura em camadas é útil, mas deve ser opcional no começo.

## Stacks suportadas

Na geração, o Copier pergunta a **stack** principal. O projeto inclui um servidor HTTP mínimo (biblioteca padrão de cada linguagem) em `src/main.<extensão>`, além de **Makefile**, **Dockerfile**, **CI** e alvos de teste alinhados à stack:

| Stack        | Entrada     | Observação |
| ------------ | ----------- | ---------- |
| Python       | `src/main.py` | HTTP via `http.server` |
| TypeScript   | `src/main.ts` | Node.js 22 (`--experimental-strip-types` onde aplicável) |
| Go           | `src/main.go` | `net/http` |

Há também `docker-compose.yml` na raiz do projeto gerado (build a partir de `infra/docker/Dockerfile`, porta **8000**) e `.editorconfig` com convenções básicas.

## Como usar este template

```bash
git clone https://github.com/fppfurtado/scaffold-kit.git
mkdir novo-projeto
copier copy scaffold-kit/template/ novo-projeto
```

Após gerar o projeto, siga o fluxo recomendado no `README.md` dentro do projeto gerado.

## Estrutura gerada

O nome do pacote ou módulo interno vem da resposta **`module_name`** no Copier (por padrão derivado do slug do projeto). A estrutura evolui junto com o projeto:

- `docs/` — Cérebro do projeto (discovery, spikes, domain opcional, ADRs)
- `src/main.<ext>` — Ponto de entrada HTTP mínimo da stack escolhida
- `src/<módulo>/` — Código fonte com suporte condicional a camadas (app, domain, infrastructure, interfaces); spikes de código em `src/<módulo>/spikes/` quando aplicável
- `docs/strategy/spikes/` — Documentação de experimentos técnicos
- `cycles/cycle-1/` — Primeiro ciclo: modelos `PXXX-pitch-template.md`, `NXXX-note-template.md`, `RXXX-review-template.md` (convenção alinhada a `docs/strategy/discovery/`)
- `tests/` — Testes automatizados (estrutura inicial; dependências de teste variam por stack)
- `infra/docker/` — Imagem Docker por stack
- `docker-compose.yml` — Subir a aplicação com `make up` ou `docker compose up`

## Contribuindo com o template

No diretório `template/`, apenas arquivos com sufixo **`.jinja`** têm o conteúdo renderizado como **Jinja2** pelo Copier. Se você incluir interpolação Jinja no conteúdo, o arquivo precisa usar esse sufixo; caso contrário, o texto será copiado literalmente para o projeto gerado.
