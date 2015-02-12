class FruitShop:

    def __init__(self, name, fruitPrices):

        self.fruitPrices = fruitPrices
        self.name = name
        print 'Welcome to the %s fruit shop' % (name)
        
    def getCostPerPound(self, fruit):

        if fruit not in self.fruitPrices:
            print "Sorry we don't have %s" % (fruit)
            return None
        return self.fruitPrices[fruit]
        
    def getPriceOfOrder(self, orderList):

        totalCost = 0.0             
        for fruit, numPounds in orderList:
            costPerPound = self.getCostPerPound(fruit)
            if costPerPound != None:
                totalCost += numPounds * costPerPound
        return totalCost
    
    def getName(self):
        return self.name