from django.db import models
# from datetime import datetime



class SearchInformation(models.Model):
    user_ip_address = models.CharField(max_length=100, default="", blank=True)
    search_value = models.CharField(max_length=200, default="", blank=True)
    last_search_date = models.DateTimeField(auto_now_add=True, null=True)

class SearchConfig(models.Model):
    time_config = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    modification_date = models.DateTimeField(auto_now_add=True, null=True,)


class ResultSearch(models.Model):
    title = models.CharField(max_length=200, default="", blank=True)
    link_to_side = models.TextField(default="", blank=True)
    link_to_display = models.TextField(default="", blank=True)
    position = models.IntegerField(default=None, null=True)
    count_words = models.TextField(default="", blank=True)
    search_information_fk = models.ForeignKey("SearchInformation", on_delete=models.SET_NULL, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)