import cohere
import json
import os

class CohereService:
    def __init__(self, api_key):
        self.client = cohere.Client(api_key)
        self.history_file = 'history.json'
        
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        else:
            self.history = []

    def salvar_historico(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def gerar_resposta(self, user_input):
        self.history.append(f"Usuário: {user_input}")
        historico_limitado = self.history[-6:]

        
        prompt = (
        "Você é um assistente virtual brasileiro, educado, simpático e que fala APENAS em português. "
        "Mesmo que o usuário escreva em outro idioma, você NUNCA pode responder em inglês, espanhol ou qualquer outro idioma. "
        "Responda de forma natural, como se estivesse conversando com um amigo brasileiro. Não use palavras estranhas nem traduções literais.\n\n" +
        "\n".join(historico_limitado) + "\nAI:"
)
        
        response = self.client.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=50,
            temperature=0.7  # pode aumentar um pouco a criatividade
        )
        
        resposta = response.generations[0].text.strip()
        self.history.append(f"AI: {resposta}")
        self.salvar_historico()
        return resposta

    def zerar_historico(self):
        self.history = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
