# project-template-hybrid-solo

Template Copier projetado para **projetos solo ou com até 2 desenvolvedores** que começam com ideias e requisitos ainda vagos ou incompletos.

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

## Como usar este template

```bash
copier copy https://github.com/seuusuario/project-template-hybrid-solo template/ meu-novo-projeto
```

Após gerar o projeto, siga o fluxo recomendado no README.md gerado dentro do projeto.

## Estrutura gerada
O template gera uma estrutura que evolui junto com o projeto:

`docs/` → Cérebro do projeto (discovery, spikes, domain, ADRs)
`src/{{ module_name }}/` → Código fonte com suporte condicional a camadas
`spikes/` → Experimentos temporários
`cycles/` → Ciclos de entrega
