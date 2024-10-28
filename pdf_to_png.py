import pymupdf  # PyMuPDF
import os

def pdf_to_png(pdf_file):
    # Получаем имя файла без расширения
    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    
    # Создаем папку с названием документа
    if not os.path.exists(base_name):
        os.makedirs(base_name)
    
    # Открываем PDF-документ
    pdf_document = pymupdf.open(pdf_file)
    
    # Проходим по всем страницам и сохраняем каждую как PNG
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Загружаем страницу
        pix = page.get_pixmap()  # Конвертируем страницpoetry i
        # Формируем путь для сохранения слайда
        image_path = os.path.join(base_name, f"{page_num + 1}.png")
        
        # Сохраняем изображение
        pix.save(image_path)
    
    print(f"Все страницы сохранены в папку: {base_name}")

# Пример использования:
pdf_to_png("./PDFs2/КП-Калифорния-157.pdf")
