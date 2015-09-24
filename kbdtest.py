#!/usr/bin/python

"""
This is intended to be a script for testing the physical keys on keyboards. The idea is as follows:
1) run with --train mode, with a JPEG/PNG key layout file given. User presses a key, then clicks the
corresponding location on the image. A green circle appears. Coordinates and key code are recorded in
a hash, indexed by key code. Continue until all keys for a given layout are pressed. Press a special
key combination or click a button, and the hash is pickled and saved to disk.

2) Normal mode, every time a key is pressed, a green circle is drawn at the corresponding spot on
the selected keyboard layout. User can easily see which keys aren't working on a keyboard.

The problem here is that we need to be able to read the raw scan codes sent from the keyboard - i.e.
if we can't read and differentiate each and every key on the keyboard - i.e. left-ctrl from right-ctrl
from print screen from pause/break from F24 - it's useless.

References for finishing this:
http://www.velocityreviews.com/forums/t320050-reading-keyboard-scan-codes.html
http://www.thelinuxdaily.com/2010/05/grab-raw-keyboard-input-from-event-device-node-devinputevent/
"""

import sys
import wx
from PIL import Image
import subprocess
import argparse
import logging

FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger(__name__)

class MyFrame(wx.Frame):

    def __init__(self, parent, title, width, height):
        self.img_width = width
        self.img_height = height
        wx.Frame.__init__(self, parent, -1, title, size=(width, height))

        """
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        """
        self.bitmap = wx.Bitmap('us_qwerty_104key.png')
        self.bitmap.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)
        self.bitmap.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        wx.EVT_PAINT(self, self.OnPaint)
        self.Centre()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0)
        self.dc = dc

    def OnKeyDown(self, event):
        logger.debug(event)
        logger.debug(dir(event))
        logger.debug(vars(event))
        print(event.ControlDown())
        print(event.GetKeyCode())
        print(event.GetRawKeyCode())
        event.Skip()
        return

    def OnMouseClick(self, event):
        pos = event.GetPosition()
        x = pos[0]
        y = pos[1]
        print(pos)
        self.dc.SetBrush(wx.Brush('green'))
        self.dc.DrawCircle(x, y, 10)

    def run(self):
        pass

class MyApp(wx.App):
    def OnInit(self):
        im = Image.open('us_qwerty_104key.png')
        ims = im.size
        frame = MyFrame(None, 'kbdtest', ims[0], ims[1])
        frame.Show(True)
        frame.SetFocus()
        return True

def parse_args(argv):
    """
    parse arguments/options

    this uses the new argparse module instead of optparse
    see: <https://docs.python.org/2/library/argparse.html>
    """
    p = argparse.ArgumentParser(description='Show keyboard key presses to test'
                                ' a keyboard.')
    p.add_argument('-v', '--verbose', dest='verbose', action='count', default=0,
                   help='verbose output. specify twice for debug-level output.')
    args = p.parse_args(argv)
    return args

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    if args.verbose > 1:
        logger.setLevel(logging.DEBUG)
    elif args.verbose > 0:
        logger.setLevel(logging.INFO)
    app = MyApp(0)
    app.MainLoop()
