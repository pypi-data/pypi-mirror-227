import uuid
from typing import Iterable

try:
    from Qt.QtCore import QObject, Signal, Qt
    from Qt.QtGui import QPixmap, QColor
    from Qt.QtWidgets import QLabel, QGraphicsBlurEffect, QGraphicsOpacityEffect, QGraphicsColorizeEffect, \
        QGraphicsDropShadowEffect, QWidget
except ImportError:
    from qtpy.QtCore import QObject, Signal, Qt
    from qtpy.QtGui import QPixmap, QColor
    from qtpy.QtWidgets import QLabel, QGraphicsBlurEffect, QGraphicsOpacityEffect, QGraphicsColorizeEffect, \
        QGraphicsDropShadowEffect, QWidget


class EasyPropInterface:
    """
    QSuagr Property Extension Interface
    which extends `prop` and `__getitem__` method
    """

    PropMethodMap = {
        'qss': 'setStyleSheet',
        'max_width': 'setMaximumWidth',
        'min_width': 'setMinimumWidth',
        'max_height': 'setMaximumHeight',
        'min_height': 'setMinimumHeight',
        'max_size': 'setMaximumSize',
        'min_size': 'setMinimumSize',
        'width': 'setFixedWidth',
        'height': 'setFixedHeight',
        'size': 'setFixedSize',
        'margin': 'setContentsMargins',
    }
    '''
    QSugar property setter method mapping dictionary
    '''

    @staticmethod
    def name_prop_method(obj: QObject, value: str):
        """
        Default `name` property setter method definition
        """
        obj.setObjectName(value)
        if obj.parent():
            setattr(obj.parent(), value, obj)

    @staticmethod
    def style_prop_method(widget: QWidget, value: str):
        """
        Default `style` property setter method definition
        """
        if widget.objectName() == '':
            widget.setObjectName(str(uuid.uuid4()))
        qss = '#' + widget.objectName() + '{' + value + '}'
        widget.setStyleSheet(qss)

    @staticmethod
    def src_prop_method(obj: QObject, value: str):
        """
        Default `src` property setter method definition
        """
        if isinstance(obj, QPixmap):
            obj.load(value)
        elif isinstance(obj, QLabel):
            obj.setPixmap(QPixmap(value))

    @staticmethod
    def x_prop_method(widget: QWidget, value: int):
        """
        Default `x` property setter method definition
        """
        geometry = widget.geometry()
        geometry.setX(value)
        widget.setGeometry(geometry)

    @staticmethod
    def y_prop_method(widget: QWidget, value: int):
        """
        Default `y` property setter method definition
        """
        geometry = widget.geometry()
        geometry.setY(value)
        widget.setGeometry(geometry)

    @staticmethod
    def pos_prop_method(widget: QWidget, value: tuple):
        """
        Default `pos` property setter method definition
        """
        geometry = widget.geometry()
        geometry.setX(value[0])
        geometry.setY(value[1])
        widget.setGeometry(geometry)

    AlignFlags = {
        'justify': Qt.AlignJustify,
        'center': Qt.AlignCenter,
        'h_center': Qt.AlignHCenter,
        'v_center': Qt.AlignVCenter,
        'left': Qt.AlignLeft,
        'right': Qt.AlignRight,
        'top': Qt.AlignTop,
        'bottom': Qt.AlignBottom,
    }

    @staticmethod
    def align_content_prop_method(widget: QWidget, value: str):
        """
        Default `align_content` property setter method definition
        """
        widget.setAlignment(EasyPropInterface.AlignFlags[value])

    @staticmethod
    def opacity_prop_method(widget: QWidget, value: float):
        """
        Default `opacity` property setter method definition
        """
        widget.setWindowOpacity(value)
        effect = QGraphicsOpacityEffect(widget.parent())
        effect.setOpacity(value)
        widget.setGraphicsEffect(effect)

    @staticmethod
    def blur_prop_method(widget: QWidget, value: float):
        """
        Default `blur` property setter method definition
        """
        effect = QGraphicsBlurEffect(widget.parent())
        effect.setBlurRadius(value)
        widget.setGraphicsEffect(effect)

    @staticmethod
    def colorize_prop_method(widget: QWidget, value: tuple):
        """
        Default `colorize` property setter method definition
        """
        effect = QGraphicsColorizeEffect(widget.parent())
        value = list(value) if isinstance(value, Iterable) else [value]
        value.reverse()
        strength = value.pop()
        effect.setStrength(strength)
        if not value:
            color = widget.palette().background().color()
        else:
            color = value.pop()
            if not isinstance(color, str) and isinstance(color, Iterable):
                color = QColor(*color)
            else:
                color = QColor(color)
        effect.setColor(color)
        widget.setGraphicsEffect(effect)

    @staticmethod
    def shadow_prop_method(widget: QWidget, value: tuple):
        """
        Default `shadow` property setter method definition
        """
        effect = QGraphicsDropShadowEffect(widget.parent())
        value = list(value)
        value.reverse()
        x_offset, y_offset = value.pop(), value.pop()
        effect.setXOffset(x_offset)
        effect.setYOffset(y_offset)
        if value[-1] == 'blur':
            value.pop()
            effect.setBlurRadius(value.pop())
        color = value.pop()
        if not isinstance(color, str) and isinstance(color, Iterable):
            effect.setColor(QColor(*color))
        else:
            effect.setColor(QColor(color))
        widget.setGraphicsEffect(effect)

    PropMethodDefine = {
        'name': name_prop_method,
        'style': style_prop_method,
        'src': src_prop_method,
        'x': x_prop_method,
        'y': y_prop_method,
        'pos': pos_prop_method,
        'align_content': align_content_prop_method,
        'opacity': opacity_prop_method,
        'blur': blur_prop_method,
        'shadow': shadow_prop_method,
        'colorize': colorize_prop_method,
    }
    '''
    QSugar property setter method definition dictionary
    '''

    @staticmethod
    def style_prop_conflict_method(old_value: str, new_value: str):
        """
        Default `style` property conflict method definition
        """
        return old_value + ';\n' + new_value

    @staticmethod
    def qss_prop_conflict_method(old_value: str, new_value: str):
        """
        Default `qss` property conflict method definition
        """
        return old_value + ';\n' + new_value

    PropConflictMethodDefine = {
        'style': style_prop_conflict_method,
        'qss': qss_prop_conflict_method,
    }
    '''
    QSugar property conflict method definition dictionary
    '''

    @classmethod
    def def_prop(cls, name: str, func):
        """
        QSugar custom property setter definition method
        :param name:property name
        :param func:setter method func(obj,value)
        :return:`Prop` Class
        """
        cls.PropMethodDefine[name] = func
        return cls

    @classmethod
    def map_prop(cls, name: str, func_name: str):
        """
        QSugar custom property setter definition method
        :param name:property name
        :param func_name:setter method name
        :return:`Prop` Class
        """
        cls.PropMethodMap[name] = func_name
        return cls

    def prop(self, *prop_objs: Iterable[dict], **kwargs):
        """
        QSugar property setter method
        :param prop_objs: property injection dictionary
        :param kwargs: property key-value
        :return: method caller
        """
        if kwargs is None:
            kwargs = dict()

        for prop_obj in prop_objs:
            conflict_props = prop_obj.keys() & self.PropConflictMethodDefine.keys()
            if conflict_props == 0:
                kwargs.update(prop_obj)
            else:
                for prop in prop_obj:
                    if prop in conflict_props:
                        if prop in kwargs:
                            kwargs[prop] = self.PropConflictMethodDefine[prop](kwargs[prop], prop_obj[prop])
                        else:
                            kwargs[prop] = prop_obj[prop]
                    else:
                        kwargs[prop] = prop_obj[prop]

        for name_, value_ in kwargs.items():
            if name_ in self.PropMethodDefine:
                func = self.PropMethodDefine[name_]
                func(self, value_)
            elif name_ in self.PropMethodMap:
                setter_name = self.PropMethodMap[name_]
                setter = getattr(self, setter_name)
                try:
                    setter(value_)
                except TypeError as e:
                    if isinstance(value_, Iterable):
                        setter(*value_)
                    else:
                        raise e
            else:
                # Signal Property Mapper
                if name_.startswith('on'):
                    name_ = name_.removeprefix('on')
                    name_ += 'ed'
                    name_ = name_.lower()

                if hasattr(self, name_):
                    prop = getattr(self, name_)
                    if isinstance(prop, Signal):
                        prop.connect(value_)

                # Qt Default Property Mapper
                setter_name = 'set' + name_.title()
                if hasattr(self, setter_name):
                    setter = getattr(self, setter_name)
                    try:
                        setter(value_)
                    except TypeError as e:
                        if isinstance(value_, Iterable):
                            setter(*value_)
                        else:
                            raise e
                else:
                    self.setProperty(name_, value_),
        return self

    def __getitem__(self, children):
        """
        QSuagr nesting containers method simplifying `setXXX` and `addXXX`
        :param children:children
        :return:method caller
        """
        if isinstance(children, Iterable):
            for child in children:
                for class_ in type(child).mro():
                    class_name = class_.__name__.removeprefix('Q')
                    add_func_name = 'add' + class_name.title()
                    if hasattr(self, add_func_name):
                        add_func = getattr(self, add_func_name)
                        add_func(child)

                    setter_name = 'set' + class_name.title()
                    if hasattr(self, setter_name):
                        setter = getattr(self, setter_name)
                        setter(child)
        else:
            child = children
            for class_ in type(child).mro():
                class_name = class_.__name__.removeprefix('Q')
                add_func_name = 'add' + class_name.title()
                if hasattr(self, add_func_name):
                    add_func = getattr(self, add_func_name)
                    add_func(child)

                setter_name = 'set' + class_name.title()
                if hasattr(self, setter_name):
                    setter = getattr(self, setter_name)
                    setter(child)
        return self

    def set(self, prop, value):
        """
        QSugar reserved property setter method
        :param prop:property name
        :param value:property value
        :return:method caller
        """
        setter_name = "set" + prop.title()
        setter = getattr(self, setter_name)
        setter(value)
        return self

    def bind(self, signal: str, fn):
        """
        QSugar reserved signal and slots binding method
        :param signal: signal name
        :param fn: slots function
        :return: method caller
        """
        getattr(self, signal).connect(fn)
        return self

    def unbind(self, signal: str):
        """
        QSugar reserved signal and slots unbinding method
        :param signal: signal name
        :return: method caller
        """
        getattr(self, signal).disconnect()
        return self


Prop = EasyPropInterface


def propInterfaceInject(class_):
    """
    QSugar property extension interface injection method
    :param class_: Qt class
    """
    if issubclass(class_, object):
        class_.PropMethodMap = EasyPropInterface.PropMethodMap
        class_.PropMethodDefine = EasyPropInterface.PropMethodDefine
        class_.PropConflictMethodDefine = EasyPropInterface.PropConflictMethodDefine
        class_.prop = EasyPropInterface.prop
        class_.set = EasyPropInterface.set
    if issubclass(class_, QObject):
        class_.bind = EasyPropInterface.bind
        class_.unbind = EasyPropInterface.unbind
        class_.__getitem__ = EasyPropInterface.__getitem__
