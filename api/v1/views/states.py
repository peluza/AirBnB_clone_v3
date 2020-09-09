from models.base_model import BaseModel, Base
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def allstates(state_id=None):
    """ jsonify """
    if state_id is None:
        lista = []
        for v in storage.all(State).values():
            lista.append(v.to_dict())
        return (jsonify(lista))
    else:
        flag = 0
        for v in storage.all(State).values():
            if v.id == state_id:
                attr = (v.to_dict())
                flag = 1
        if flag == 0:
            abort(404)
        else:
            return (jsonify(attr))


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete(state_id=None):
    if state_id is None:
        abort(404)
    dicti = {}
    flag = 0
    for v in storage.all(State).values():
        if v.id == state_id:
            storage.delete(v)
            storage.save()
            flag = 1
    if flag == 0:
        abort(404)
    else:
        return (jsonify(dicti), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_task():
    if not request.json or not 'name' in request.json:
        abort(400)

    result = request.get_json()
    obj = State()
    for k, v in result.items():
        setattr(obj, k, v)
    storage.new(obj)
    storage.save()
    var = obj.to_dict()
    return (jsonify(var), 201)