setup:
ifeq ($(stack),python-fastapi)
	pip install fastapi uvicorn
endif

run:
ifeq ($(stack),python-fastapi)
	uvicorn src.python-fastapi.app.main:app --reload
endif

ifeq ($(stack),node-nest)
	npm run start
endif
