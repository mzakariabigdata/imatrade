###################
##### include #####
###################
# Inclusion du fichier de fonctions
include Makefile-Functions.mk
PYTHON = python

###################
####### Ci ########
###################

run-ci: ## Run ci
	@echo "Run ci..."
	@docker run -it --rm --name imatrade-ci --mount type=bind,source="${PWD}"/.,target=/app imatrade-ci:1.0.0 bash

build-ci: ## Build ci
	@echo "Build ci..."
	@cp Pipfile ci/
	@docker build -t imatrade-ci:1.0.0 -f ci/Dockerfile .

rm-ci: ## Remove ci
	@echo "Remove ci..."
	@docker rm -f imatrade-ci:1.0.0

.PHONY: build-ci rm-ci
###################
### Virtual ENV ###
###################
env-create: ## Crée un environnement virtuel "imatrade" utilisant Python 3.11 avec conda.
	@echo "Creation de l'environnement virtuel \"imatrade\" utilisant Python 3.11 avec conda..."
	conda create -n imatrade python=3.11

env-deactivate: ## Désactive l'environnement virtuel "imatrade" créé précédemment.
	@echo "Désactivation de l'environnement virtuel \"imatrade\"..."
	conda deactivate

env-delete: ## Supprime l'environnement virtuel "imatrade" créé précédemment avec conda.
	@echo "Suppression l'environnement virtuel \"imatrade\"..."
	conda env remove -n imatrade

env-activate: ## Active l'environnement virtuel "imatrade" créé précédemment et définit la variable PYTHONPATH pour qu'elle pointe vers le répertoire de travail courant.
	@echo "Activation l'environnement virtuel \"imatrade\"..."
	@echo "source ~/anaconda3/etc/profile.d/conda.sh; conda activate imatrade"
	@echo 'PYTHONPATH="$$(pwd)"'
	@source ~/anaconda3/etc/profile.d/conda.sh; conda activate imatrade

env-variables: ## Ajouter costums variables au Shell
	@echo "Ajout des variables d'environnement personnalisées au Shell..."
	. ./.env.sh

get-vscode-extensions: ## Récupérer la liste des extensions installées dans VS Code
	@echo "Récupération de la liste des extensions installées dans VS Code..."
	code --list-extensions >> vscode-extensions.txt

install-vscode-extensions: vscode-extensions.txt ## Installe les extensions VS Code à partir du fichier vscode-extensions.txt.
	@echo "Installation des extensions VS Code à partir vscode-extensions.txt..."
	cat vscode-extensions.txt | xargs -n 1 code --install-extension

env-init: ## Installe l'outil pipenv dans l'environnement système.
	@echo "Installation l'outil pipenv..."
	pip install pipenv


requirements-lock: ## Verrouille les dépendances de production dans un fichier Pipfile.lock à partir du fichier Pipfile.
	@echo "Verrouillage des dépendances de production dans  Pipfile.lock..."
	pipenv lock

requirements-prod: requirements-lock Pipfile ## Génère un fichier requirements-prod.txt contenant une liste des dépendances de production et de leur hachage à partir du fichier Pipfile.lock.
	@echo "Génération de requirements-prod.txt à partir Pipfile.lock..."
	pipenv requirements --hash > requirements-prod.txt

requirements-dev: env-init requirements-lock Pipfile ##  Génère un fichier requirements-dev.txt contenant une liste des dépendances de développement et de leur hachage à partir du fichier Pipfile.lock.
	@echo "Génération de requirements-dev.txt à partir Pipfile.lock..."
	pipenv requirements --hash --dev > requirements-dev.txt

install-requirements-prod: requirements-prod ##  Installe les dépendances de production en utilisant le fichier requirements-prod.txt.
	@echo "Installer les dépendances de production en utilisant le fichier requirements-prod.txt."
	pip3 install -r requirements-prod.txt --user

install-requirements-dev: requirements-dev ## Installe les dépendances de développement en utilisant le fichier requirements-dev.txt.
	@echo "Installer les dépendances de développement en utilisant le fichier requirements-dev.txt."
	pip3 install -r requirements-dev.txt --user

.PHONY: env-activate env-create kivy-install env-init requirements-prod requirements-dev install-requirements-prod install-requirements-dev requirements-lock get-vscode-extensions install-vscode-extensions env-variables


#####################
###### Jupyter ######
#####################
jupyter: ## Lance le serveur Jupyter Notebook.
	@echo "Lancement du serveur Jupyter Notebook..."
	@jupyter notebook
.PHONY: jupyter

###################
###### Behave ######
###################
behave: ## Exécuter les tests comportementaux en utilisant l'outil Behave.
	@echo "Lancement des tests comportementaux en utilisant l'outil Behave..."
	@behave --no-capture
.PHONY: behave
###################
###### Build ######
###################
app-examples: ## Lancer les exemples de l'application.
	@echo "Lancement des exemples de l'application..."
	@cd examples && $(PYTHON) run_examples.py
