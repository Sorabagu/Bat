import wx
import wx.stc as stc
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SuccessDialog(wx.Dialog):
    def __init__(self, parent, message, title="Success"):
        super(SuccessDialog, self).__init__(parent, title=title, size=(300, 150))
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="Cascadia Code")
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label=message)
        text.SetForegroundColour(wx.Colour(0, 255, 0))
        text.SetBackgroundColour(wx.Colour(0, 0, 0))
        text.SetFont(font)
        sizer.Add(text, 1, wx.ALIGN_CENTER|wx.ALL, 10)
        ok_btn = wx.Button(self, wx.ID_OK, label="OK")
        ok_btn.SetBackgroundColour(wx.Colour(17, 17, 17))
        ok_btn.SetForegroundColour(wx.Colour(0, 255, 0))
        ok_btn.SetFont(font)
        sizer.Add(ok_btn, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        self.SetSizer(sizer)
        self.Centre()

class EditorBatFrame(wx.Frame):
    def __init__(self, parent, title, initial_content=""):
        super(EditorBatFrame, self).__init__(parent, title=title, size=(800, 600))
        
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.SetIcon(wx.Icon(resource_path("icon.ico"), wx.BITMAP_TYPE_ICO))
        self.SetWindowStyleFlag(wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="Cascadia Code")
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        commands = [
            "ASSOC", "BREAK", "CALL", "CD", "CHDIR", "CHCP", "CLS", "COLOR", "COPY", "DATE",
            "DEL", "DIR", "ECHO", "ENDLOCAL", "EXIT", "FC", "FIND", "FINDSTR", "FOR", "FTYPE",
            "GOTO", "IF", "MD", "MKDIR", "MOVE", "PATH", "PAUSE", "POPD", "PRINT", "PROMPT",
            "PUSHD", "RD", "RMDIR", "REM", "REN", "RENAME", "SET", "SETLOCAL", "SHIFT", "START",
            "TIME", "TITLE", "TYPE", "VER", "VERIFY", "VOL", "HELP", "CHOICE", "DOSKEY", "TREE",
            "XCOPY", "ROBOCOPY", "ATTRIB", "COMP", "COMPACT", "CONVERT", "LABEL", "MODE", "SORT",
            "REPLACE", "RECOVER"
        ]
        self.cmd_list = wx.ListBox(self.panel, choices=commands)
        self.cmd_list.SetBackgroundColour(wx.Colour(17, 17, 17))
        self.cmd_list.SetForegroundColour(wx.Colour(0, 255, 0))
        self.cmd_list.SetFont(font)
        self.cmd_list.Bind(wx.EVT_LISTBOX_DCLICK, self.on_command_dclick)
        hbox.Add(self.cmd_list, 0, wx.EXPAND | wx.ALL, 5)
        
        self.text_ctrl = stc.StyledTextCtrl(self.panel)
        self.text_ctrl.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.text_ctrl.StyleSetBackground(stc.STC_STYLE_DEFAULT, wx.Colour(0, 0, 0))
        self.text_ctrl.SetLexer(stc.STC_LEX_CONTAINER)
        self.text_ctrl.StyleClearAll()
        self.text_ctrl.StyleSetSpec(stc.STC_STYLE_DEFAULT,
            "face:Cascadia Code,size:10,fore:#00FF00,back:#000000")
        self.text_ctrl.StyleSetSpec(0, "fore:#00FF00,back:#000000")
        self.text_ctrl.StyleSetSpec(1, "fore:#00AA00,italic,back:#000000")
        self.text_ctrl.StyleSetSpec(2, "fore:#66FF66,bold,back:#000000")
        self.text_ctrl.StyleSetSpec(3, "fore:#66FFFF,bold,back:#000000")
        self.text_ctrl.StyleSetSpec(4, "fore:#FF66FF,back:#000000")
        self.text_ctrl.StyleSetSpec(5, "fore:#FFFF66,back:#000000")
        self.text_ctrl.SetCaretForeground(wx.Colour(0, 255, 0))
        self.text_ctrl.SetCaretStyle(stc.STC_CARETSTYLE_BLOCK)
        self.text_ctrl.Bind(stc.EVT_STC_STYLENEEDED, self.OnStyleNeeded)
        hbox.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        
        vbox.Add(hbox, 1, wx.EXPAND)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.AddStretchSpacer()
        save_btn = wx.Button(self.panel, label="Save")
        save_btn.SetBackgroundColour(wx.Colour(17, 17, 17))
        save_btn.SetForegroundColour(wx.Colour(0, 255, 0))
        save_btn.SetFont(font)
        btn_sizer.Add(save_btn, 0, wx.ALL, 5)
        vbox.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        self.panel.SetSizer(vbox)
        
        if initial_content:
            self.text_ctrl.SetText(initial_content)
        
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        
        self.Center()
        self.Show()
    
    def on_command_dclick(self, event):
        selection = self.cmd_list.GetStringSelection()
        if selection:
            pos = self.text_ctrl.GetCurrentPos()
            self.text_ctrl.InsertText(pos, selection + " ")
    
    def OnStyleNeeded(self, event):
        startPos = self.text_ctrl.GetEndStyled()
        endPos = self.text_ctrl.GetTextLength()
        text = self.text_ctrl.GetTextRange(startPos, endPos)
        self.text_ctrl.StartStyling(startPos)
        for line in text.splitlines(keepends=True):
            stripped_line = line.lstrip()
            if stripped_line.startswith("::"):
                self.text_ctrl.SetStyling(len(line), 1)
            elif stripped_line.startswith(":"):
                self.text_ctrl.SetStyling(len(line), 3)
            else:
                i = 0
                while i < len(line):
                    ch = line[i]
                    if ch == '"':
                        start_str = i
                        i += 1
                        while i < len(line) and line[i] != '"':
                            i += 1
                        if i < len(line):
                            i += 1
                        token_length = i - start_str
                        self.text_ctrl.SetStyling(token_length, 5)
                    elif ch == '%':
                        start_var = i
                        i += 1
                        while i < len(line) and line[i] != '%':
                            i += 1
                        if i < len(line) and line[i] == '%':
                            i += 1
                        token_length = i - start_var
                        self.text_ctrl.SetStyling(token_length, 4)
                    elif ch.isalnum():
                        start_word = i
                        while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                            i += 1
                        word = line[start_word:i]
                        keywords = {"echo", "pause", "set", "if", "goto", "for", "call", "start",
                                    "shutdown", "cls", "dir", "copy", "del", "md", "rd"}
                        if word.lower() in keywords:
                            self.text_ctrl.SetStyling(i - start_word, 2)
                        else:
                            self.text_ctrl.SetStyling(i - start_word, 0)
                    else:
                        self.text_ctrl.SetStyling(1, 0)
                        i += 1
        event.Skip()

    def on_save(self, event):
        dlg = wx.FileDialog(self, "Save BAT file", "", "", "BAT files (*.bat)|*.bat",
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
            content = self.text_ctrl.GetText()
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                dlg_success = SuccessDialog(self, "File created successfully!", "Success")
                dlg_success.ShowModal()
                dlg_success.Destroy()
            except Exception as e:
                wx.MessageBox(f"Error saving file:\n{e}", "Error", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

    def on_close(self, event):
        self.Destroy()
        wx.GetApp().ExitMainLoop()

if __name__ == '__main__':
    app = wx.App(False)
    EditorBatFrame(None, "BAT - Editor", initial_content="")
    app.MainLoop()
