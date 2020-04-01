"""
 Simple Gui for CA 2d using wxpython gui library. 
 Implemented by: Anas Gauba
"""

import wx 
from CABoard import *
from CA2dSIRDynamicsPart2a import CA2dSIRDeterministicDynamics

i = 0

# TODO: Need to look into resizing of window so the board panel also gets resized
class CA2dGUI(wx.Frame):
    def __init__(self, parent, title, ca):
        super(CA2dGUI, self).__init__(parent, title=title, size=(CABoard._board_col*10, CABoard._board_row*10))

        self.ca = ca
        self.initFrame()

    def initFrame(self):

        self.statusbar = self.CreateStatusBar()
        #self.statusbar.SetStatusText('0')
        self.statusbar.SetStatusText('0')
        self.board = CABoardPanel(self, self.ca, self.statusbar)
        self.board.SetFocus()
        # self.board.start()

        #self.SetTitle("CA 2d Dynamics")
        # centres the frame.
        self.Centre()
        

class CABoardPanel(wx.Panel):

    boardWidth = CABoard._board_col
    boardHeight = CABoard._board_row
    ID_TIMER = 1

    def __init__(self, parent, ca, statusbar):
        #super(CABoardPanel, self).__init__(*args, **kw)
        super(CABoardPanel, self).__init__(parent)
        
        # initialize stuff
        self.ca = ca
        self.statusBar = statusbar
        self.timer = wx.Timer(self, CABoardPanel.ID_TIMER)
        self.board = []
        
        # TODO: if time permits, add Start and Pause Buttons to the gui.
        self.isStarted = False
        self.isPaused = False

        # some event handlers.
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=CABoardPanel.ID_TIMER)
        self.Bind(wx.EVT_SIZE, self.Size)
        self.timer.Start(10000)

    def Size(self, event):
        return event.GetSize()

    def OnTimer(self, event):
        if event.GetId() == CABoardPanel.ID_TIMER:
            # figure out a better way to refresh.
            self.Refresh()
            self.Update()

        else:
            event.Skip()


    def squareWidth(self):
        return self.GetSize().GetWidth() // CABoardPanel.boardWidth

    def squareHeight(self):

        return self.GetSize().GetHeight() // CABoardPanel.boardHeight

    def OnPaint(self, event):
        global i
        dc = wx.PaintDC(self)
        wx.BufferedDC(dc)
        board = self.ca.currentBoard.getBoard()

        # need to fix the pixel issue so the cells align well with the frame.
        pixelWidth = self.GetSize().GetWidth()
        pixelHeight = self.GetSize().GetHeight()
        if (pixelWidth < pixelHeight):
            blockSize = self.squareWidth()
        else:
            blockSize = self.squareHeight()

        for y in range(0,CABoard._board_col):
            for x in range(0, CABoard._board_row):
                if (board[x][y] == "S"):
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0))
                    dc.SetBrush(wx.Brush(wx.GREEN))
                    dc.DrawRectangle(x*blockSize,y*blockSize,blockSize,blockSize)
                elif board[x][y] == "I":
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0))
                    dc.SetBrush(wx.Brush(wx.RED_BRUSH))
                    dc.DrawRectangle(x*blockSize,y*blockSize,blockSize,blockSize)
                elif board[x][y] == "i":
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0))
                    # oragne color
                    dc.SetBrush(wx.Brush("#FF7F00"))
                    dc.DrawRectangle(x*blockSize,y*blockSize,blockSize,blockSize)  
                elif board[x][y] == "r":                    
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0))
                    dc.SetBrush(wx.Brush("black"))
                    dc.DrawRectangle(x*blockSize,y*blockSize,blockSize,blockSize)
                else:
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0))
                    dc.SetBrush(wx.Brush("blue"))
                    dc.DrawRectangle(x*blockSize,y*blockSize,blockSize,blockSize)
        
        # done with this iteration, do it again, update the iteration statusBar.
        board = self.ca.iterateCABoard().getBoard()
        i += 1
        self.statusBar.SetStatusText(str(i))

def main():

    app = wx.App()
    boardObj = CABoard(isBoardRandom=True)
    ca = CA2dSIRDeterministicDynamics(boardObj, diseaseVariants=2, ruleTypeIsDeterministic=False)
    ex = CA2dGUI(None, "CA 2d Dynamics", ca)
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()