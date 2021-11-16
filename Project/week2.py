import pandas as pd
import os

class SNP:
    def __init__(self, ProbeID, RSID, Chromosome, relationship, distance, GeneSymbol, NCBIGeneID, AlsoKnowAs):
        self.ProbeSetID = ProbeID
        self.dbSNPRSID = RSID
        self.Chromosome =  Chromosome
        self.relationship = relationship
        self.distance = distance
        self.GeneSymbol = GeneSymbol
        self.NCBIGeneID = NCBIGeneID
        self.AlsoKnowAs = AlsoKnowAs

def listfilename(path):
    listfile = os.listdir(path)
    return listfile

def ReadCSV(file):
    dataCSV = pd.read_csv(file)
    return dataCSV

if __name__ == "__main__":
    dfNCBI = ReadCSV( '/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/GetDataOnWe/Dataset/soknowas.csv')
    dataframeSNP = ReadCSV('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/GetDataOnWe/Dataset/Mapping250K_Nsp.na32.annot.csv')
    All_ProbeID = dataframeSNP['Probe Set ID']
    All_SnpID = dataframeSNP['dbSNP RS ID']
    All_Gene = dataframeSNP['Associated Gene']
    All_Chromosome = dataframeSNP['Chromosome']
    DataForExport = []
    eventchangedistance =[]
    eventNotsame =[]
    for row in range(dataframeSNP.shape[0]):#dataframeSNP.shape[0]
        print('row at: ', row)
        eachrow_ProbeID = All_ProbeID[row]
        eachrow_SnpID = All_SnpID[row]
        eachrow_Chromosome = All_Chromosome[row]
        eachrow_Gene = All_Gene[row]
        split_Gene = eachrow_Gene.split('///')
        memory = []
        listGeneInSNP = []
        if eachrow_ProbeID and eachrow_SnpID and eachrow_Gene != '---':
            for Gene in split_Gene:
                GeneDetail = Gene.split(' // ') # -- Gene[1] = relationship // Gene[2] = distance // Gene[4] = GeneSymbol // Gene[5] = GeneID
                if GeneDetail[5] != '---':
                    GeneSymbol = GeneDetail[4] 
                    GeneID = GeneDetail[5]
                    SnpRelationship = GeneDetail[1] 
                    GeneDistance = GeneDetail[2]
                    alsoknowas = dfNCBI.loc[dfNCBI['GeneID'] == int(GeneID)]['AlsoKnowAs'].iloc[0][2:-2]
                    if GeneSymbol in memory :
                        for i in listGeneInSNP:
                            changeDis = []
                            notsame = []
                            if i.GeneSymbol == GeneSymbol:
                                if i.relationship != SnpRelationship:
                                    notsame.append(eachrow_ProbeID)
                                    notsame.append(GeneSymbol)
                                    notsame.append(i.relationship)
                                    notsame.append(SnpRelationship)
                                    eventNotsame.append(notsame)
                                elif int(i.distance) > int(GeneDetail[2]):
                                    changeDis.append(eachrow_ProbeID)
                                    changeDis.append(GeneSymbol)
                                    changeDis.append(i.relationship)
                                    changeDis.append(i.distance)
                                    i.relationship = SnpRelationship
                                    i.distance = GeneDistance
                                    changeDis.append(i.relationship)
                                    changeDis.append(i.distance)
                                    eventchangedistance.append(changeDis)   
                    else :
                        memory.append(GeneDetail[4])
                        SNProw = SNP(eachrow_ProbeID, eachrow_SnpID, eachrow_Chromosome, SnpRelationship, GeneDistance, GeneSymbol, GeneID, alsoknowas)
                        listGeneInSNP.append(SNProw)
        for eachGene in listGeneInSNP:
            print(eachGene.ProbeSetID,eachGene.relationship,eachGene.distance ,eachGene.GeneSymbol, eachGene.NCBIGeneID)
            DataForExport.append(eachGene)

        df = pd.DataFrame([t.__dict__ for t in DataForExport])
        df.to_csv('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/GetDataOnWe/Dataset/Week2_Nsp_1.csv',index=False)
        dfeventchangedis = pd.DataFrame(eventchangedistance,columns=['ProbeSetID', 'GeneSymbol', 'relationship Before', 'distance Before', 'relationship After', 'distance After'])
        dfeventchangedis.to_csv('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/GetDataOnWe/Dataset/event_1_Nsp_1.csv',index=False)
        dfeventnotsame = pd.DataFrame(eventNotsame,columns=['ProbeSetID', 'GeneSymbol', 'relationship Before', 'relationship After'])
        dfeventnotsame.to_csv('/Users/parkin/Documents/Work/KMUTNB/NetAffx-Project/Project/Python/GetDataOnWe/Dataset/even_2_Nsp_1.csv',index=False)


