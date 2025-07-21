import json
import ollama
import unicodedata

def sanitize(texto: str) -> str:
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    texto_sem_acentos = ''.join(
        c for c in texto_normalizado if unicodedata.category(c) != 'Mn'
    )
    
    return texto_sem_acentos.lower()


class Classifier:
    __model: str

    documents = {
        "historico": ["nome", "matricula", "curso"],
        "declaracao": ["nome", "curso", "matricula", "instituição"],
        "requerimento": ["nome", "curso", "matricula", "instituição"],
    }

    def __init__(self):
        self.__model = "gemma3:4b"

    def __command(self, prompt):
        response = ollama.chat(
            model=self.__model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a document information extractor. Responses must be in JSON format and no other formatting.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response

    def __to_json(self, content):
        print(content)
        content = content.replace("```json", "")
        content = content.replace("```", "")

        json_data = json.loads(content)

        return json_data

    def __classifier(self, content):
        prompt = f"""
            Identify the document type in the text below:
            Return only the type, nothing else.

            Exemplo: declaracao
            Exemplo: historico
            
            \"{content}\"
        """

        response = ollama.chat(
            model=self.__model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a document classifier. Responses should be just the classification, in text format, without any markup.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response["message"]["content"]

    def __from_content(self, type, content):

        metadata = self.documents[type]
        m = ",".join(metadata)

        prompt = f"""
            Extract the following entities from the text below: {m}.
            Return the result in JSON format, it should be an array with key and value objects, the key is the name of the entity and the value is the extracted value. Text:
            
            Example: [{{'key': 'curso', 'value': 'SISTEMAS DE INFORMAÇAO' }}]

            \"{content}\"
        """

        print(prompt)

        return self.__command(prompt)

    def __from_entities(self, entities):
        prompt = f"""
            Classify these entities identified by NLP.
            Return the result in JSON, it should be an array with key and value objects, the key is the name of the entity and the value is the extracted value. Text:
            
            Example: [{{'key': 'curso', 'value': 'SISTEMAS DE INFORMAÇAO' }}]

            \"{entities}\"
        """

        return self.__command(prompt)

    def execute(self, content, entities):

        document_type = ""

        try:
            response = self.__classifier(content[:1000])
            print(response)
            document_type = sanitize(response)
        except Exception:
            print("Error")

        try:
            response = self.__from_content(document_type, content[:1000])

            data = self.__to_json(response["message"]["content"])

            return {"document_type": document_type, "metadata": data}
        except Exception:
            print("Error")

        # try:
        #     response = self.__from_entities(entities)

        #     data = self.__to_json(response["message"]["content"])

        #     print(data)
        # except Exception:
        #     print("Error")

        return {"document_type": document_type, "metadata": {}}
