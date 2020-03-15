#   <-- Обработка данных после парсинга -->

# Получение данных (между кавычками)
def BetweenQuotes(string, index, length):
    start_data = string[index + length:]
    first_occurrence = 1
    second_occurrence = start_data.find("'", string.find("'") + 1)
    return start_data[first_occurrence:second_occurrence]

def TableRow(value, t_index, dl_index, vl_index):
    # Размер ключевых слов (до первой ' с данными)
    # T - TITLE   DL - DOWNLOAD_LINK    VL - VIEW_LINK
    T_LENGTH = 8
    DL_LENGTH = 16
    VL_LENGTH = 12

    # makaka = [Заголовок, Смотреть, Скачать]
    makaka = [BetweenQuotes(value, t_index, T_LENGTH),  BetweenQuotes(value, dl_index, DL_LENGTH),  BetweenQuotes(value, vl_index, VL_LENGTH)]
    return (makaka)

def GetTable(Data):
    table = []
    i = 0
    for i in range(len(Data)):
        # Получить индексы ключевых слов
        value = Data[i]
        t_index = str(value).find("title")
        dl_index = str(value).find("download_link")
        vl_index = str(value).find("view_link")
        table.append(TableRow(str(value), t_index, dl_index, vl_index))
    return (table)