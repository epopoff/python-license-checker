import requests
import re

def get_license(package_name):
    """Получает информацию о лицензии пакета с PyPI, включая classifiers."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Проверяем поле 'license'
        license_info = data['info'].get('license')
        
        # Если поле 'license' пустое, проверяем 'classifiers'
        if not license_info:
            classifiers = data['info'].get('classifiers', [])
            # Ищем строку с информацией о лицензии в classifiers
            license_info = next(
                (classifier for classifier in classifiers if classifier.startswith("License")),
                "Лицензия не указана"
            )
        
        return license_info
    else:
        return "Пакет не найден на PyPI"

def parse_requirements(file_path, output_file):
    """Парсит файл requirements.txt и сохраняет пакеты с их лицензиями в файл с разметкой Markdown."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Открываем файл для записи в формате Markdown
        with open(output_file, 'w') as md_file:
            md_file.write("# Список пакетов и их лицензий\n\n")
            
            for line in lines:
                # Извлекаем имя пакета без версии (если версия указана)
                package = re.split('==|>=|<=|>|<', line.strip())[0]
                license_info = get_license(package)
                # Записываем информацию в формате Markdown
                md_file.write(f"- **{package}**: {license_info}\n")
                
        print(f"Информация сохранена в файл {output_file}")
    
    except FileNotFoundError:
        print("Файл requirements.txt не найден.")

if __name__ == "__main__":
    # Укажите путь к вашему файлу requirements.txt и имя выходного файла
    file_path = "requirements.txt"
    output_file = "licenses.md"
    parse_requirements(file_path, output_file)