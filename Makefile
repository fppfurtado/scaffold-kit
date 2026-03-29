.PHONY: dev test up clean

dev:
	@echo "🚀 Rodando em modo desenvolvimento..."
	# Adicione aqui o comando da sua stack

test:
	@echo "🧪 Executando testes..."
	# pytest ou vitest ou go test

up:
	docker compose up --build

clean:
	rm -rf __pycache__ dist build .pytest_cache