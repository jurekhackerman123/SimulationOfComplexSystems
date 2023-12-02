from TradingStrategies import * 
from stocks import *
from AgentClass import * 


# global variables 
NUMBEROFDAYS = 100

INITIALPRICE = 100  # Initial stock price
DRIFT = 0.0001       # Drift term
VOLATILITY = 0.01  # Volatility term
NUMBEROFSIMULATIONS = 5  # Number of simulations

DT = 1/24

# initial money for agent 
INITIALMONEY = 1000

def MainSimulation(initialMoney, tradingStrategy, show): 

    stock = GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)

    # define agent 
    agent = Agent(initialMoney, tradingStrategy, stock, holdsAtOnce=5)

    print('how much money does this guy have???', initialMoney)

    for timeStep in range(len(stock)): 

        agent.take_action(timeStep, stock)

    # if the end of the stock is reached and the agent is still holding stocks, sell all the stocks for the current price 
    while len(agent.sellList) < len(agent.buyList): 
        agent.sell(stock, timeStep, agent.taxFactor)

    print(agent.buyList)
    print(agent.sellList)

    if show: 
        for i in range(len(agent.buyList)):
            plt.scatter(agent.buyList[i], stock[agent.buyList[i]], s= 200, color = 'red')#, label = 'Buy')
            plt.scatter(agent.sellList[i], stock[agent.sellList[i]], s=200, color = 'green')#, label = 'Sell')
        ShowStock(stock, False, 0, False, [5, 20], NUMBEROFDAYS, DT, 'Profit: ' + str(agent.money - initialMoney))
        # plt.plot(stock)
        # plt.legend()
        plt.show()
    
    print('current money after trading: ', agent.money)


# MainSimulation(INITIALMONEY, BreakOut, True)



def CompareTradingStrategies(initialMoney, holdsAtOnce, numberOfAverages): 

    # one stock (for now, only one) that all agents with all different trading strategies will follow 
    globalStock = GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)

    stockList = []
    for i in range(numberOfAverages): 

        stockList.append(GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT))

    # all the trading strategies
    namesList = ['BuyAndHold', 'MovingAverage', 'Crossover', 'MeanReversion', 'Rangetrading', 'BO', 'MorningNight', 'Scalping', 'Random'] 


    # list to store the profits that certain agents make following a certain strategy 
    profitList = np.zeros(len(namesList))

    # iterate over the different stocks: 
    for globalStock in stockList:

        # define different agents for all 10 (9) trading strategies: 

        agentBAH = Agent(initialMoney, BuyAndHold, globalStock, holdsAtOnce=holdsAtOnce)

        agentMA = Agent(initialMoney, MovingAverage, globalStock, holdsAtOnce=holdsAtOnce)

        agentCO = Agent(initialMoney, CrossOverMovingAverage, globalStock, holdsAtOnce=holdsAtOnce)

        agentMR = Agent(initialMoney, MeanReversion, globalStock, holdsAtOnce=holdsAtOnce)

        agentRT = Agent(initialMoney, RangeTrading, globalStock, holdsAtOnce=holdsAtOnce)

        agentBO = Agent(initialMoney, BreakOut, globalStock, holdsAtOnce=holdsAtOnce)

        agentMN = Agent(initialMoney, BuyMorningSellNight, globalStock, holdsAtOnce=holdsAtOnce)

        agentSC = Agent(initialMoney, Scalping, globalStock, holdsAtOnce=holdsAtOnce)

        agentRandom = Agent(initialMoney, BuyAndSellRandomly, globalStock, holdsAtOnce=holdsAtOnce)  

        agentList = [agentBAH, agentMA, agentCO, agentMR, agentRT, agentBO, agentMN, agentSC, agentRandom]

        



        for timeStep in range(len(globalStock)):

            for agent in agentList: 

                agent.take_action(timeStep, globalStock)

            
        for agentNo in range(len(agentList)): 

            agent = agentList[agentNo]

            while len(agent.sellList) < len(agent.buyList): 
                agent.sell(globalStock, timeStep, agent.taxFactor)
            
            profitList[agentNo] += (agent.money - initialMoney)

            # plot stuff that is better than BuyAndHold

            # if profitList[-1] > profitList[0]: 

            #     for i in range(len(agent.buyList)):
            #         plt.scatter(agent.buyList[i], globalStock[agent.buyList[i]], s= 200, color = 'red')#, label = 'Buy')
            #         plt.scatter(agent.sellList[i], globalStock[agent.sellList[i]], s=200, color = 'green')#, label = 'Sell')
            #     ShowStock(globalStock, False, 0, False, [5, 20], NUMBEROFDAYS, DT, 'Profit: ' + str(agent.money - initialMoney) + ' ' + namesList[agentNo])
            #     # plt.plot(stock)
            #     # plt.legend()
            #     plt.show()
    
    # after iteration of stocks is done, average over number 
    profitList = profitList / numberOfAverages


    # show a histogram of money of agents: 

    colors = []

    for i in (profitList): 
        if i >= 0: 
            colors.append('green')
        else: 
            colors.append('red')

    bars = plt.bar(namesList ,profitList, color = colors)
    plt.title('Comparison of profits with different trading strategies')
    plt.ylabel('Profit')
    # plt.xlabel('Trading Strategy')
    plt.xticks(rotation = 45, fontsize = 8)
    plt.show()


CompareTradingStrategies(1000, 5, 100)



