#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# Подключение к таблице через сервисный аккаунт
# Выгрузка из таблицы данных

import os

import httplib2
import googleapiclient.discovery
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import config

CREDENTIALS_FILE = config.CREDENTIALS_FILE

# Получение данных из таблицы
def getDataTable(sheet_id, name_sheet):
    service = get_service_sacc()
    sheet = service.spreadsheets()
    sheet_id= sheet_id
    # sheet_id = config.ID_SHHET_SETTING


    catalogs = sheet.values().batchGet(spreadsheetId=sheet_id,
                                       ranges=name_sheet).execute()

    return catalogs

# ID таблицы для записи, имя листа и начальная ячейка при необходимости, данные для вставки в таблицу
def appendSheets(idSheet, nameListofSheet, val):
    sheet = get_service_sacc().spreadsheets()

    # # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
    resp = sheet.values().append(
        spreadsheetId=idSheet,
        range=nameListofSheet,
        # valueInputOption="RAW",
        valueInputOption="USER_ENTERED",
        body={'values': val}).execute()


# ID таблицы для записи, имя листа и начальная ячейка при необходимости, данные для вставки в таблицу
def updateSheets(idSheet, nameListofSheet,val):
    sheet = get_service_sacc().spreadsheets()
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
    resp = sheet.values().update(
        spreadsheetId=idSheet,
        range=nameListofSheet,
        valueInputOption="USER_ENTERED",
        body={'values': val}).execute()


# Очистка листа
def clearSheets(idSheet, nameListofSheet):
    sheet = get_service_sacc().spreadsheets()
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear
    resp = sheet.values().clear(spreadsheetId=idSheet, range=nameListofSheet, ).execute()


# Подключение к таблице для чтения данных
def get_service_sacc():
    creds_json = os.path.join(os.path.dirname(__file__), CREDENTIALS_FILE)
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)

