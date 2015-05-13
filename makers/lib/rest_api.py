from flask import Response
from flask import json
from flask import request
from functools import wraps
from werkzeug.datastructures import MultiDict

from makers.models import Model


def post_json_to_tuples(post_data):
  for k, v in post_data.items():
    if isinstance(v, list):
      for value in v:
        yield (k, value)
    elif isinstance(v, bool):
      if v:
        yield (k, 'on')
    else:
      yield (k, v)

def rest_view(func):
  @wraps(func)
  def wrapped(*args, **kwargs):
    if request.method in ['POST', 'PUT']:
      params = json.loads(request.data)
      data = MultiDict(post_json_to_tuples(params))
      kwargs['data'] = data

    result = func(*args, **kwargs)

    if hasattr(result, '__iter__'):
      result = map(_simplify_model, result)

    elif isinstance(result, Model):
      result = result.dict()

    elif isinstance(result, Response):
      return result

    return json.dumps(result)

  return wrapped

def form_error(form):
  response = Response(status=400)
  response.data = json.dumps(form.errors)
  return response

def _simplify_model(model):
  return model.dict()


