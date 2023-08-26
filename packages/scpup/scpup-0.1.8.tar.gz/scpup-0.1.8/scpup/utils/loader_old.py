from __future__ import annotations

import os
import json
from typing import Any, Callable, Literal, Optional, TypeVar
from functools import partial, wraps
import pygame, pygame.freetype, pygame.mixer


ResourceType = TypeVar("ResourceType", pygame.freetype.Font, pygame.mixer.Sound, pygame.Surface, Any)
ConfigurationFunction = Callable[[[Any], Optional[ResourceType]], Optional[Any]]
WrapperFunction = Callable[..., ResourceType]
Extension = Literal[".png", ".jpg", ".jpeg",  ".ttf", ".otf",  ".wav", ".ogg"]
ASSETS_BASE_PATH = os.path.join(__file__.split("src", 1).pop(0), "assets")
_assets: dict[str, ] = {}


def load_json(*paths) -> Optional[Any]:
    file = os.path.join(ASSETS_BASE_PATH, *paths)
    if not os.path.exists(file):
        return None
    with open(file, "r") as fp:
        jsonObj = json.load(fp)
    return jsonObj

def load_map(name: str) -> Optional[dict]:
    if not name.endswith(".json"):
        name += ".json"
    return load_json("maps", name)

def load_mblk(name: str) -> Optional[dict]:
    if not name.endswith(".mblk"):
        name += ".mblk"
    return load_json("mblks", name)

def save_mblk(name: str, data: dict) -> None:
    if not name.endswith(".mblk"):
        name += ".mblk"
    path = os.path.join(ASSETS_BASE_PATH, "mblks", name)
    with open(path, "w") as file:
        json.dump(data, file, indent=2)

def load_image(path: str, *paths: str, copy: bool = True) -> pygame.Surface:
    file = os.path.join(ASSETS_BASE_PATH, "images", path, *paths)
    if file not in _assets:
        try:
            _assets[file] = pygame.image.load(file)
        except Exception:
            print(f"Unable to load image: {file}")
            raise
    img = _assets[file]
    if img.get_alpha() is None:
        img = img.convert()
    else:
        img = img.convert_alpha()
    return img.copy() if copy else img

def load_sound(path: str, *paths: str) -> pygame.mixer.Sound:
    if not pygame.mixer:
        return None
    file = os.path.join(ASSETS_BASE_PATH, "sounds", path, *paths)
    if file not in _assets:
        try:
            _assets[file] = pygame.mixer.Sound(file)
        except Exception:
            print(f"Unable to load sound: {file}")
            raise
    return _assets[file]

def load_font(path: str, *paths: str, origin: bool = False) -> pygame.freetype.Font:
    file = os.path.join(ASSETS_BASE_PATH, "fonts", path, *paths)
    if file not in _assets:
        try:
            font = pygame.freetype.Font(file)
            font.origin = origin
            _assets[file] = font
        except Exception:
            raise
    return _assets[file]

def Resource(path: str, /, *paths: str, eager: bool=False, origin: bool=False, copy: bool=True, **_other) -> Callable[[ConfigurationFunction], ResourceType | WrapperFunction]:
    filename = (path if len(paths) == 0 else paths[-1]).lower()
    if filename.endswith((".png", ".jpg", ".jpeg")):
        fn = partial(load_image, copy=copy)
    elif filename.endswith((".wav", ".ogg")):
        fn = load_sound
    elif filename.endswith((".ttf", ".otf")):
        fn = partial(load_font, origin=origin)
    elif filename.endswith(".json"):
        fn = load_json
    elif eager:
        fmt = filename.rsplit(".", 1).pop()
        raise NotImplementedError(f"Unknown format: {fmt:!r}")
    else:
        fn = None
    def decorator(configfn: ConfigurationFunction) -> ResourceType | WrapperFunction:
        if eager:
            _item_: ResourceType = fn(path, *paths)
            if configfn.__code__.co_argcount == 1:
                configfn(_item_)
            else:
                configfn()
            return _item_
        else:
            @wraps(configfn)
            def wrapper(self_or_cls: Any, *subpaths, **kwargs) -> ResourceType:
                if hasattr(configfn, "_names_"):
                    _item_: list[ResourceType] = []
                    for name in configfn._names_:
                        filename = name if name.endswith(".png") else f"{name}.png"
                        _item_.append(load_image(path, *paths, *subpaths, filename, copy=copy))
                else:
                    if fn is not None:
                        _item_: ResourceType = fn(path, *paths)
                    else:
                        if len(subpaths) == 0:
                            raise RuntimeError("Load function couldn't be defined and subpaths were not provided!")
                        filename = subpaths[-1]
                        filename = filename.lower()
                        if filename.endswith((".png", ".jpg", ".jpeg")):
                            _item_: ResourceType = load_image(path, *paths, *subpaths, copy=copy)
                        elif filename.endswith((".wav", ".ogg")):
                            _item_: ResourceType = load_sound(path, *paths, *subpaths)
                        elif filename.endswith((".ttf", ".otf")):
                            _item_: ResourceType = load_font(path, *paths, *subpaths, origin=origin)
                        elif filename.endswith(".json"):
                            _item_: ResourceType = load_json(path, *paths, *subpaths)
                        else:
                            raise NotImplementedError(f"Unknown format for value '{filename}'")
                _kwargs = _other.copy()
                _kwargs.update(kwargs)
                if callable(self_or_cls):
                    # Class method (Call to constructor)
                    # Keep in mind that the decorated function does not get called # Nevermind
                    instance = self_or_cls(_item_, **_kwargs)
                    # return configfn(instance) or instance
                    return instance
                else:
                    # Instance method (Call to function)
                    return configfn(self_or_cls, _item_, **_kwargs)
            return wrapper
    return decorator


def ResourceClass(path: str, *paths: str, restype: Literal["image", "sound", "font"], **defaults):
    def decorator(res_cls: Any):
        resdir = [name for name in dir(res_cls) if not name.startswith("_")]
        for p in resdir:
            attr = getattr(res_cls, p)
            if callable(attr) and not hasattr(attr, '_not_resource_') and attr.__qualname__.removesuffix(f".{p}") == res_cls.__name__:
                props = defaults.copy()
                props.update(getattr(attr, "_resource_params_", {}))
                subpaths = getattr(attr, "_subpaths_", [])
                if not getattr(attr, "_incomplete_", False):
                    extension = \
                        ".png" if restype == "image" else \
                        ".wav" if restype == "sound" else \
                        ".ttf" if restype == "font" else \
                        None
                    if extension is None:
                        raise TypeError(f"Missing resource type for class {res_cls.__name__}")
                    subpaths += (f"{p}{extension}",)
                res = Resource(path, *paths, *subpaths, **props)(attr)
                setattr(res_cls, p, classmethod(res))
        return res_cls
    return decorator


def ResourceParams(**kwargs):
    def decorator(fn):
        fn._resource_params_ = kwargs.copy()
        return fn
    return decorator


def ResourcePath(path: str, *paths: str):
    def decorator(fn):
        fn._subpaths_ = (path,) + paths
        return fn
    return decorator


def NotResource(fn):
    fn._not_resource_ = True
    return fn


def IncompleteResource(fn):
    fn._incomplete_ = True
    return fn


def MultipleImages(*filenames):
    def decorator(fn):
        if len(filenames) > 0:
            fn = IncompleteResource(fn)
            fn._names_ = filenames
        return fn
    return decorator

