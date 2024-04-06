# -*- coding:utf-8 -*-
#
# Copyright (C) 2018 sthoo <sth201807@gmail.com>
#
# Support: Report an issue at https://github.com/sth2018/FastWordQuery/issues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version; http://www.gnu.org/copyleft/gpl.html.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import subprocess
from aqt.qt import *

from ..context import config
from ..lang import _, _sl
from ..service import service_manager, service_pool
from .base import WIDGET_SIZE, Dialog

# 2x3 compatible
if sys.hexversion >= 0x03000000:
    unicode = str

__all__ = ['DictManageDialog']


class DictManageDialog(Dialog):
    """
    Dictionary manager window. enabled or disabled dictionary, and setting params of dictionary.
    """

    def __init__(self, parent, title=u'Dictionary Manager'):
        super(DictManageDialog, self).__init__(parent, title)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        text_line = QLabel(_('EDITOR_NAME_NOTE'))
        text_line.setWordWrap(True)
        self.edit_line = QLineEdit()
        self.edit_line.setPlaceholderText("editor name")
        self.main_layout.addWidget(text_line)
        self.main_layout.addWidget(self.edit_line)
        self._options = list()
        btnbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok, Qt.Orientation.Horizontal, self)
        btnbox.accepted.connect(self.accept)
        self.scroll = QWidget()
        self.scroll.setMinimumSize(250, 1100)
        # add dicts mapping
        self.dicts_layout = QGridLayout(self.scroll)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.scroll)
        self.main_layout.addWidget(self.scroll_area)
        # self.main_layout.addLayout(self.dicts_layout)
        self.main_layout.addWidget(btnbox)
        self.build()


    def build(self):
        """ """
        # labels
        f = QFont()
        f.setBold(True)
        labels = ['', '']
        for i, s in enumerate(labels):
            if s:
                label = QLabel(_(s))
                label.setFont(f)
                label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
                self.dicts_layout.addWidget(label, 0, i)
        # enabled all
        self.enabled_all_check_btn = QCheckBox(_('DICTS_NAME'))
        self.enabled_all_check_btn.setFont(f)
        self.enabled_all_check_btn.setEnabled(True)
        self.enabled_all_check_btn.setChecked(True)
        # signal
        self.enabled_all_check_btn.clicked.connect(self.enabled_all_changed)
        # add widgets
        self.dicts_layout.addWidget(self.enabled_all_check_btn, 0, 0)
        # dict service list
        confs = config.dicts
        dicts = list()
        services = service_manager.local_custom_services + service_manager.web_services
        for clazz in services:
            dicts.append({
                'title':
                clazz.__title__,
                'unique':
                clazz.__unique__,
                'path':
                clazz.__path__,
                'enabled':
                confs.get(clazz.__unique__, dict()).get('enabled', True)
            })
        # add dict
        for i, d in enumerate(dicts):
            self.add_dict_layout(i, **d)
        # update
        self.enabled_all_update()
        self.adjustSize()

    def add_dict_layout(self, i, **kwargs):
        # args
        title, unique, enabled, path = (
            kwargs.get('title', u''),
            kwargs.get('unique', u''),
            kwargs.get('enabled', False),
            kwargs.get('path', u''),
        )
        # button
        check_btn = QCheckBox(title)
        check_btn.setMinimumSize(WIDGET_SIZE.map_dict_width * 2, 0)
        check_btn.setEnabled(True)
        check_btn.setChecked(enabled)
        edit_btn = QToolButton(self)
        edit_btn.setText(_('EDIT'))
        # signal
        check_btn.stateChanged.connect(self.enabled_all_update)
        edit_btn.clicked.connect(lambda: self.on_edit(path))
        # add
        self.dicts_layout.addWidget(check_btn, i + 1, 0)
        self.dicts_layout.addWidget(edit_btn, i + 1, 1)
        self._options.append({
            'unique': unique,
            'check_btn': check_btn,
            'edit_btn': edit_btn,
        })

    def enabled_all_update(self):
        b = True
        for row in self._options:
            if not row['check_btn'].isChecked():
                b = False
                break
        self.enabled_all_check_btn.setChecked(b)

    def enabled_all_changed(self):
        b = self.enabled_all_check_btn.isChecked()
        for row in self._options:
            row['check_btn'].setChecked(b)

    def on_edit(self, path):
        """edit dictionary file"""

        print("[FWQ] open dict path:", path)
        try:
            on_edit = self.edit_line.text()
            self.open_text_editor(path, on_edit)
        except:
            pass

    def open_text_editor(self, filename, editor=""):
        if editor:
            subprocess.Popen([f"{editor}", filename])
        elif sys.platform == 'win32':
            os.system(f"start notepad {filename}")
        elif sys.platform == 'darwin':
            subprocess.Popen(["open", filename])
        elif sys.platform == 'linux':
            os.system(f"xdg-open {filename}")
        else:
            subprocess.Popen(["code", filename])

    def accept(self):
        """ok button clicked"""
        self.save()
        super(DictManageDialog, self).accept()

    def save(self):
        """save config to file"""
        data = dict()
        dicts = {}
        for row in self._options:
            dicts[row['unique']] = {
                'enabled': row['check_btn'].isChecked(),
            }
        data['dicts'] = dicts
        config.update(data)
