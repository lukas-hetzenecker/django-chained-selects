# -*- coding: utf-8 -*-

import locale

from django.db.models import get_model
from django.http import HttpResponse
from django.utils import simplejson


def filterchain_all(request, app_name, model_name, method_name, pk):
    Model = get_model(app_name, model_name)
    pk = pk.split(':')
    results = getattr(Model, method_name)(*pk)
    final = []
    for item in results:
        for field in Model.chained_child_pk_field():
            _pk += str(item[field]) + ':'
        _pk = _pk[:-1]
        final.append({'value': _pk, 'display': item[Model.chained_child_visible_field()]})
    json = simplejson.dumps(final)
    return HttpResponse(json, mimetype='application/json')
