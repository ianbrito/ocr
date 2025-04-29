from processor import Processor

from database.mongo import MongoDB


# Use handwritten=False para texto impresso
if __name__ == "__main__":
    file_path = (
        "/home/ian/Downloads/historico_2023016794.pdf"
    )

    connection = MongoDB()

    processor = Processor(connection)

    output = processor.execute(file_path, handwritten=False)

    print("--- Texto Extraído ---")
    print(output["extracted_text"][:1000])

    print("\n--- Entidades Encontradas ---")
    for entity in output["entities"]:
        print(f"{entity['label']}: {entity['text']}")
