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

import wx
from PIL import Image
import subprocess

class MyFrame(wx.Frame):
    keymap = None

    def __init__(self, parent, id, title, width, height):
        self.img_width = width
        self.img_height = height
        wx.Frame.__init__(self, parent, id, title, size = (width, height))

        self.bitmap = wx.Bitmap('us_qwerty_104key.png')
        wx.EVT_PAINT(self, self.OnPaint)

        self.Centre()
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0)
        self.dc = dc

    def OnKeyDown(self, event):
        print event.ControlDown()
        print event.GetKeyCode()
        print event.GetRawKeyCode()

    def OnMouseClick(self, event):
        pos = event.GetPosition()
        x = pos[0]
        y = pos[1]
        print pos
        self.dc.SetBrush(wx.Brush('green'))
        self.dc.DrawCircle(x, y, 10)

    def run(self):
        self.proc = subprocess.Popen("sudo /usr/bin/showkey", shell = True, stdout = subprocess.PIPE)
        inline = self.proc.stdout.readline()

class MyApp(wx.App):
    def OnInit(self):
        im = Image.open('us_qwerty_104key.png')
        ims = im.size
        frame = MyFrame(None, -1, 'kbdtest', ims[0], ims[1])
        im = None
        frame.Show(True)
        self.SetTopWindow(frame)
        frame.run()
        return True

app = MyApp(0)
app.MainLoop()
