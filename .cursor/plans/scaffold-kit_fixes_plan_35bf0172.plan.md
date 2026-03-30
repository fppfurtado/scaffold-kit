---
name: scaffold-kit fixes plan
overview: Corrigir bugs de renderizacao Jinja/Copier, inconsistencias de caminhos, e adicionar suporte multi-stack minimo (stdlib) ao scaffold-kit, alem de melhorias de design como docker-compose, OpenAPI generico, e .editorconfig.
todos:
  - id: phase1-tmpl-suffix
    content: Renomear 9 arquivos para adicionar sufixo .tmpl (garantir renderizacao Jinja)
    status: completed
  - id: phase1-main-multistack
    content: Reescrever main.{{ main_extension }}.tmpl com HTTP server stdlib para Python/TS/Go
    status: completed
  - id: phase1-dockerfile
    content: "Corrigir Dockerfile.tmpl: CMD per-stack, caminho correto, remover pip install"
    status: completed
  - id: phase1-src-readme
    content: "Corrigir src/README.md.tmpl: {{ extension }} -> {{ main_extension }}, {{ stack }} -> {{ module_name }}"
    status: completed
  - id: phase1-path-refs
    content: Corrigir src/{{ stack }}/ -> src/{{ module_name }}/ em 4 arquivos de documentacao
    status: completed
  - id: phase2-copier-yaml
    content: Corrigir comentario e help text de module_name no copier.yaml
    status: completed
  - id: phase2-readme-title
    content: Adicionar titulo e descricao ao README.md.tmpl
    status: completed
  - id: phase2-makefile
    content: Tornar Makefile.tmpl consciente da stack com condicionais Jinja
    status: completed
  - id: phase2-ci
    content: Implementar setup real per-stack no ci.yaml.tmpl
    status: completed
  - id: phase2-compose
    content: Criar docker-compose.yml.tmpl
    status: completed
  - id: phase2-pitches-ref
    content: Corrigir cycle-01 -> cycle-1 em pitches/README.md
    status: completed
  - id: phase2-gitignore
    content: Adicionar Go e remover Java do .gitignore
    status: pending
  - id: phase2-openapi
    content: Tornar openapi.yaml generico (substituir conciliador por /items)
    status: pending
  - id: phase2-domain
    content: Corrigir filtro Jinja invalido e termos especificos no domain.md
    status: pending
  - id: phase3-editorconfig
    content: Criar .editorconfig no template
    status: pending
isProject: false
---

# Plano de Correcoes e Melhorias do scaffold-kit

## Contexto

O template Copier usa `_templates_suffix: .tmpl` ([template/copier.yaml](template/copier.yaml) linha 7), o que significa que **apenas arquivos com sufixo `.tmpl` tem seu conteudo renderizado como Jinja2**. Varios arquivos usam variaveis Jinja no conteudo sem esse sufixo, resultando em texto literal `{{ variavel }}` no projeto gerado. Alem disso, o template oferece 3 stacks mas so gera codigo Python.

---

## Fase 1: Correcao de Bugs Criticos (P0)

### 1.1. Adicionar `.tmpl` a 9 arquivos que usam Jinja no conteudo

Estes arquivos contem `{{ }}` no conteudo mas nao tem sufixo `.tmpl`, entao o Copier copia o texto literal sem renderizar:

- `template/.env.example` -> `template/.env.example.tmpl`
- `template/src/main.{{ main_extension }}` -> `template/src/main.{{ main_extension }}.tmpl`
- `template/src/README.md` -> `template/src/README.md.tmpl`
- `template/Makefile` -> `template/Makefile.tmpl`
- `template/docs/{% if include_domain_model %}domain.md{% endif %}` -> `template/docs/{% if include_domain_model %}domain.md.tmpl{% endif %}`
- `template/docs/strategy/spikes/README.md` -> `template/docs/strategy/spikes/README.md.tmpl`
- `template/docs/strategy/spikes/SPK-XXX-definicao-contrato-api.md` -> `template/docs/strategy/spikes/SPK-XXX-definicao-contrato-api.md.tmpl`
- `template/src/{{ module_name | lower }}/{% if use_clean_architecture %}interfaces{% endif %}/contracts/openapi.yaml` -> adicionar `.tmpl`
- `template/src/{{ module_name | lower }}/spikes/README.md` -> adicionar `.tmpl`

### 1.2. Corrigir `main.{{ main_extension }}.tmpl` com suporte multi-stack

O conteudo atual e hardcoded FastAPI. Substituir por hello world HTTP usando stdlib de cada stack:

```jinja2
{% if stack == 'python' -%}
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Server running on http://localhost:8000")
    server.serve_forever()
{% elif stack == 'typescript' -%}
import { createServer } from "node:http";

const server = createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ status: "ok" }));
});

server.listen(8000, () => {
  console.log("Server running on http://localhost:8000");
});
{% elif stack == 'go' -%}
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})
	fmt.Println("Server running on http://localhost:8000")
	http.ListenAndServe(":8000", nil)
}
{% endif %}
```

### 1.3. Corrigir `Dockerfile.tmpl`

Problemas atuais em [template/infra/docker/Dockerfile.tmpl](template/infra/docker/Dockerfile.tmpl):

- `CMD` usa `python` para todas as stacks
- Caminho `src/{{ stack | lower }}/main.py` nao existe (o correto e `src/main.{{ main_extension }}`)
- `pip install -r requirements.txt` sem `requirements.txt` gerado

Novo conteudo:

