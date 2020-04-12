"""
 Simple Gui for CA 2d using wxpython gui library. 
 Implemented by: Anas Gauba
"""

import wx 
import secondVariantRuleGA 
from CABoard import *
from CA2dSIRDynamics import CA2dSIRDynamics

i = 0

class CA2dGUI(wx.Frame):
    def __init__(self, parent, title, ca):
        super(CA2dGUI, self).__init__(parent, title=title, size=(600, 600))

        self.ca = ca
        self.initFrame()

    def initFrame(self):

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Iteration = 0')
        self.board = CABoardPanel(self, self.ca, self.statusbar)
        self.board.SetBackgroundColour(wx.Colour(128,128,128))
        self.board.SetFocus()

        # centres the frame.
        self.Centre()
        

class CABoardPanel(wx.Panel):

    boardWidth = CABoard._board_col
    boardHeight = CABoard._board_row
    ID_TIMER = 1

    def __init__(self, parent, ca, statusbar):
        super(CABoardPanel, self).__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)
        
        # initialize stuff
        self.ca = ca
        self.statusBar = statusbar
        self.timer = wx.Timer(self, CABoardPanel.ID_TIMER)
        self.board = []
        # needed this because DrawRectangle() only deals with ints, and not doubles.
        self.widthRemainder = 0
        self.heightRemainder = 0

        # some event handlers.
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=CABoardPanel.ID_TIMER)
        self.Bind(wx.EVT_SIZE, self.Size)
        self.timer.Start(10000)

    def Size(self, event):
        return event.GetSize()

    def OnTimer(self, event):
        if event.GetId() == CABoardPanel.ID_TIMER:
            self.Refresh()
            self.Update()

        else:
            event.Skip()


    def squareWidth(self):
        self.widthRemainder = self.GetSize().GetWidth() % CABoardPanel.boardWidth
        return self.GetSize().GetWidth() // CABoardPanel.boardWidth

    def squareHeight(self):
        self.heightRemainder = self.GetSize().GetHeight() % CABoardPanel.boardHeight
        return self.GetSize().GetHeight() // CABoardPanel.boardHeight

    def OnPaint(self, event):
        global i
        dc = wx.PaintDC(self)
        
        board = self.ca.currentBoard.getBoard()

        blockSizeW = self.squareWidth()
        blockSizeH = self.squareHeight()

        for y in range(0,CABoard._board_col):
            for x in range(0, CABoard._board_row):
                if (board[x][y] == "S"):
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0))
                    dc.SetBrush(wx.Brush(wx.GREEN))
                    dc.DrawRectangle(x*blockSizeW+self.widthRemainder/2,y*blockSizeH+self.heightRemainder/2,blockSizeW,blockSizeH)
                elif board[x][y] == "I":
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0))
                    dc.SetBrush(wx.Brush(wx.RED_BRUSH))
                    dc.DrawRectangle(x*blockSizeW+self.widthRemainder/2,y*blockSizeH+self.heightRemainder/2,blockSizeW,blockSizeH)
                elif board[x][y] == "i":
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0))
                    # oragne color
                    dc.SetBrush(wx.Brush("#FF7F00"))
                    dc.DrawRectangle(x*blockSizeW+self.widthRemainder/2,y*blockSizeH+self.heightRemainder/2,blockSizeW,blockSizeH)  
                elif board[x][y] == "r":                    
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0))
                    dc.SetBrush(wx.Brush("black"))
                    dc.DrawRectangle(x*blockSizeW+self.widthRemainder/2,y*blockSizeH+self.heightRemainder/2,blockSizeW,blockSizeH)
                else:
                    dc.SetPen(wx.Pen(wx.LIGHT_GREY, 0))
                    dc.SetBrush(wx.Brush("blue"))
                    dc.DrawRectangle(x*blockSizeW+self.widthRemainder/2,y*blockSizeH+self.heightRemainder/2,blockSizeW,blockSizeH)
        
        # done with this iteration, do it again, update the iteration statusBar.
        board = self.ca.iterateCABoard().getBoard()
        i += 1
        self.statusBar.SetStatusText("Iteration = " + str(i))

def main():
    app = wx.App()

    print("\nWelcome to the simulation of using multiple variants of Covid-19 disease epidemic spread using Cellular Automata (CA) model with SIR dynamics.")

    print("You have four possible options to simulate the Covid-19 spread:")
    print(" 1. Use 1-variant of Covid-19 disease with determinstic rule mapping.")
    print(" 2. Use 1-variant of Covid-19 disease with non-deterministic rule mapping.")
    print(" 3. Add second variant of Covid-19 disease (always uses non-deterministic) without Genetic Algorithm (GA's) solution.")
    print(" 4. Add second variant of Covid-19 disease (always uses non-deterministic) with GA's solution.")
    simulation = input("Please select which variant of the simulation you would like to run? 1,2,3, or 4:\n")

    if (simulation == str(1)):
        boardObj = CABoard()
        ca = CA2dSIRDynamics(boardObj)

    elif (simulation == str(2)):
        boardObj = CABoard()
        ca = CA2dSIRDynamics(boardObj,ruleTypeIsDeterministic=False)

    elif (simulation == str(3)):
        boardObj = CABoard(isBoardRandom=True)
        ca = CA2dSIRDynamics(boardObj,diseaseVariants=2,ruleTypeIsDeterministic=False)

    elif (simulation == str(4)):
        boardObj = CABoard(isBoardRandom=True)
        ca = CA2dSIRDynamics(boardObj,diseaseVariants=2,ruleTypeIsDeterministic=False)
        ca.nonDeterministicRule2ndVar = secondVariantRuleGA.ruleFor2ndVariant

    else:
        errMessage = "Invalid user input: {}. Please select values from 1 to 4 again.".format(simulation)
        raise Exception(errMessage)

    ex = CA2dGUI(None, "CA 2d Dynamics", ca)
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()