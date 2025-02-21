import json
import requests


API_KEY = "..."
ENDPOINT = "..."
BASE_URL = "http://127.0.0.1:5000/api"

 
USER_PROMPT_PATH = "C:/Users/wdossantos/Aks/prompts/prompt-user1.pro"
SYSTEM_PROMPT_PATH = "C:/Users/wdossantos/Aks/prompt-system.pro"



# Lista de objetos possíveis de serem consultados pela API do AKS
aks_objects = [
    "pods",
    # "services",
    # "deployments",
    # "ingresses",
    #"hpas"
]


def fetch_object_data(endpoint):
    try:
        response = requests.get(endpoint)  # Fazendo uma requisição GET para a API
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        contentaks = response.json()  # Convertendo a resposta para JSON
        #print(contentaks)
        return contentaks
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

def send_analysis_request(contentaks, userprompt, systemprompt):
    
    
    prompt = userprompt + " infos: [" + str(contentaks) + "]"
    print(prompt)

    
    # Configuration
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    # Payload for the request
    PAYLOAD = {
        "messages": [
            {
                "role": "system",
                "content": systemprompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 8000
    }

    # Send request
    try:
        response = requests.post(ENDPOINT, headers=headers, json=PAYLOAD)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Supondo que 'data' seja uma string JSON
    data = response.json()

    # Acessando a propriedade 'content' dentro da estrutura JSON
    message_content = data["choices"][0]["message"]["content"]
    # Handle the response as needed (e.g., print or process)
    #print(message_content)
    return message_content

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred while reading the file: {e}"

def run_all_objects():

    user_prompt_content = read_file_content(USER_PROMPT_PATH)
    system_prompt_content = read_file_content(SYSTEM_PROMPT_PATH)

    for obj in aks_objects:
        endpoint = f"{BASE_URL}/{obj}"
        contentaks = fetch_object_data(endpoint)
        analysis = send_analysis_request(contentaks, user_prompt_content, system_prompt_content)
        print(f"Analysis for {obj}: " + analysis)

run_all_objects()