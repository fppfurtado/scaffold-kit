# Domain Model

Este documento é a **fonte de vocabulário ubíquo, invariantes e regras de negócio**. Detalhes de desenho técnico e descobertas de integração estão em [design.md](./design.md). Decisões estruturais imutáveis em [decisions/](./decisions/).

## Visão geral do domínio

<preencher: o que esse domínio representa, escopo, premissas fundamentais (ex.: moeda, território, multi-tenancy).>

## Linguagem ubíqua

### <Conceito>
- **Definição:** <descrever o conceito em uma ou duas frases na linguagem do negócio>
- **Relações:** <com quais outros conceitos ele se relaciona>
- **Aliases/Sinônimos:** <termos equivalentes que aparecem no negócio ou na API>

## Agregados e Entidades

### <Agregado>

- **Raiz:** <Entidade raiz>
- **Value Objects:** <bullets>
- **Propriedades Derivadas:** <bullets>

## Invariantes e regras de negócio

- **RN01:** <regra invariante e seu racional>

> Numerar `RN01`, `RN02`, ... à medida que aparecerem. Cada RN é citável de outros documentos (e.g. `[RN05](#invariantes-e-regras-de-negócio)`).
