import lxml.etree as ET
import os, time
from colorama import init, Fore, Back
init(convert=True)


def validate_with_lxml(xsd_tree, xml_tree, z=0):
    schema = ET.XMLSchema(xsd_tree)
    try:
        schema.assertValid(xml_tree)                                              # валидация данных по xsd схеме
        print(Fore.GREEN + '----------------------------')
        if z == 0: print(Fore.GREEN +'Входящий файл xml успешно прошел валидацию')
        else: print(Fore.GREEN +'Трансформированный файл xml успешно прошел валидацию')
        print(Fore.GREEN + '----------------------------')
        return True
    except ET.DocumentInvalid:
        if z==0: print(Fore.RED+"Ошибка валидации входного файла xml: ")
        else: print(Fore.RED+"Ошибка валидации трансформированного файла xml по xslt шаблону: ")
        for error in schema.error_log:
            print(Fore.RED+"  Line {}: {}".format(error.line, error.message))      # вывод ошибки в терминал на каждом этапе валидации
        return False


def transform_xslt_xml(xml_tree, xslt_tree):
    try:
        transform = ET.XSLT(xslt_tree)
        result = transform(xml_tree)                                                # трансформация документа по xslt шаблону
        if not validate_with_lxml(xsd_tree, result, z=1): return None               # валидация трансформированного файла
        return result                                                               # в случае успешной валидации вернуть преобразованные данные
    except Exception as e:                                                          # обработка ошибки трансформации и вывод ее в терминал
        print(Fore.RED + "----------------------------")
        print(Fore.RED+"Ошибка трансформации: "+str(e))
        print(Fore.RED + "----------------------------")
        time.sleep(5)
        return None


def save_result(result, new_doc):
    with open(new_doc, 'w') as file:
        result.write(new_doc)                                                        # запись результата трансформации в файл
    print(Fore.GREEN + "Результирующий файл успешно сохранен")


if __name__ == "__main__":

    while True:
        try:
            print(Fore.GREEN+ "Введите путь к xml файлу: ", end='')
            file_name = input().strip()
            print(Fore.GREEN + "Введите путь к xsd файлу: ", end='')
            xsdschema_name = input().strip()
            print(Fore.GREEN + "Введите путь к xslt файлу: ", end='')
            xslt_name = input().strip()
            print(Fore.GREEN + "Введите путь к результирующему xml файлу: ", end='')
            new_doc =input().strip()
            xml_tree = ET.parse(file_name)                                              # парсинг входящего xml
            xsd_tree = ET.parse(xsdschema_name)                                         # парсинг схемы xsd
            xslt_tree=ET.parse(xslt_name)                                               # парсинг входящего xslt

            validate_with_lxml(xsd_tree, xml_tree)                                      # валидация входящего файла xml
            result=transform_xslt_xml(xml_tree, xslt_tree)                              # трансформация входящего файла xml
            if result is not None: save_result(result, new_doc)                         # сохранение трансформированного файла xml
            else: print(Fore.RED+"Результирующий файл не был сохранен ")
            break
        except (FileNotFoundError, OSError) as e:                                       # обработка ошибки "файл не найден"
            print(Fore.RED+str(e))
            print(Fore.RED+"-----------------------------------------------------")
            print(Fore.RED+'ВНИМАНИЕ: ' + 'Файл не найден. Возможно вы ввели неверное название')
            print(Fore.YELLOW + 'Попробуйте снова')
            print(Fore.RED+"-----------------------------------------------------")
            continue
        except ET.XMLSyntaxError as e:                                                   # обработка синатксической ошибки
            print(Fore.RED + 'ВНИМАНИЕ: ' + 'Файл синтаксическая ошибка файла xml.')
            print(Fore.RED+str(e))
            print(Fore.YELLOW + 'Попробуйте другой файл')
            continue
    time.sleep(20)
