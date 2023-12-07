# Makefile

# Переменные
VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
SETUP := setup.py

# Цель по умолчанию
all: venv setup test

# Создание и активация виртуального окружения, установка зависимостей
venv: 
	python3 -m venv $(VENV)
	source $(VENV)/bin/activate
	$(PIP) install ujson

# Установка зависимостей, если изменен setup.py
setup: $(SETUP)
	$(PYTHON) $(SETUP) install

# Запуск тестов
test: setup
	$(PYTHON) -m unittest

# Очистка
clean:
	rm -rf $(VENV)
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

.PHONY: venv
.PHONY: setup
.PHONY: test
.PHONY: clean