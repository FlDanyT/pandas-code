# @see {@link https://t.me/FlDanyT Telegram} разработка Google таблиц и GAS скриптов
# @see {@name @FlDanyT Telegram} разработка Google таблиц и GAS скриптов


import requests
import pandas as pd
from datetime import datetime, timedelta

from api_google_sheet import *

from config import *


def Oz_Mpstats_by_keywords():
    getDateSheet = getDataTable(config.ID_SHET_SETTING, [config.OZON_NAME_SHEET_MPSTATS_BY_KEYWORDS])
    getDateSheet_List = getDataTable(config.ID_SHET_SETTING, [config.OZON_NAME_SHEET_MPSTATS_BY_KEYWORDS_LIST])
    getDateSheetSetting = getDataTable(config.ID_SHET_SETTING, [config.NAME_SHEET_SETTING])


    today = datetime.now()
    yesterday = today - timedelta(days=1)
    formatted_dateOne = yesterday.strftime('%Y-%m-%d')
    formatted_dateTwo = today.strftime('%Y-%m-%d')
    
    
    IDsSheets_date = [sublist[0:1] for sublist in getDateSheet_List['valueRanges'][0]['values']]
    IDsSheets_date.pop(0)
    lastRow_date = len(IDsSheets_date)
    
    
    for number_row_date in range(lastRow_date):
        row_date = config.OZON_NAME_SHEET_MPSTATS_BY_KEYWORDS_LIST + '!A' + str(number_row_date+2)
        valus_date = [['', '', '', '', '']]


        try:
          last_date = IDsSheets_date[number_row_date][0]
          if last_date == formatted_dateOne:
              updateSheets(config.ID_SHET_SETTING, row_date, valus_date)
          
          
          if last_date == formatted_dateTwo:
              updateSheets(config.ID_SHET_SETTING, row_date, valus_date)
        except:
          print('Нет дат')
          
    
    IDsSheetsSetting = getDateSheetSetting['valueRanges'][0]['values']
    get_token = IDsSheetsSetting[1][4]


    IDsSheets = getDateSheet['valueRanges'][0]['values']
    IDsSheetsLast = [sublist[:2] for sublist in IDsSheets]
    IDsSheetsLast = [item for item in IDsSheetsLast if all(x for x in item)]
    IDsSheetsLast.pop(0)
    
    
    letValuesCatalogs = len(IDsSheetsLast)
    lastRow = letValuesCatalogs
    
    values = []
    
    for date_number in range(2):
      if date_number == 0:
        date = formatted_dateOne
      else:
       date = formatted_dateTwo
     
      
      for number_row in range(lastRow):
        number_row = number_row + 1

        word_values = pd.DataFrame(IDsSheets) # Делаем таблицу pandas
        word_values = word_values.iloc[:, 2:12] # Получаем определеные колонки
        
        
        get_sku = IDsSheets[number_row][1]
        get_artikul = IDsSheets[number_row][0]
        token = get_token
        sku = get_sku
          
          
        date_one = 'd1='+date
        date_two = '&d2='+date
        main_url_one = 'https://mpstats.io/api/oz/get/item/'
        main_url_two = '/by_keywords?'


        url = main_url_one + sku + main_url_two + date_one + date_two


        headers = {
          'X-Mpstats-TOKEN': token,
          'Content-Type': 'application/json',
            }
        
        
        r = requests.get(url, headers=headers)
        if r.status_code == 200:           
            dataSets = r.json()
            words = dataSets['words']
            df = pd.DataFrame(words)
            # result = df.filter(items=['свет для сьемки'])
            headers = df.columns # Получаем названия колонок


            try:
              word_values = word_values.iloc[number_row] # Получаем определеную строчку
            except:
              word_values = word_values.iloc[number_row-1] # Получаем определеную строчку


            word_values_list = word_values.values.tolist() # Преобразуем в список в лист
            
            
            for i, word_values_list_row in enumerate(word_values_list): # Получаем по очереди список
              
              
              if word_values_list_row in headers:
                
                
                print('Есть слово - ' + word_values_list_row)
                index_colum = df.columns.get_loc(word_values_list_row) # Получаем номер колонки
                
                              
                value_colum = df.iloc[:, index_colum]
                pos = value_colum['pos'][0]

                key_word = 'Ключ ' + str(i + 1)


                row = config.OZON_NAME_SHEET_MPSTATS_BY_KEYWORDS_LIST + '!A2'  
                elements = [date, get_artikul, word_values_list_row, pos, key_word]
                values.append(elements)

                
    appendSheets(config.ID_SHET_SETTING, row, values)


if __name__ == "__main__":
    Oz_Mpstats_by_keywords()