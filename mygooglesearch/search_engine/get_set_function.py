from .models import SearchInformation, SearchConfig, ResultSearch
from apiclient.discovery import build
import re
from time import time
from datetime import datetime, timezone
import traceback



def get_client_ip(request):
    """Funkcja odpowiedzialna za pobranie IP użytkownika, który szuka informacji
    
    Args:
        request (http request): Http request
    
    Returns:
        (str): IP użytkownika
    """
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    except AttributeError:
        return {"status": 500, "data": "Błędny obiekt request."}
        
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return {"status": 200, "data": ip}

def get_google_search(api_key, cse_id, search_value, user_ip):
    """Funkcja odpowiedzialna za pobranie danych z API Google
    
    Args:
        api_key (str): Klucz API
        cse_id (str): Klucz przeglądarki
        search_value (str): Szukana fraza
        user_ip (str): IP osoby, która wyszukuje dane
    
    Returns:
        (list): Lista z wynikami wyszukiwania
    """
    try:
        service = build("customsearch", "v1", developerKey=api_key).cse()
        res = service.list(q=search_value, cx=cse_id, num=10).execute()

    except BaseException:
        return {"status": 500, "data": ""}
    
    res = get_prepare_data(res)    
    
    save_to_db = save_result_to_db(res, user_ip, search_value)
    if not save_to_db==True:
        return {"status": save_to_db["status"], "data": ""}

    return {"status": 200, "data": res}


def get_prepare_data(items):
    """Funkcja odpowiedzialan za przygotowanie danych po frontend
    
    Args:
        items (list): Wynik wyszukiwania
    
    Returns:
        (dict): Słowik z wynikiem przetwarzania
    """
    for index, item in enumerate(items["items"]):
        tmp = dict()
        words = item['title'].split()
        for word in words:
            if re.findall("[a-zA-Z]", word):
                if word in tmp:
                    tmp[word] += 1
                else:
                    tmp[word] = 1

        snippet = item['snippet'].split()
        for word in snippet:
            if re.findall("[a-zA-Z]", word):
                if word in tmp:
                    tmp[word] += 1
                else:
                    tmp[word] = 1


        item['count_words'] = ''.join(f"{key}: {tmp[key]}," for key in list(tmp.keys()))
        item['position'] = index+1

    return items



def save_result_to_db(items, user_ip, search_value):
    """Funkcja odpowiedzialna za zapisanie danych do bazy po odwołaniu się do API
    
    Args:
        items (list): wynik po odpowiedzi API
        user_ip (str): IP użytkownika
        search_value (str): wartość szukana
    
    Returns:
        (str/bool): Wiadomość o błędzie lub wartość True po poprawnym zapisie
    """
    try: 
        flag_search_info = False
        search_item_info = SearchInformation.objects.get(search_value=search_value, user_ip_address=user_ip)
        search_item_info.last_search_date = datetime.now()
        search_item_info.save()

    except SearchInformation.DoesNotExist: 
        flag_search_info = True
        info_to_save = SearchInformation()
        info_to_save.user_ip_address = user_ip
        info_to_save.search_value = search_value
        info_to_save.save()

    except BaseException:
        return {"status": 507}

    try:
        search_item_result = ResultSearch.objects.filter(search_information_fk__search_value=search_value, search_information_fk__user_ip_address=user_ip)
        if search_item_result:
            for item in search_item_result:
                item.delete()

        for item in items["items"]:
            result_to_save = ResultSearch()
            result_to_save.title = item["title"]
            result_to_save.link_to_display = item["displayLink"]
            result_to_save.link_to_side = item["link"]
            result_to_save.position = item["position"]
            result_to_save.count_words = item["count_words"]
            result_to_save.search_information_fk = info_to_save if flag_search_info else search_item_info
            result_to_save.save()
            
    except BaseException:
        return {"status": 507}

    return True


def get_data_from_db(search_value, user_ip):
    """Funkcja odpowiedzialna za pobranie danych z bazy
    
    Args:
        search_value (str): Szukana wartość
        user_ip (str): Ip użytkownika
    
    Returns:
        (list): Lista z danymi z bazy danych
    """
    start_time = time()
    try:
        search_item_result = ResultSearch.objects.filter(search_information_fk__search_value=search_value, search_information_fk__user_ip_address=user_ip)
    except BaseException:
        return False
    if search_item_result:
        data_to_return = {
                "searchInformation": {
                    "formattedSearchTime": None,
                    "formattedTotalResults": None,
                },
                "items": []
            }

        for result in search_item_result:
            data_to_return["items"].append({
                "position": result.position,
                "displayLink": result.link_to_display,
                "title": result.title,
                "link": result.link_to_side,
                "count_words": result.count_words,
            })
            data_to_return["searchInformation"]["formattedSearchTime"] = time() - start_time 
            data_to_return["searchInformation"]["formattedTotalResults"] = len(search_item_result)

        return data_to_return
    else:
        return False