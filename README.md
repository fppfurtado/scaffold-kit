# scaffold-kit

Template **Copier** para projetos solo ou times pequenos que querem **estrutura mínima e disciplina narrativa** desde o primeiro commit, sem cerimônia tática.

> **v2 — flat & pragmatic, Python-first.** Substitui o v1 (Shape Up cycles + camadas Clean Architecture opcionais + multi-stack). v1 continua acessível via tag `v1.0.0` para consumidores que dependem dele (`copier copy --vcs-ref v1.0.0 ...`).

## Filosofia

**Bounded contexts e linguagem ubíqua sim, cerimônia tática não.** Bounded contexts (DDD estratégico) e vocabulário compartilhado entre código e negócio são fundamentais. Já a cerimônia tática (camadas formais `application/`/`domain/`/`infrastructure/`, ports/adapters universais, mappers em cascata) gera muitos arquivos para pouco valor — adicionar abstração só quando há **dor real** (uma integração instável, uma substituição prevista). YAGNI por padrão. Refatorar mais tarde costuma ser mais barato do que abstrair cedo.

## Como usar

Pré-requisitos: [`uv`](https://docs.astral.sh/uv/) e [`copier`](https://copier.readthedocs.io/).

```bash
pipx install copier        # ou: pip install copier
copier copy gh:fppfurtado/scaffold-kit ./meu-projeto
cd meu-projeto
uv sync
make test
```

Atualizar um projeto já gerado quando o template evoluir:

```bash
copier update
```

## Perguntas no bootstrap

| Pergunta | Default | Para que serve |
|----------|---------|----------------|
| `project_name` | `my-new-project` | Nome de exibição (README, cabeçalho do IDEA). |
| `project_slug` | derivado | Diretório, nomes de serviço Docker. |
| `module_name` | derivado | Pacote Python sob `src/`. |
| `description` | vazio | Linha curta para `pyproject.toml` e topo do `IDEA.md`. |
| `use_docker` | `true` | Inclui `docker-compose.yml`, `infra/docker/Dockerfile`, `.dockerignore`. |

## O que é gerado

```
meu-projeto/
├── CLAUDE.md            # filosofia + ordem de leitura para Claude Code
├── IDEA.md              # esqueleto de visão de produto
├── README.md            # entrada do projeto
├── BACKLOG.md           # itens em fluxo (Próximos / Em andamento / Concluídos)
├── Makefile             # alvos: dev, test, clean (+ up se use_docker)
├── pyproject.toml       # uv-friendly, pytest+pytest-asyncio+respx
├── .editorconfig
├── .gitignore
├── .env.example
├── .worktreeinclude     # consumido por /run-plan
├── docs/
│   ├── domain.md        # esqueleto de linguagem ubíqua + invariantes
│   ├── design.md        # esqueleto de peculiaridades de integração
│   ├── decisions/
│   │   └── ADR-template.md
│   └── plans/.gitkeep
├── src/<module_name>/
│   ├── __init__.py
│   └── main.py          # health-check HTTP placeholder
├── tests/
│   ├── unit/.gitkeep
│   ├── integration/.gitkeep
│   └── conftest.py
├── .github/workflows/ci.yml
└── (use_docker)
    ├── docker-compose.yml
    ├── .dockerignore
    └── infra/docker/Dockerfile
```

Sem `cycles/`, `spikes/`, camadas Clean/Hexagonal opcionais ou prompts multi-stack — esses elementos do v1 foram descartados deliberadamente (ver tag `v1.0.0` se precisar do template antigo).

## Companion: Claude Code plugin

Para automação alinhada à filosofia (skills `/new-feature`, `/new-adr`, `/run-plan`, agent `code-reviewer`, hook que protege `.env`), instalar o plugin [`pragmatic-dev-toolkit`](https://github.com/fppfurtado/pragmatic-dev-toolkit) no projeto gerado:

```
/plugin marketplace add fppfurtado/pragmatic-dev-toolkit
/plugin install pragmatic-dev-toolkit@fppfurtado-pragmatic-dev-toolkit
```

Os dois artefatos são desacoplados — o template gera as convenções de path (`docs/plans/`, `docs/decisions/`, `BACKLOG.md`, `Makefile` com alvo `test`, `.worktreeinclude`) que o plugin assume. Você pode usar um sem o outro, mas a sinergia é evidente.

## Contribuindo

No diretório `template/`, arquivos com sufixo `.jinja` são processados como **Jinja2** pelo Copier. Sem o sufixo, o conteúdo é copiado literalmente. Conditionals de inclusão de arquivo ficam em `template/copier.yaml` (`_exclude`).

Smoke tests de render: `pip install -e ".[dev]" && pytest`.

## Licença

Sem `LICENSE` versionado ainda — adicionar conforme intenção do operador.
