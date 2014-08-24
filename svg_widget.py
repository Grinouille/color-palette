
from string import Template
from PyQt4 import QtGui, QtSvg, QtCore

from colors import *
from spaces import *
import svg
import transform
import matching

class SvgTemplateWidget(QtSvg.QSvgWidget):
    template_loaded = QtCore.pyqtSignal()
    colors_matched = QtCore.pyqtSignal()

    def __init__(self, *args):
        QtSvg.QSvgWidget.__init__(self, *args)
        self._colors = [Color(i*10,i*10,i*10) for i in range(20)]
        self._template = None
        self._template_filename = None
        self._svg = None
        self._need_render = True
        self._svg_colors = None
        self._dst_colors = None

    def _get_color(self, i):
        if i < len(self._colors):
            return self._colors[i]
        else:
            return Color(i*10, i*10, i*10)
    
    def _update(self):
        arr = QtCore.QByteArray.fromRawData(self.get_svg())
        print("Data loaded: {} bytes".format(arr.length()))
        self.load(arr)
        self.update()

    def loadTemplate(self, filename):
        self._template_filename = filename
        self._svg_colors, self._template = svg.read_template(filename)
        print("Source SVG colors:")
        for c in self._svg_colors:
            print str(c)
        print("Template loaded: {}: {} bytes".format(filename, len(self._template)))
        self._need_render = True
        self._update()
        self.template_loaded.emit()

    def set_color(self, idx, color):
        self._colors[idx] = color
        self._need_render = True
        self._update()

    def setColors(self, dst_colors):
        self._dst_colors = dst_colors
        self._colors = matching.match_colors(self._svg_colors, dst_colors)
        self._need_render = True
        self._update()
        self.colors_matched.emit()

    def resetColors(self):
        self.load(self._template_filename)
        self.repaint()

    def get_svg_colors(self):
        return self._svg_colors
    
    def get_dst_colors(self):
        return self._colors

    def get_svg(self):
        if self._svg is not None and not self._need_render:
            return self._svg
        else:
            self._svg = self._render()
            self._need_render = False
            return self._svg

    def _render(self):
        d = dict([("color"+str(i), color.hex() if color is not None else Color(255,255,255)) for i, color in enumerate(self._colors)])
        return Template(self._template).substitute(d)

        
