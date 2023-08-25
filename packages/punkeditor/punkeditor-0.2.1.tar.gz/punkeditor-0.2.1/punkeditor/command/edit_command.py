from dataclasses import dataclass
from argparse import ArgumentParser
import os
import curses

from punkeditor.command import PunkEditorCommand
from punkeditor.editbox import EditBox


@dataclass
class EditCommand(PunkEditorCommand):

    name = 'edit'

    def loop(self, window: curses.window):
        window.bkgd(' ')
        window.border()
        window.refresh()
        maxy, maxx = window.getmaxyx()
        subwin = window.subwin(maxy-2, maxx-2, 1, 1)
        box = EditBox(subwin, insert_mode=True)
        self.result = box.edit()

    def execute(self):
        curses.wrapper(self.loop)
        return self.result