app-clean: ## Nettoie les fichiers générés précédemment pour l'application.
	@echo "Nettoyage des fichiers générés par dist..."
	rm -f dist/*.gz
app-dist: app-clean  ## Crée une distribution de l'application.
	@echo "Création d'une distribution de l'application..."
	$(PYTHON) setup.py sdist
app-deploy: app-dist ## Déploie l'application en envoyant la distribution sur PyPI.
	@echo "Déploiement d'une distribution de l'application sur PyPI."
	twine upload dist/*
app-install: ## Installer 'imatrade' localement
	@echo "Installation de 'imatrade' localement..."
	pip install -e .
app: src/app.py  ## Lance l'application principale en exécutant le fichier src/app.py.
	@echo "Lancement de l'application principale en exécutant le fichier src/app.py..."
	$(PYTHON) -m pyclean . -q
	export PYTHONPATH=$$(pwd) ;\
	cd src && $(PYTHON) app.py trade menu
	$(PYTHON) -m pyclean . -q
format: ## Formate le code source en utilisant l'outil Black.
	@echo "Formatage du code source..."
	@$(PYTHON) -m black .
format-check: ## Formate check en utilisant l'outil Black.
	$(PYTHON) -m black . --check
lint: ## Verifie le code source avec pylint.
	@echo "Verification du code source avec pylint..."
	@$(PYTHON) -m pylint src/. tests/.
	@echo "Verification ended."

tests: clean-py ## Execute unit tests.
	@echo "Execute unit tests..."
	@$(PYTHON) -m pytest -s -vv
	@echo "Execution ended."

cov: ## Execute unit tests with coverage HTML.
	@echo "Execute unit tests with coverage HTML..."
	@$(PYTHON) -m pytest -s -vvv --cov-report term-missing:skip-covered --cov-report=html:reports/ --cov=src/imatrade tests/

cov-xml: ## Execute unit tests with coverage XML.
	@echo "Execute unit tests with coverage XML..."
	@$(PYTHON) -m pytest  -rX -vvv --cov-report term-missing:skip-covered --cov-report=xml:reports/coverage.xml --cov=src/imatrade tests/

clean-py: ## Clean cache files.
	@echo "Clean cache files..."
	$(PYTHON) -m pyclean . -q
fl: format lint ## Format and lint code.
	
.PHONY: tests clean-py lint format app app-clean fl app-examples

###################
###### Docs #######
###################
# Sphinx documentation
SPHINXOPTS		=
SPHINXINIT		= sphinx-quickstart
SPHINXBUILD		= sphinx-build
SOURCEDIR		= docs/source
BUILDDIR		= docs/build
DOCSDIR			= docs

.PHONY: docs-init docs clean-docs

docs-init: ## Initialisation du repo docs.
	@echo "Initialisation du repo docs..."
	$(call create-dir, $(DOCSDIR)) && cd docs && $(SPHINXINIT) && sphinx-apidoc -o docs src/
	@echo "Initialisation terminée."

docs: clean-docs ## Génération de la documentation avec Sphinx.
	@echo "Génération de la documentation avec Sphinx..."
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	# cd docs && make html
	@echo "Génération terminée."

clean-docs: ## Suppression des fichiers générés pour la documentation.
	@echo "Suppression des fichiers générés pour la documentation..."
	rm -rf "$(BUILDDIR)"
	@echo "Nettoyage terminé."

##########################
###### Change logs #######
##########################

pre-commit-install: ## Installation des hooks pre-commit.
	@echo "Installation des hooks pre-commit..."
	pre-commit install
	@echo "Installation terminée."

pre-commit-run: ## Exécution des hooks pre-commit sur tous les fichiers.
	@echo "Exécution des hooks pre-commit sur tous les fichiers..."
	pre-commit run --all-files
	@echo "execution ended."

.PHONY: pre-commit-install pre-commit-run

##########################
###### Change logs #######
##########################

DOCSDIR			:= 2.0.0

add-fragments: ## Création de nouveaux fragments de changelog.
	@echo "Création de nouveaux fragments de changelog..."
	towncrier create --config towncrier.toml --content 'Can also be ``rst`` as well!' 3452.doc.rst
	@echo "Création terminée."

newsfragment: ## Génère les fichiers .rst pour chaque section de changelog
	@echo "Génération des fichiers .rst pour chaque section de changelog..."
	towncrier --draft --yes
	@echo "Génération terminée."


build-news: ## Génère les fichiers de sortie pour les nouvelles sections de changelog
	@echo "Génération des fichiers de sortie pour les nouvelles sections de changelog..."
	towncrier --yes
	@echo "Génération terminée."

costum-changelogs: ## Génération des journaux de changement personnalisés.
	@echo "Génération des journaux de changement personnalisés..."
	cd changelogs/costum && $(PYTHON) changelogs.py
	@echo "Génération terminée."

.PHONY: newsfragment add-fragments build-news costum-changelogs


##########################
########## Help ##########
##########################

.PHONY: help kaka
help: ## Affiche cette aide
	@echo "Les commandes disponibles sont :"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*?# .*$$' Makefile | sort | awk -F':.*?# ' '/^[a-zA-Z0-9_-]+:.*?#/ {printf "  make \033[36m%-16s\033[0m %s\n", $$1, $$2}'

help2: ## Affiche cette aide
	@echo "Voici les commandes disponibles :"
	@echo ""
	@awk -F ':.*?##' '/^[^\t].+?:.*?##/ { printf " make \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST) | sort
