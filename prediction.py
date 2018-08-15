# implementing random forest from scratch
import pandas as pd

# data preprocessing
train_data= pd.read_csv('training.csv')
clean= train_data.dropna(subset=["MMRCurrentRetailAveragePrice", \
"MMRAcquisitionRetailAveragePrice", "MMRCurrentAuctionAveragePrice", \
"MMRAcquisitionAuctionAveragePrice"])
clean= clean[["VehBCost", "MMRCurrentRetailAveragePrice", \
"MMRAcquisitionRetailAveragePrice", "VehOdo", "VehicleAge", "IsBadBuy", \
"MMRAcquisitionAuctionAveragePrice", "MMRCurrentAuctionAveragePrice"]]
clean.reset_index(inplace=True)
featuresL= list(clean)
featuresL = [f for f in featuresL if f not in ('IsBadBuy', 'index')]

#calculate Gini inpurity- basis for splits
def featureGini(featureName, df, outputName):
    totalCount= len(df)
    splitPoint= df[featureName].median()
    leftObs= len(df[df[featureName] <= splitPoint])
    rightObs= len(df[df[featureName] > splitPoint])
    leftPos= len(df[(df[featureName] <= splitPoint) & (df[outputName]==1)])
    rightPos= len(df[(df[featureName] > splitPoint) & (df[outputName]==1)])
    leftNeg= len(df[(df[featureName] <= splitPoint) & (df[outputName]==0)])
    rightNeg= len(df[(df[featureName] > splitPoint) & (df[outputName]==0)])
    if leftObs==0:
        leftProp=0
    else:
        leftProp= 1-((leftPos/leftObs)**2 + (leftNeg/leftObs)**2)
    if rightObs==0:
        rightProp=0
    else:
        rightProp= 1-((rightPos/rightObs)**2 + (rightNeg/rightObs)**2)
    leftGini= leftProp * (leftObs/totalCount)
    rightGini= rightProp * (rightObs/totalCount)
    return leftGini + rightGini

# return min Gini value
def findMinGini(parentDf, features, outputName):
    minGini= []
    for i in features:
        gScore= featureGini(i, parentDf, outputName)
        minGini.append(gScore)
    minScore= min(minGini)
    minInx= minGini.index(minScore)
    bestFeature= features[minInx]
    return minScore, bestFeature

# recursive splitting the datasets
def splittingData(parentDf, features, outputName, prevGini=1, depth=0, treeLst= None, fromDirection=None):
    if treeLst==None:
        treeLst=[[depth, fromDirection, None, None]]
    bestGini, bestFeature= findMinGini(parentDf, features, outputName)
    splitPt= parentDf[bestFeature].median()
    if prevGini-bestGini < 0.01:
        return [[depth, fromDirection, bestFeature, splitPt]]
    else:
        left= parentDf[parentDf[bestFeature] <= splitPt]
        right= parentDf[parentDf[bestFeature] > splitPt]
        return splittingData(left, features, outputName, bestGini, depth+1, treeLst, 'L') + \
        splittingData(right, features, outputName, bestGini, depth+1, treeLst, 'R')

# random forest implementation
def forest(df, features, outputName):
    tree1= splittingData(df.sample(frac=0.25), features, outputName)
    tree2= splittingData(df.sample(frac=0.25), features, outputName)
    tree3= splittingData(df.sample(frac=0.25), features, outputName)
    tree4= splittingData(df.sample(frac=0.25), features, outputName)
    return [tree1, tree2, tree3, tree4]

# ouput each tree's prediction
# multiplier for weighing decisions since data unbalanced with that ratio
def predict(df, treeL, featureDict, outputName, multiplier= 0.15):
    treeL.sort()
    goDirection= None
    slicedf= None
    for i in treeL:
        splitDirection, feature, splitVal= i[1], i[2], i[3]
        if featureDict[feature] <= splitVal:
            goDirection= 'L'
            splicedf= df[df[feature] <= splitVal]
        else:
            goDirection='R'
            splicedf= df[df[feature] > splitVal]
        if goDirection != splitDirection:
            break
    valLst= list(splicedf[outputName])
    zeros= int(valLst.count(0)*multiplier)
    ones= valLst.count(1)
    if zeros > ones:
        return 0
    else:
        return 1

# return the majority vote from all trees
def returnPreds(featureDict, df=clean, outputName= 'IsBadBuy', multiplier=0.15):
    models= forest(clean, featuresL, outputName)
    finalLst= []
    for i in models:
        finalLst.append(predict(df, i, featureDict, outputName, multiplier))
    return max(set(finalLst), key=finalLst.count)
