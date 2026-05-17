# Backlog

Lista exploratória de itens em fluxo. Sem ciclos formais, sem pitches/notes/reviews — apenas intenção e fechamento curto.

## Próximos

- _(vazio)_

## Concluídos

- _(vazio)_

---

## Como usar

- Cada item em **Próximos** é **uma linha** com a intenção. Sem detalhamento prévio.
- **Não há seção "Em andamento".** Trabalho em curso vive em git/forge — branch ativa, worktree corrente, PR aberto. O autor da branch sabe sem consultar; quem está de fora vê pelos PRs abertos.
- Ao fechar, **adicionar** linha em **Concluídos** (append-only) com uma frase curta sobre a decisão tomada. Não mover de Próximos — append em Concluídos e remover de Próximos são edits independentes.
- **Decisões estruturais** que afetam o código de forma duradoura viram ADR em [docs/decisions/](docs/decisions/).
- **Aprendizado de negócio** atualiza [docs/domain.md](docs/domain.md).
- **Peculiaridade nova de integração** atualiza [docs/design.md](docs/design.md).
- Tudo mais fica só no histórico do git.

A intenção é manter **Próximos** curto e vivo — itens que envelhecem sem progredir são removidos ou reformulados, não acumulados. **Concluídos** funciona como registro editorial: além de listar o que fechou, captura notas úteis ("flagado durante X", "observado na release Y") que não cabem em commit message.