```jinja2
FROM {{ stack == 'python' and 'python:3.12-slim' or stack == 'typescript' and 'node:22-slim' or 'golang:1.23' }}

WORKDIR /app
COPY . .
{% if stack == 'python' -%}
CMD ["python", "src/main.py"]
{% elif stack == 'typescript' -%}
CMD ["node", "--experimental-strip-types", "src/main.ts"]
{% elif stack == 'go' -%}
RUN go build -o /app/bin/main src/main.go
CMD ["/app/bin/main"]
{% endif %}
```

### 1.4. Corrigir `src/README.md.tmpl` - variavel inexistente

Em [template/src/README.md](template/src/README.md) linha 14-16:

- `src/{{ stack }}/` -> `src/{{ module_name }}/`
- `{{ extension }}` -> `{{ main_extension }}`

### 1.5. Corrigir caminhos `src/{{ stack }}/` nos docs

Apos renomear para `.tmpl`, corrigir todas as referencias `src/{{ stack }}/` para `src/{{ module_name }}/` nestes arquivos:

- `template/docs/{% if include_domain_model %}domain.md.tmpl{% endif %}` (linha 6)
- `template/docs/strategy/spikes/README.md.tmpl` (linhas 26, 28)
- `template/docs/strategy/spikes/SPK-XXX-definicao-contrato-api.md.tmpl` (linhas 17, 40, 43)
- `template/src/{{ module_name | lower }}/spikes/README.md.tmpl` (linha 33)

---

## Fase 2: Correcoes de Design (P1)

### 2.1. Corrigir `copier.yaml`

Em [template/copier.yaml](template/copier.yaml):

- Linha 1: comentario `# copier.yml` -> `# copier.yaml`
- Linha 22: `help` de `module_name`: `"Nome do módulo Python (ou equivalente)..."` -> `"Nome do módulo principal para imports e estrutura interna"`

### 2.2. Adicionar titulo ao `README.md.tmpl`

Em [template/README.md.tmpl](template/README.md.tmpl), adicionar no inicio:

```jinja2
# {{ project_name }}

{{ description }}
```

### 2.3. Tornar `Makefile.tmpl` consciente da stack

Apos renomear para `.tmpl`, usar condicionais Jinja:

```makefile
.PHONY: dev test up clean

dev:
{% if stack == 'python' %}
	python src/main.py
{% elif stack == 'typescript' %}
	node --experimental-strip-types src/main.ts
{% elif stack == 'go' %}
	go run src/main.go
{% endif %}

test:
{% if stack == 'python' %}
	python -m pytest tests/
{% elif stack == 'typescript' %}
	npx vitest run
{% elif stack == 'go' %}
	go test ./...
{% endif %}

up:
	docker compose up --build

clean:
{% if stack == 'python' %}
	rm -rf __pycache__ dist build .pytest_cache
{% elif stack == 'typescript' %}
	rm -rf node_modules dist .cache
{% elif stack == 'go' %}
	rm -rf bin/ vendor/
{% endif %}
```

### 2.4. Corrigir CI workflow (`ci.yaml.tmpl`)

Substituir o stub em [template/.github/workflows/ci.yaml.tmpl](template/.github/workflows/ci.yaml.tmpl) por setup real per-stack:

```yaml
    steps:
      - uses: actions/checkout@v4
{% if stack == 'python' %}
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
{% elif stack == 'typescript' %}
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
{% elif stack == 'go' %}
      - uses: actions/setup-go@v5
        with:
          go-version: "1.23"
{% endif %}
      - run: make test
```

### 2.5. Adicionar `docker-compose.yml.tmpl`

Criar `template/docker-compose.yml.tmpl`:

```yaml
services:
  app:
    build:
      context: .
      dockerfile: infra/docker/Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env
```

### 2.6. Corrigir referencia em `pitches/README.md`

Em [template/docs/strategy/pitches/README.md](template/docs/strategy/pitches/README.md) linha 8:

- `cycles/cycle-01/pitch.md` -> `cycles/cycle-1/pitch.md`

### 2.7. Corrigir `.gitignore` - adicionar Go

Em [template/.gitignore](template/.gitignore), adicionar secao Go e remover Java (que nao e uma stack oferecida):

```gitignore
# Go
bin/
vendor/
```

### 2.8. Tornar OpenAPI generico

Em `template/src/.../contracts/openapi.yaml.tmpl`, substituir `/agents/conciliar` e schemas de conciliacao por exemplos genericos:

- Manter `/health` (ja generico)
- Substituir `/agents/conciliar` por `/items` com CRUD basico
- Renomear schemas `ConciliarRequest/Response` para `CreateItemRequest/ItemResponse`
- Manter `ErrorResponse` (ja generico)

### 2.9. Corrigir `domain.md` - filtro Jinja invalido

Em `template/docs/{% if include_domain_model %}domain.md.tmpl{% endif %}`:

- Linha 52: `{{ now | date(format="%d/%m/%Y") }}` nao e um filtro Jinja2/Copier valido
- Substituir por texto estatico: `(preencha a data da ultima atualizacao)`
- Remover termos especificos "Conciliacao/Agente" da tabela de vocabulario (linhas 39-40), substituir por placeholders genericos

---

## Fase 3: Melhorias (P2)

### 3.1. Adicionar `.editorconfig`

Criar `template/.editorconfig`:

```ini
root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[Makefile]
indent_style = tab
```

---

## Resumo de Operacoes por Arquivo

- **Renomear (9)**: adicionar `.tmpl` aos 9 arquivos listados em 1.1
- **Editar conteudo (14)**: `main`, `Dockerfile`, `src/README`, `copier.yaml`, `README.tmpl`, `Makefile`, `ci.yaml`, `.gitignore`, `openapi.yaml`, `domain.md`, `pitches/README`, `spikes/README` (docs), `SPK-XXX`, `spikes/README` (src)
- **Criar (2)**: `docker-compose.yml.tmpl`, `.editorconfig`

