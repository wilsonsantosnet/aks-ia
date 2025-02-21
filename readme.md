# AKS IA Analysis Report

Este projeto é uma aplicação Flask que consulta informações de um cluster Kubernetes (AKS) e envia essas informações para um endpoint de análise. O objetivo é fornecer insights detalhados sobre o desempenho, segurança e escalabilidade do cluster.

## Estrutura do Projeto

- `k8s.py`: Implementa a API Flask para consultar informações do cluster Kubernetes.
- `prompt-system.pro`: Contém o prompt do sistema para a análise.
- `prompts/prompt-user1.pro`: Contém o prompt do usuário para a análise.
- `run_analysis_report.py`: Script principal que consulta a API do AKS e envia os dados para análise.
- `readme.md`: Este arquivo.

## Requisitos

- Python 3.x
- Flask
- Kubernetes Python Client
- Requests

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/aks-ia.git
    cd aks-ia
    ```

2. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure o acesso ao seu cluster Kubernetes no arquivo [k8s.py](http://_vscodecontentref_/1).

## Uso

### Executando a API Flask

Para iniciar a API Flask, execute o seguinte comando:
```sh
python k8s.py

Para rodar a analise, execute o seguinte comando:
```sh
python .\run_analysis_report.py