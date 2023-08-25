"""
PySide/PyQt 's need for QSugar is like coffee's need for sugar.

They are not essential, but they can make everything easier to accept.

So, just enjoy it.
                                                --- Dev.Ranor
"""

from .layout import layoutInterfaceInject, Layout
from .prop import propInterfaceInject, Prop
from .utils import *
from .widgets import *


def register(*qt_class_or_module, include=None) -> None:
    """
    Qt module/class QSugar enhanced registration function
    :param include: QSugar modules included
    :param qt_class_or_module:Qt class or module
    """
    if include is None:
        include = ['Prop', 'Layout']

    for each in qt_class_or_module:
        typename = type(each).__name__
        if typename in ('type', 'ObjectType'):
            if 'Prop' in include:
                propInterfaceInject(each)
            if 'Layout' in include:
                layoutInterfaceInject(each)
        elif typename == 'module':
            for module_obj in dir(each):
                if hasattr(each, module_obj):
                    register(getattr(each, module_obj))
