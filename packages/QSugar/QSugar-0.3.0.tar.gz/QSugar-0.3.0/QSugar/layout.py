from typing import Iterable

try:
    from Qt.QtCore import Qt
    from Qt.QtWidgets import QWidget, QLayout
except ImportError:
    from qtpy.QtCore import Qt
    from qtpy.QtWidgets import QWidget, QLayout


class EasyLayoutInterface:
    """
    QSuagr Layout Extension Interface
    which extends `__getitem__` method , `align` nad `stretch` params in `prop`
    """

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
    '''
    Alignment property value and Qt alignment flag mapping dictionary
    '''

    def __getitem__(self, *children):
        """
        QSuagr nesting containers method simplifying `addWidget` and `andLayout`
        :param children: children
        :return: method caller
        """
        while isinstance(children, tuple) and len(children) == 1:
            children = children[0]

        if isinstance(children, Iterable):
            for row, row_children in enumerate(children):
                if isinstance(row_children, Iterable):
                    for col, child in enumerate(row_children):

                        if isinstance(child, slice):
                            on_init = child.stop
                            on_del = child.step
                            child = child.start

                            if on_init:
                                on_init(child)
                            if on_del:
                                child.__del__ = on_del

                        if isinstance(child, QWidget):
                            self.addWidget(child, row, col)
                        elif isinstance(child, QLayout):
                            self.addLayout(child, row, col)

                else:
                    child = row_children

                    if isinstance(child, slice):
                        on_init = child.stop
                        on_del = child.step
                        child = child.start

                        if on_init:
                            on_init(child)
                        if on_del:
                            child.__del__ = on_del

                    args = [child]

                    stretch = child.property("stretch")
                    if stretch:
                        args.append(stretch)

                    align = child.property("align")
                    if align:
                        align = self.AlignFlags[align]
                        if not stretch:
                            args.append(1)
                        args.append(align)

                    if isinstance(child, QWidget):
                        self.addWidget(*args)
                    elif isinstance(child, QLayout):
                        self.addLayout(*args)

        else:
            child = children
            args = [child]

            if isinstance(child, slice):
                on_init = child.stop
                on_del = child.step
                child = child.start
                if on_init:
                    on_init(child)
                if on_del:
                    child.__del__ = on_del

                stretch = child.property("stretch")
                if stretch:
                    args.append(stretch)

                align = child.property("align")
                if align:
                    if not stretch:
                        args.append(1)
                    align = self.AlignFlags[align]
                    args.append(align)

            if isinstance(child, QWidget):
                self.addWidget(*args)
            elif isinstance(child, QLayout):
                self.addLayout(*args)

        return self


Layout = EasyLayoutInterface


def layoutInterfaceInject(class_):
    """
    QSugar layout extension interface injection method
    :param class_: Qt class
    """
    if issubclass(class_, QLayout):
        class_.AlignFlags = EasyLayoutInterface.AlignFlags
        class_.__getitem__ = EasyLayoutInterface.__getitem__
