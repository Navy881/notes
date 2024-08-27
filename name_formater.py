
import os
import re
import urllib.parse
import difflib

# Регулярное выражение для поиска UUID в имени файла
uuid_pattern = re.compile(r'\s*[0-9a-f]{32}\s*')
md_uuid_pattern = re.compile(r'%20[0-9a-f]{32}')


def remove_uuid_from_name(name):
    """Удаляет UUID из названия файла или папки, сохраняя пробелы в остальных частях имени"""
    new_name = re.sub(uuid_pattern, '', name).strip()
    return new_name


def extract_diff(str1, str2):
    # Создаем объект SequenceMatcher
    matcher = difflib.SequenceMatcher(None, str1, str2)

    # Список для хранения частей, которые отличаются
    differences = []

    # Обрабатываем каждый блок отличий
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace' or tag == 'insert':
            # Извлекаем часть из второй строки, где произошла замена или вставка
            differences.append(str2[j1:j2])
        elif tag == 'delete':
            # Извлекаем часть из первой строки, где произошла удаление
            differences.append(str1[i1:i2])

    # Объединяем все отличия в одну строку
    return ''.join(differences)


def rename_files_and_folders(root):
    """Рекурсивно проходит по дереву каталогов и переименовывает файлы и папки"""
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        # Переименовываем файлы
        for filename in filenames:
            new_filename = remove_uuid_from_name(filename)
            if filename != new_filename:
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, new_filename)
                os.rename(old_path, new_path)
                print(f'Файл переименован: {old_path} -> {new_path}')
                diff = extract_diff(old_path, new_path)
                update_references(root, diff)

        # Переименовываем папки
        for dirname in dirnames:
            new_dirname = remove_uuid_from_name(dirname)
            if dirname != new_dirname:
                old_path = os.path.join(dirpath, dirname)
                new_path = os.path.join(dirpath, new_dirname)
                os.rename(old_path, new_path)
                print(f'Папка переименована: {old_path} -> {new_path}')
                diff = extract_diff(old_path, new_path)
                update_references(root, diff)
    
    print(f'\n\n\nВсе файлы и папки переименованы\n\n\n')
              

def is_text_file(filepath):
    """Проверяет, является ли файл текстовым"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            file.read()
        return True
    except (UnicodeDecodeError, IOError):
        return False
        
        
def decode_url(encoded_url):
    """Декодирует URL, заменяя %20 и другие символы на их оригинальные значения"""
    return urllib.parse.unquote(encoded_url)
    

def update_references(root, target_string):
    """Рекурсивно проходит по файлам и обновляет ссылки на переименованные файлы"""
    target_string = target_string.replace(' ', '%20')
    
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            
            # Обрабатываем только текстовые файлы
            if is_text_file(filepath):
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Удаляем значения из файла
                new_content = content
                new_content = new_content.replace(target_string, '')
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f'Обновлены данные в файле: {filename}')
             

def main():
    root_dir = 'Other'  # Укажите корневую папку
    rename_files_and_folders(root_dir)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
