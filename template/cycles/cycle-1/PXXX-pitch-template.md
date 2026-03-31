# Pitch — <título curto do ciclo>

> **Lembrete:** Pitch é um **fatia delimitada** de trabalho, não um PRD. Para solo/dupla: prefira metade do escopo que você acha que cabe e **no-gos** explícitos. Documentação longa aqui é sinal de que o ciclo pode estar grande demais.

**Appetite (time-box)**  
(ex.: 2 semanas · 1 pessoa | 4 semanas · 2 pessoas — defina teto realista)

**Datas**  
Início: YYYY-MM-DD · Fim alvo: YYYY-MM-DD

**Proposto por**  
(nome ou “solo”)

---

## 1. Problema ou oportunidade

Em poucas frases: qual dor ou ganho justifica este ciclo? O que já se sabe de discovery ou spikes?

**Casos ou histórias que guiam o escopo (opcional):**

- …
- …

*(Não precisa formalizar como “UC” completo — só o suficiente para não discutir escopo no vazio.)*

---

## 2. O que entra neste ciclo (solução em alto nível)

- Entrega ou resultado **visível** ao fim do appetite:
- O que o usuário ou o sistema passa a conseguir fazer?
- **Fora do ciclo** (ver também seção No-Gos): …

### Técnico (opcional, só o relevante)

- Integrações, contratos ou libs que **já** são decisão tomada (ou spike concluído):
- Se ainda há incerteza técnica forte → considere um **spike** antes de comprometer o ciclo inteiro.

---

## 3. Rabbit holes (armadilhas)

- [Armadilha provável] → Como evitamos ou limitamos: …

---

## 4. No-Gos (o que NÃO faremos neste ciclo)

- …
- …

*(Itens aqui podem virar pitch ou spike futuros.)*

---

## 5. Riscos, desconhecidos e dependências

- Riscos:
- O que ainda não sabemos:
- Dependências externas (API, acesso, aprovação):
- Mitigação mínima:

---

## 6. Critérios de pronto (definição de “feito”)

- [ ] …
- [ ] …

*(Alinhe com `make test` / CI da stack do projeto quando fizer sentido — não exija cobertura de meta enterprise se o time é mínimo.)*

---

## 7. Ritmo

- **Time:** solo | dupla (quem)
- **Check-ins:** (ex.: 15 min 2× por semana — ou “assíncrono + review no fim”)

---

**Status:** rascunho | pronto para executar | em andamento

*(“Betting table” só faz sentido com time maior; solo pode marcar “pronto para executar” e seguir.)*
