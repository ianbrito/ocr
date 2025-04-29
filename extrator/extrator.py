import ollama
import json

class Extractor:
    __model: str

    def __init__(self):
        self.__model = "gemma3:4b"
        pass

    def extract(self, texto_extraido):

        prompt = f"""
            Extraia do texto abaixo as seguintes entidades: nome, curso, instituição e matrícula.
            Retorne o resultado em JSON, deve ser um array com objetos key e value, a key é o nome da entidade e o value é o valor extraido. Texto:
            
            Exemplo: [{{'key': 'curso', 'value': 'SISTEMAS DE INFORMAÇAO' }}]

            \"{texto_extraido}\"
        """

        print(prompt)

        response = ollama.chat(
            model=self.__model,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um extrator de informações de documentos.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response["message"]["content"]

        print(content)

        content = content.replace("```json", "")
        content = content.replace("```", "")

        json_data = json.loads(content)

        return json_data
