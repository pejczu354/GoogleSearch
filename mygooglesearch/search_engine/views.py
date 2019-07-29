from django.http import JsonResponse
from datetime import datetime, timezone
import json
import traceback
from .models import SearchInformation, SearchConfig, ResultSearch
from .get_set_function import (
    get_client_ip, get_google_search, get_prepare_data, 
    get_data_from_db
)

def get_data(request):
    """Funkcja odpowiedzialna za pobranie danych

    Zależnie od tego czy dana fraza była już wyszukiwana przez danego użytkownika
    dane będą pobrane z API bądź z bazy zależnie od konfiguracji
    
    Args:
        request (http request): Http request wraz z danymi w postaci JSON {
            search_item(str): szukana wartość
        }
    
    Returns:
        (dict/str): Wynik z danymi w postaci słownika lub pusty string jeżeli wystąpi błąd
    """
    try:
        search_item = json.loads(request.body.decode("utf-8"))['search_item']
    except KeyError:
        return JsonResponse(status=400, data="", safe=False)
    except ValueError:
        return JsonResponse(status=400, data="", safe=False)

    config = SearchConfig.objects.all().values().first()
    my_api_key = ""
    my_cse_id = ""
    ip = get_client_ip(request)
    if ip["status"] == 200:
        try:
            check_search_value = SearchInformation.objects.get(search_value=search_item, user_ip_address=ip['data'])
        except SearchInformation.DoesNotExist:
        ###################### GOOGLE API SEARCH IF SEARCH INFORMATION NOT EXIST #########################
            google_result = get_google_search(my_api_key, my_cse_id, search_item, ip['data'])

            if google_result["status"]==500:
                return JsonResponse(status=500, data=google_result["data"], safe=False)
            return JsonResponse(status=200, data=google_result["data"], safe=False)


        check_time = datetime.now(timezone.utc) - check_search_value.last_search_date

        if check_time.total_seconds() > int(config["time_config"]):
        ################## GOOGLE API SEARCH #####################
            google_result = get_google_search(my_api_key, my_cse_id, search_item, ip['data'])
            if google_result["status"]!=200:
                return JsonResponse(status=int(google_result["status"]), data=google_result["data"], safe=False)
            
            return JsonResponse(status=200, data=google_result["data"], safe=False)
        else:
        ################### SEARCH IN DB #######################
            db_result = get_data_from_db(search_item, ip['data'])
            if db_result:
                return JsonResponse(status=200, data=db_result, safe=False)
            else:
                return JsonResponse(status=500, data=db_result, safe=False)
    else:
        return JsonResponse(status=500, data=ip["data"], safe=False)

def set_configure_data(request):
    """Funkcja odpowiedzialna za ustawienie konfiguracji po 
    jakim czasie dane zostną pobierane z bazy lub z API
    
    Args:
        request (Http request): Http request z danymi w postaci JSON {
            config_id(int): id z bazy (jeżeli będzie null zostanie założony nowy rekord)
            time_config(str): czas po jakim dane będą pobierane z bazy lub z API w sekundach
        }
    
    Returns:
        (http response): Odpowiedz http wraz z danymi w postaci JSON
    """
    try:
        try:
            data_frontend = json.loads(request.body.decode("utf-8"))
        except ValueError:
            return JsonResponse(status=400, data="", safe=False)

        config_data = SearchConfig.objects.get(id=data_frontend["config_id"])
        config_data.time_config = data_frontend["time_config"]
        config_data.modification_date = datetime.now()
        config_data.save()
    
    except KeyError:
        return JsonResponse(status=400, data="", safe=False)

    except SearchConfig.DoesNotExist:
        create_config = SearchConfig()
        create_config.time_config = data_frontend["time_config"]
        create_config.save()

    except BaseException:
        return JsonResponse(status=500, data="", safe=False)
    return JsonResponse(status=200, data="Pomyślnie dodano konfigurację.", safe=False)


def get_configuration_data(request):
    """Funkcja odpowiedziala na pobranie danych konfiguracyjnych
    
    Args:
        request (Http request): Zapytanie http
    
    Returns:
        (http response): odpowiedz http wraz z danymi w postaci json
    """
    try:
        data_to_send = list(SearchConfig.objects.all().values())
    except SearchConfig.DoesNotExist:
        return JsonResponse(status=200, data="", safe=False)

    except BaseException:
        return JsonResponse(status=500, data="", safe=False)

    if data_to_send:
        return JsonResponse(status=200, data=data_to_send, safe=False)
    else:
        return JsonResponse(status=200, data="", safe=False)
