# @see {@link https://t.me/FlDanyT Telegram} разработка Google таблиц и GAS скриптов
# @see {@name @FlDanyT Telegram} разработка Google таблиц и GAS скриптов

import requests
import pandas as pd
from datetime import datetime, timedelta

from api_google_sheet import *

from config import *
import json


def Ozon_analytics_data():
    getDateSheetSetting = getDataTable(config.ID_SHET_SETTING, [config.NAME_SHEET_SETTING])
    IDsSheetsSetting = getDateSheetSetting['valueRanges'][0]['values']
    getDateSheet_List = getDataTable(config.ID_SHET_SETTING, [config.OZON_NAME_SHEET_ANALYTICS_DATA_LIST])

    ozon_id = IDsSheetsSetting[1][2]
    client_id = IDsSheetsSetting[1][3]

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    formatted_date_One = yesterday.strftime('%Y-%m-%d')
    formatted_date_Two = today.strftime('%Y-%m-%d')
    
    
    IDsSheets_date = [sublist[0:1] for sublist in getDateSheet_List['valueRanges'][0]['values']]
    IDsSheets_date.pop(0)
    lastRow_date = len(IDsSheets_date)
    
    
    for number_row_date in range(lastRow_date):
        row_date = config.OZON_NAME_SHEET_ANALYTICS_DATA_LIST + '!A' + str(number_row_date+2)
        valus_date = [['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']]


        try:
          last_date = IDsSheets_date[number_row_date][0]
          if last_date == formatted_date_One:
              updateSheets(config.ID_SHET_SETTING, row_date, valus_date)
          
          
          if last_date == formatted_date_Two:
              updateSheets(config.ID_SHET_SETTING, row_date, valus_date)
        except:
          print('Нет дат')
    
    
    url = 'https://api-seller.ozon.ru/v1/analytics/data'
    
    
    cap = [
      "Дата", "SKU товара.", "Наименование.",  "Заказано на сумму", "Заказано товаров", "Показы в поиске и в категории", "Показы на карточке товара", "Всего показов", 
      "В корзину из поиска или категории", "в корзину из карточки товара",  "Всего добавлено в корзину", "Cессии с показом в поиске или в каталоге", "Cессии с показом на карточке товара", 
      "Считаются уникальные посетители", "Конверсия в корзину из поиска или категории", "Конверсия в корзину из карточки товара", "Общая конверсия в корзину", "Возвращено товаров", 
      "Отменено товаров", "Доставлено товаров", "Позиция в поиске и категории",
    ]
    
    
    metrics_one = [
      "revenue",
      "ordered_units",
      "hits_view_search",
      "hits_view_pdp",
      "hits_view",
      "hits_tocart_search",
      "hits_tocart_pdp",
      "hits_tocart",
      "session_view_search",
      "session_view_pdp",
      "session_view",
      "conv_tocart_search",
      "conv_tocart_pdp",
      "conv_tocart",
    ]
    
    metrics_two = [
      "returns",
      "cancellations",
      "delivered_units",
      "position_category",
    ]
    
    
    key_one = "revenue"
    key_two= "returns"
  
  
    values = []  
    index_elements = 0

    for metrics_number in range(2):
      if metrics_number == 0:
        metrics = metrics_one
        key = key_one
        date = formatted_date_One
      else:
        metrics = metrics_two
        key = key_two
        date = formatted_date_Two
        
      for date_number in range(2):
        if date_number == 0:
          date = formatted_date_One
        else:
          date = formatted_date_Two
        

        
        headers = {
        "client-id": ozon_id,
        "api-key": client_id
        }

        body = {
          "date_from": date,
          "date_to": date,
          "metrics": metrics,
          "dimension": [
              "sku",
              "day",
          ],
          "sort": [
              {
                  "key": key,
                  "order": "DESC"
              }
          ],
          "limit": 1000,
          "offset": 0
        }
        
        
        # Не нужно создавать отдельный словарь options
        r = requests.post(url, headers=headers, json=body)
        if r.status_code == 200:           
              dataSets = r.json()
          

              # dimensions_id = dimensions['id']
              # dimensions_name = dimensions['name']

              data = dataSets["result"]["data"]
              df = pd.json_normalize(data)
              
              
              for index, row in df.iterrows():
                
                 
                  
                  
                  dimensions = row['dimensions'][0]
                  dimensions_id = dimensions['id']
                  dimensions_name = dimensions['id']
                  
                  metrics_row = row['metrics']
                  
                  if metrics[0] == "revenue":
                    revenue = metrics_row[0]
                    ordered_units = metrics_row[1]
                    hits_view_search = metrics_row[2]
                    hits_view_pdp = metrics_row[3]
                    hits_view = metrics_row[4]
                    hits_tocart_search = metrics_row[5]
                    hits_tocart_pdp = metrics_row[6]
                    hits_tocart = metrics_row[7]
                    session_view_search = metrics_row[8]
                    session_view_pdp = metrics_row[9]
                    session_view = metrics_row[10]
                    conv_tocart_search = metrics_row[11]
                    conv_tocart_pdp = metrics_row[12]
                    conv_tocart = metrics_row[13]
                    
                    
                    elements = [date, dimensions_id, dimensions_name, revenue, ordered_units, hits_view_search, hits_view_pdp, hits_view, 
                                hits_tocart_search, hits_tocart_pdp, hits_tocart, session_view_search, session_view_pdp, session_view, conv_tocart_search, conv_tocart_pdp, conv_tocart]
                    values.append(elements)
                  else:
                    index_elements = index_elements+1
                    
                    returns = metrics_row[0]
                    cancellations = metrics_row[1]
                    delivered_units = metrics_row[2]
                    position_category = metrics_row[3]
                    
                    
                    values[index_elements-1].extend([returns, cancellations, delivered_units, position_category])



                      
    row = config.OZON_NAME_SHEET_ANALYTICS_DATA_LIST + '!A2'
    appendSheets(config.ID_SHET_SETTING, row, values)
     
              
              
if __name__ == "__main__":
    Ozon_analytics_data()