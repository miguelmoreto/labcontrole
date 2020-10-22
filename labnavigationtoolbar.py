#-*- coding: utf-8 -*-
#==============================================================================
# This file is part of LabControle 2.
# 
# LabControle 2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
# 
# LabControle 2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with LabControle 2.  If not, see <http://www.gnu.org/licenses/>.
#==============================================================================
#==============================================================================
# Este arquivo é parte do programa LabControle 2
# 
# LabControle 2 é um software livre; você pode redistribui-lo e/ou 
# modifica-lo dentro dos termos da Licença Pública Geral GNU como 
# publicada pela Fundação do Software Livre (FSF); na versão 3 da 
# Licença.
# Este programa é distribuido na esperança que possa ser  util, 
# mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a 
# qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral
# GNU para maiores detalhes.
# 
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#==============================================================================
#
# Developed by Miguel Moreto
# Florianopolis, Brazil, 2015

import numpy as np

from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.qt_compat import (
    QtCore,
    QtGui,
    QtWidgets
)


class CustomNavigationToolbar(NavigationToolbar2QT):

    def __init__(self, canvas, parent, coordinates=True):
        self.curveX = {}
        self.curveY = {}
        self.error = 0.01
        self.curve_point = {}
        self.last_plot = {}
        self.siblings = []
        self.text_coordinates = u''
        self.last_message = u''
        self.canvas = canvas
        self._drag_mode = False
        NavigationToolbar2QT.__init__(self, canvas, parent, coordinates)
        self._id_scroll_event = self.canvas.mpl_connect('scroll_event', self._on_mouse_scroll)
        self._id_mouse_button_release = self.canvas.mpl_connect('button_release_event', self._on_mouse_button_release)

    def init_curve_point(self, axes):
        if axes:
            for axis, x, y in axes:
                self.curve_point[axis] = 0
                self.curveX[axis] = x
                self.curveY[axis] = y
                self.last_plot[axis] = None

    def clear_curve_point(self):
        self.curve_point = {}
        self.curveX = {}
        self.curveY = {}
        self.last_plot = {}

    def _set_axis_view_points(self, axis):
        self.text_coordinates = 'X: {:.5f}, Y: {:.5f}'.format(self.curveX[axis][self.curve_point[axis]], self.curveY[axis][self.curve_point[axis]])

    def _show_points(self, axis):
        self._set_axis_view_points(axis)
        self.set_message(self.last_message)

    def _draw_curve_point(self, axis):
        # removing any previous plot
        if axis in self.last_plot and self.last_plot[axis] != None:
            self.last_plot[axis][0].remove()
        # Finding xy pixel with xy data
        if self.curve_point[axis] != None:
            #print self.canvas.figure.get_axes() 
            #ax = self.canvas.figure.get_axes()[0]
            xdata, ydata = self.curveX[axis][self.curve_point[axis]], self.curveY[axis][self.curve_point[axis]]
            xpix, ypix = axis.transData.transform(np.vstack([xdata, ydata]).T).T
            #print 'Xdata:', xdata, 'Xpixel:', xpix
            #print 'Ydata:', ydata, 'Ypixel:', ypix
            self.last_plot[axis] = axis.plot([xdata], [ydata], 'bo')
            # draw() was deprecated in Matplotlib 3.3
            # self.draw()
            # New method to render canvas
            self.canvas.draw_idle()
            self._show_points(axis)

    def _draw_curve_axes(self, axis):
        if self.siblings and axis in self.siblings:
            for axis_parent in self.siblings:
                if axis_parent != axis:
                    self.curve_point[axis_parent] = self.curve_point[axis]
                self._draw_curve_point(axis_parent)
            # Show values for this axis
            self._show_points(axis)
        else:
            self._draw_curve_point(axis)


    def _has_curve_axes(self, axis):
        return (axis in self.curveX and axis in self.curveY) and (len(self.curveX[axis]) and len(self.curveY[axis]))

    def _move_curve_point(self, axis, step):
        if axis in self.curve_point.keys():
            if step < 0:
                if self.curve_point[axis] > 0:
                    self.curve_point[axis] -= 1
            elif step > 0:
                if self.curve_point[axis] < len(self.curveX[axis]):
                    self.curve_point[axis] += 1

    def _on_mouse_scroll(self, event):
        #if event.inaxes and self._active not in ('PAN', 'ZOOM') and self._has_curve_axes(event.inaxes):
        if event.inaxes and self._has_curve_axes(event.inaxes):
            self._move_curve_point(event.inaxes, event.step)
            self._draw_curve_axes(event.inaxes)

    def _on_mouse_button_release(self, event):
        if event.button == 1 and event.inaxes and not self._drag_mode and self._has_curve_axes(event.inaxes):
            for i, xdata in enumerate(self.curveX[event.inaxes]):
                if abs(xdata - event.xdata) <= self.error:
                    #print 'Found: Xdata = ', xdata, 'Ydata = ', ydata
                    self.curve_point[event.inaxes] = i
                    self._draw_curve_axes(event.inaxes)
                    break
        self._drag_mode = False

    def set_message(self, s):
        self.message.emit(s)
        text_label = s
        if self.coordinates:
            text_label = s.replace(', ', '\n')
        if self.text_coordinates:
            text_label = '{}\n{}'.format(text_label, self.text_coordinates)
        self.locLabel.setText(text_label)
        self.last_message = s

    def mouse_move(self, event):
        if event.inaxes:
            self.mode = u''
            if self._has_curve_axes(event.inaxes):
                self._set_axis_view_points(event.inaxes)
        NavigationToolbar2QT.mouse_move(self, event)

    def press(self, event):
        self._drag_mode = False

    def drag_pan(self, event):
        self._drag_mode = True
        NavigationToolbar2QT.drag_pan(self, event)

    def drag_zoom(self, event):
        self._drag_mode = True
        NavigationToolbar2QT.drag_zoom(self, event)

