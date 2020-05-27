class Block:
    def __init__(self,rows,cols):
        self.cols = cols
        self.rows = rows
        self.blocks = {}
    
    def doBlock(self,b):
        assert b[0] < self.rows and b[1] < self.cols,"Invalid row and Col"
        self.blocks[b] = True
    
    def unBlock(self,b):
        self.blocks.pop(b,True)

    def getsBlocks(self):
        return self.blocks
    
    def __eq__(self,blk2):
        if self.cols == blk2.cols and self.rows == blk2.cols and self.blocks == blk2.blocks:
            return True
        return False