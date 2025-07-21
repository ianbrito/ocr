from processor import Processor

from database.mongo import MongoDB


# Use handwritten=False para texto impresso
if __name__ == "__main__":
    
    paths = [
        "/home/ian/Development/projects/python/ocr/docs/historico_2023016794.pdf",
        "/home/ian/Development/projects/python/ocr/docs/declaracao_2023016794.pdf",
        "/home/ian/Development/projects/python/ocr/docs/Requerimento TCC1 Manuescrito.pdf",
        "/home/ian/Development/projects/python/ocr/docs/IAN_TCC_I_REQUERIMENTO_ACADEMICO.pdf",
        "/home/ian/Development/projects/python/ocr/docs/PC010048_Requerimento.pdf"
    ]
    
    for p in paths:
        connection = MongoDB()

        processor = Processor(connection)

        output = processor.execute(p, handwritten=False)
