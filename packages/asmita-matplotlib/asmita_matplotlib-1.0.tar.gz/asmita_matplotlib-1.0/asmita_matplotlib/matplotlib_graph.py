class Figure :
    def __init__(self):
        self.plot=[]

    def add_subplot(self,*arg):
        ax = arg
        self.plot.append(ax)
        return ax
    
figure = Figure()
figure.add_subplot(1,1,2,1)

        