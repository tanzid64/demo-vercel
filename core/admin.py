from django.contrib import admin
from django.apps import apps

installed_apps = apps.get_app_configs()

for app_config in installed_apps:
  models = app_config.get_models()
  for model in models:
    class ModelAdimn(admin.ModelAdmin):
      list_per_page = 10
    try:
      admin.site.unregister(model)
    except admin.sites.NotRegistered:
      pass
    admin.site.register(model, ModelAdimn)