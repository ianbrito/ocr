import os
import pdfplumber
import spacy
from doctr.models import ocr_predictor
from doctr.io import DocumentFile
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import fitz


class Extractor:

    __nlp: spacy.language.Language

    __pretrained_model_name_or_path = "microsoft/trocr-base-handwritten"

    def __init__(self):

        self.__nlp = spacy.load("en_core_web_sm")

        self.__ocr_model = ocr_predictor(pretrained=True)

        self.__trocr_processor = TrOCRProcessor.from_pretrained(
            self.__pretrained_model_name_or_path, use_fast=False
        )

        self.__trocr_model = VisionEncoderDecoderModel.from_pretrained(
            self.__pretrained_model_name_or_path
        )

    def extract_text_from_image(self, file_path, handwritten=False):
        if handwritten:
            image = Image.open(file_path).convert("RGB").resize((384, 384))

            pixel_values = self.__trocr_processor(
                images=image, return_tensors="pt"
            ).pixel_values

            generated_ids = self.__trocr_model.generate(pixel_values)

            text = self.__trocr_processor.batch_decode(
                generated_ids, skip_special_tokens=True
            )[0]

            return text
        else:
            doc = DocumentFile.from_images(file_path)
            result = self.__ocr_model(doc)
            text = "\n".join(
                [
                    " ".join([word.value for word in line.words])
                    for page in result.pages
                    for block in page.blocks
                    for line in block.lines
                ]
            )
            return text

    def extract_text_from_pdf(self, file_path, handwritten=False):
        text = ""
        has_text = False
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    has_text = True
                    text += page_text + "\n"

        if not has_text:
            with fitz.open(file_path) as pdf:
                for page_num in range(len(pdf)):
                    pix = pdf[page_num].get_pixmap(dpi=400)
                    img_path = f"temp_page_{page_num}.png"
                    pix.save(img_path)
                    text += (
                        self.extract_text_from_image(img_path, handwritten=handwritten)
                        + "\n"
                    )
                    os.remove(img_path)

        return text

    def analyze_text(self, text):
        doc = self.__nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({"text": ent.text, "label": ent.label_})
        return entities
