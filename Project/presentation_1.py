import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

class Presentation:
    datas = None
    def __init__(self, _PathData):
        self.datas = pd.read_csv(os.getcwd() + _PathData)
        
    
    def barChart_HowManyNamesDoesEachGeneHave(self):
        df = pd.DataFrame(self.datas, columns= ['GeneSymbol', 'GeneID', 'AlsoKnowAs'])
        
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]
        
        for index, row in df.iterrows():

            CountAlsoKnowAs = 0
            
            if ( len( row['AlsoKnowAs'] ) == 2 ):
                y[0] = y[0] + 1
            else:
                CountAlsoKnowAs = row['AlsoKnowAs'].count(';') + 1
                y[CountAlsoKnowAs] = y[CountAlsoKnowAs] + 1
        
        print(x)
        print(y)
        
        plt.bar(x, y)
        plt.xlabel('How many names does each gene have?')
        plt.show()
    
    def barChart_1(self):
                
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        y = [208437, 281572, 9035, 243, 10, 5, 3, 10, 2, 1, 2, 1, 1, 4, 6, 0, 0, 0, 2, 1]
        
        plt.bar(x, y, width=0.2)
        for i in range(len(x)):
            plt.text( i, y[i], '<=' + str(y[i]),
                    # ha = 'left',
                    # va = 'top',
                    rotation= 45,
                    )
        plt.xlabel('')
        
        plt.show()
        
    def barChart_2_eventRelationship(self):
        previousID = None
        countSameProbeSetID = 0
        
        x = ["2", "3", "4", "5"]
        y = [0, 0, 0, 0]
        
        df = (pd.DataFrame(self.datas)).sort_values(by=['ProbeSetID'])
        for index, row in df.iterrows():
            
            if (previousID == row['ProbeSetID']):
                countSameProbeSetID = countSameProbeSetID + 1
            else:
                y[countSameProbeSetID] = y[countSameProbeSetID] + 1
                if ( countSameProbeSetID == 3):
                    print( previousID )
                countSameProbeSetID = 0
            
            if (index == 0):
                continue
            else:
                previousID = row['ProbeSetID']
        
        # plt.bar(x, y)
        
        # for i in range(len(x)):
        #     plt.text( i, y[i] + 150, str(y[i]),
        #             ha = 'center',
        #             # va = 'top',
        #             rotation = 0,
        #             fontsize = 12,
        #             bbox = dict(facecolor = 'red', alpha = 0.5)
        #             )
        # plt.xlabel('Number of unique relationships')
        # plt.ylabel('Number of SNP')
        # plt.show()
        
        plt.style.use("seaborn-dark")
        for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[param] = '0.9'  # very light grey

        for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[param] = '#212946'  # bluish dark grey

        colors = [
            '#08F7FE',  # teal/cyan
            '#FE53BB',  # pink
            '#F5D300',  # yellow
            '#00ff41',  # matrix green
        ]
        
        df = pd.DataFrame({'number': y})
        
        fig, ax = plt.subplots()
        
        df.plot( marker='o', color=colors, ax=ax )
        plt.show()
        
        return
        

if __name__ == "__main__": 
    
    presentation = Presentation("/GetDataOnWe/Dataset/eventRelationship_Nsp.csv")
    presentation.barChart_2_eventRelationship()