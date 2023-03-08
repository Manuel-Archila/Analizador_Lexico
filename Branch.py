class Branch(object):
    def __init__(self,nullable=None, firstpos= None, lastpos =None, value="",leftChildren=None,rightChildren=None, pos = None):
        self.nullable=nullable
        self.firstpos=firstpos
        self.lastpos=lastpos
        self.value=value
        self.pos = pos
        self.leftChildren=leftChildren
        self.rightChildren=rightChildren

    def __repr__(self):
        return ('value -> %s leftChildren -> %s rightChildren -> %s \n' % (self.value, self.leftChildren, self.rightChildren))