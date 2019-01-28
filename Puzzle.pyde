add_library('sound')
import os, random
path=os.getcwd() 

class Tile:
    def __init__(self,r,c,v):
        self.r=r
        self.c=c
        self.v=v
        self.img=loadImage(path+"/"+str(self.v)+".png")
        
    def display (self):
        image(self.img,self.c*100+5,self.r*100+5)

class Puzzle:
    def __init__(self,numRows,numCols):
        self.numRows=numRows
        self.numCols=numCols
        self.neighbours=[[0,-1],[0,1],[-1,0],[1,0]]
        self.music=SoundFile(this,path+'/banana.mp3')
        self.gameOverSound=SoundFile(this,path+'/TaDa.mp3')
        self.createPuzzle()
        self.shufflePuzzle()
        self.gameOver=False
        self.music.play()
        
    def createPuzzle(self):
        self.board=[]
        self.hiddenBoard=[]
        v=0
        for r in range(self.numRows):
            for c in range(self.numCols):
                self.board.append(Tile(r,c,v))
                if v!=self.numRows*self.numCols-1:
                    self.hiddenBoard.append(Tile(r,c,v))
                elif v==self.numRows*self.numCols-1:
                    self.hiddenBoard.append(Tile(r,c,v+1))
                v+=1
            
    def getTile(self,r,c):
        for i in self.board:
            if i.r == r and i.c == c:
                return i
    
    def shufflePuzzle(self):
        for o in range(50):
            for i in self.board:
                if i.v==self.numRows*self.numCols-1:
                    nTile = self.getTile(self.numRows,self.numCols)
                    while nTile == None or nTile.v==self.numRows*self.numCols-1: 
                        n = random.choice(self.neighbours)
                        nTile = self.getTile(i.r+n[0],i.c+n[1])
                        
                    self.swapTiles(i,nTile)
                    break
    
    def swapTiles(self,i,nTile):            
        x=i.r
        y=i.c
        i.r = nTile.r
        i.c = nTile.c
        nTile.r = x
        nTile.c = y                                                                

    def swap(self,i):
        self.i=i
        for t in self.neighbours:
            if self.i.r+t[0] in range(self.numRows) and self.i.c+t[1] in range(self.numCols):
                nTile=self.getTile(self.i.r+t[0],self.i.c+t[1])
                if nTile.v==self.numRows*self.numCols-1:
                    self.swapTiles(self.i,nTile)
                    return
                    break
    
    def winCheck(self):
        if self.gameOver==False:
            over=0
            for final in range(self.numRows*self.numCols-1):
                if self.board[final].r==self.hiddenBoard[final].r and self.board[final].c==self.hiddenBoard[final].c:
                    over+=1
            if over==self.numRows*self.numCols-1:
                self.gameOverSound.play()
                self.music.stop()
                self.gameOver=True
            
    def display(self):
        if self.gameOver:
            for h in self.hiddenBoard:
                h.display()
        else:
            for t in self.board:
                t.display()
             
puzzle=Puzzle(4,4)

def setup():
    size(puzzle.numCols*100+10,puzzle.numRows*100+10)
    background(255)
    
def draw():
    background(255,0,0)
    puzzle.display()
    
def mouseClicked():
    if puzzle.gameOver:
        puzzle.__init__(4,4)
        return
    
    for i in puzzle.board:
        if i.c*100 <= mouseX <= i.c*100+100 and i.r*100 <= mouseY <= i.r*100+100:
               puzzle.swap(i)
               puzzle.winCheck()
               return