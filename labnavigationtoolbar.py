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

from matplotlib.backends.backend_qt4 import NavigationToolbar2QT

class CustomNavigationToolbar(NavigationToolbar2QT):

    def __init__(self, canvas, parent, coordinates=True):
        self.curveX = {}
        self.curveY = {}
        self.error = 0.01
        self.curve_point = {}
        self.last_plot = {}
        self.canvas = canvas
        NavigationToolbar2QT.__init__(self, canvas, parent, coordinates)
        self._id_scroll_event = self.canvas.mpl_connect('scroll_event', self._on_mouse_scroll)
        self._id_mouse_button_release = self.canvas.mpl_connect('button_release_event', self._on_mouse_button_release)

    def init_curve_point(self, axes):
        if axes:
            for axe, x, y in axes:
                self.curve_point[axe] = 0
                self.curveX[axe] = x
                self.curveY[axe] = y
                self.last_plot[axe] = None

    def _show_points(self, axe):
        s = 'X: {:.5f}, Y: {:.5f}'.format(self.curveX[axe][self.curve_point[axe]], self.curveY[axe][self.curve_point[axe]])
        self.set_message(s)

    def _draw_curve_point(self, axe):
        # removing any previous plot
        if axe in self.last_plot and self.last_plot[axe] != None:
            self.last_plot[axe][0].remove()
        # Finding xy pixel with xy data
        if self.curve_point[axe] != None:
            #print self.canvas.figure.get_axes() 
            #ax = self.canvas.figure.get_axes()[0]
            xdata, ydata = self.curveX[axe][self.curve_point[axe]], self.curveY[axe][self.curve_point[axe]]
            xpix, ypix = axe.transData.transform(np.vstack([xdata, ydata]).T).T
            #print 'Xdata:', xdata, 'Xpixel:', xpix
            #print 'Ydata:', ydata, 'Ypixel:', ypix
            self.last_plot[axe] = axe.plot([xdata], [ydata], 'bo')
            self.draw()
            self._show_points(axe)

    def _has_curve_axes(self, axe):
        return (axe in self.curveX and axe in self.curveY) and (len(self.curveX[axe]) and len(self.curveY[axe]))

    def _move_curve_point(self, axe, step):
        if axe in self.curve_point.keys():
            if step < 0:
                if self.curve_point[axe] > 0:
                    self.curve_point[axe] -= 1
            elif step > 0:
                if self.curve_point[axe] < len(self.curveX[axe]):
                    self.curve_point[axe] += 1

    def _on_mouse_scroll(self, event):
        #print 'Step? ', event.step
        if event.inaxes and self._active not in ('PAN', 'ZOOM') and self._has_curve_axes(event.inaxes):
            self._move_curve_point(event.inaxes, event.step)
            self._draw_curve_point(event.inaxes)

    def _on_mouse_button_release(self, event):
        # event.inaxes is the solution
        #print event.inaxes.name, ' id:', id(event.inaxes)
        #print '------'
        #print 'Event Xdata:', event.xdata, '({})'.format(event.x), 'Event Ydata:', event.ydata, '({})'.format(event.y)
        if event.inaxes and self._active not in ('PAN', 'ZOOM') and self._has_curve_axes(event.inaxes):
            for i, xdata in enumerate(self.curveX[event.inaxes]):
                ydata = self.curveY[event.inaxes][i]
                event_ydata = event.ydata
                #print 'x:', xdata, 'error: ', abs(xdata - event.xdata),
                #print ' y:', ydata, 'error: ', abs(ydata - event.ydata)
                if abs(xdata - event.xdata) <= self.error and abs(ydata - event.ydata) <= self.error:
                    #print 'Found: Xdata = ', xdata, 'Ydata = ', ydata
                    self.curve_point[event.inaxes] = i
                    self._draw_curve_point(event.inaxes)
                    break

    #def mouse_move(self, event):
    #    self._set_cursor(event)