import os

from database.mongo import MongoDB, Extract
from extrator import Extractor, Classifier

class Processor:

    __extractCollection: Extract
    __extractor: Extractor
    __classifier: Classifier

    def __init__(self, connection: MongoDB):
        self.__extractCollection = Extract(connection)
        self.__extractor = Extractor()
        self.__classifier = Classifier()
        
    def execute(self, file_path, handwritten=False):
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in [".jpg", ".jpeg", ".png", ".tiff"]:
            text = self.__extractor.extract_text_from_image(file_path, handwritten=handwritten)
        elif ext == ".pdf":
            text = self.__extractor.extract_text_from_pdf(file_path, handwritten=handwritten)
        else:
            raise ValueError("Formato de arquivo não suportado.")
        

        entities = self.__extractor.analyze_text(text)

        document_data = {
            "file_name": os.path.basename(file_path),
            "extracted_text": text,
            "entities": entities,
        }

        json_data = self.__classifier.execute(document_data["extracted_text"], entities)

        document_data["document_type"] = json_data["document_type"]
        
        if len(json_data["metadata"]) != 0:
            document_data["metadata"] = json_data["metadata"]

        self.__extractCollection.insert(document_data)

        return document_data
