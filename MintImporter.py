#!/usr/bin/env python

import sys
import wx
import wx.lib.filebrowsebutton as filebrowse
import subprocess
import json
import csv
import datetime
import os
import random
import time

#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    # def OnSetFocus(self, evt):
    #     print("OnSetFocus")
    #     evt.Skip()
    # def OnKillFocus(self, evt):
    #     print("OnKillFocus")
    #     evt.Skip()
    # def OnWindowDestroy(self, evt):
    #     print("OnWindowDestroy")
    #     evt.Skip()

    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        self.panel = wx.Panel(self,-1)
        
        self.fbb = filebrowse.FileBrowseButton(
            self, -1, size=(450, -1), changeCallback = self.fbbCallback
            )

        l1 = wx.StaticText(self, -1, "Cookie")
        t1 = wx.TextCtrl(self, -1, "", size=(125, -1))
        wx.CallAfter(t1.SetInsertionPoint, 0)
        self.cookie = t1

        self.Bind(wx.EVT_TEXT, self.EvtText, t1)
        t1.Bind(wx.EVT_CHAR, self.EvtChar)
        # t1.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        # t1.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        # t1.Bind(wx.EVT_WINDOW_DESTROY, self.OnWindowDestroy)

        l2 = wx.StaticText(self, -1, "token")
        t2 = wx.TextCtrl(self, -1, "", size=(125, -1))
        wx.CallAfter(t2.SetInsertionPoint, 0)
        self.token = t2

        self.Bind(wx.EVT_TEXT, self.EvtText, t2)
        t2.Bind(wx.EVT_CHAR, self.EvtChar)

        b = wx.Button(self, -1, "Import")
        self.Bind(wx.EVT_BUTTON, self.Import, b)

        space = 6
        bsizer = wx.BoxSizer(wx.VERTICAL)
        bsizer.Add(b, 0, wx.GROW | wx.ALL, space)

        sizer = wx.FlexGridSizer(cols=1, hgap=space, vgap=space)
        sizer.AddMany([l1, t1,
                       l2, t2,
                       bsizer])
        border = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.fbb, 0, wx.ALL, 5)
        sizer.Add(bsizer, 0, wx.ALL, 5)
        border.Add(sizer, 0, wx.ALL, 25)
        self.SetSizer(border)
        self.SetAutoLayout(True)

    def fbbCallback(self, evt):
        self.log.write('FileBrowseButton: %s\n' % evt.GetString())

    def EvtText(self, event):
        self.log.WriteText('EvtText: %s\n' % event.GetString())

    def EvtTextEnter(self, event):
        self.log.WriteText('EvtTextEnter\n')
        event.Skip()

    def EvtChar(self, event):
        self.log.WriteText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()

    def Import(self, evt):
        print("Cookie is " + self.cookie.GetValue())
        cookie = self.cookie.GetValue()
        print("Token is " + self.token.GetValue())
        token = self.token.GetValue()
        print("File is " + self.fbb.GetValue())
      #  f = open("changes.txt", "w")
      #  f.write(cookie+"\n"+token+"\n"+self.fbb.GetValue())
      #  f.close()
        data = {}
        data['changes'] = []
        data['changes'].append({
            'cookie': self.cookie.GetValue(),
            'token': self.token.GetValue(),
            'csv_name': self.fbb.GetValue(),
        })

        with open('changes.txt', 'w') as outfile:
            json.dump(data, outfile)


        secondWindow = window2(parent=self.panel)
        secondWindow.Show()

class window2(wx.Frame):

    title = "Importer"

    def __init__(self,parent):
        wx.Frame.__init__(self,parent, -1,'Importing...', size=(500,320))
        panel=wx.Panel(self, -1)

        self.SetBackgroundColour(wx.Colour(100,100,100))
        self.Centre()
        self.Show()

        self.text1 = wx.TextCtrl(self, -1, '', wx.DefaultPosition, wx.Size(500,300),
                            wx.NO_BORDER | wx.TE_MULTILINE)
        p = subprocess.Popen(["python", "-u", "import.py"], stdout=subprocess.PIPE, bufsize=-1)
        self.pid = p.pid
        while p.poll() is None:
            x = p.stdout.readline().decode() #decode bytes but don't strip linefeeds
            self.text1.write(x)
            wx.GetApp().Yield() # Yield to MainLoop for interactive Gui
#---------------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#---------------------------------------------------------------------------


overview = """\
A TextCtrl allows text to be displayed and (possibly) edited. It may be single
line or multi-line, support styles or not, be read-only or not, and even supports
text masking for such things as passwords.


"""


if __name__ == '__main__':
    import sys
    import os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
