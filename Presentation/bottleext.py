import os
import bottle
from bottle import *
from bottle import TEMPLATE_PATH


# Potrebujemo, če želimo, da imamo html datoteke v pod mapi
TEMPLATE_PATH.append('./Presentation/views')

class Route(bottle.Route):
    """
    Nadomestni razred za poti s privzetimi imeni.
    """
    def __init__(self, app, rule, method, callback, name=None, plugins=None, skiplist=None, **config):
        if name is None:
            name = callback.__name__
        def decorator(*largs, **kwargs):
            bottle.request.environ['SCRIPT_NAME'] = os.environ.get('BOTTLE_ROOT', '')
            return callback(*largs, **kwargs)
        super().__init__(app, rule, method, decorator, name, plugins, skiplist, **config)

def template(*largs, **kwargs):
    if 'url' not in kwargs:
        kwargs['url'] = bottle.url
    return bottle.template(*largs, **kwargs)


def template_user(*largs, **kwargs):
    """
    Izpis predloge s podajanjem funkcije url in dodanim uporabnikom ter njegovo.
    """
    # Dodamo ime uporabnika, ki je prebran iz cookija direktno v vsak html, ki ga uporabimo kot template.
    usr_cookie = request.get_cookie("uporabnik")
    usr_role = request.get_cookie("rola")
    return bottle.template(*largs, **kwargs, uporabnik=usr_cookie, rola=usr_role, url=bottle.url)



bottle.Route = Route

