def getWarmingFunctions(statesFullObj, requestingFunctionName):
    states = statesFullObj["States"]
    if requestingFunctionName in states:
        requestingFunctionData = states[requestingFunctionName]
        if 'End' in requestingFunctionData and requestingFunctionData['End']==True :
            return "%=END=%"
        
        elif requestingFunctionData['Type'] == 'Choice':
            warmingFunctions = [state['Next'] for state in requestingFunctionData['Choices']]
            if 'Default' in requestingFunctionData:
                warmingFunctions.append(requestingFunctionData['Default'])
            return warmingFunctions
        elif requestingFunctionData['Type'] == 'Parallel':
            warmingFunctions = [branch['StartAt'] for branch in requestingFunctionData['Branches']]
            return warmingFunctions
        else:
            return requestingFunctionData['Next']
    else:
        parallelTypes = [states[stateName] for stateName in states if states[stateName]['Type']== 'Parallel']
        warmingFunctions = []

        for parallelType in parallelTypes:
            branches = [branch for branch in parallelType['Branches']]
            branchFunctions = [getWarmingFunctions(branch, requestingFunctionName) for branch in branches]
            if '%=END=%' in branchFunctions and 'Next' in parallelType:
                branchFunctions.append(parallelType['Next'])
            # branchFunctions = [branchFunction for branchFunction in branchFunctions if branchFunction != None if len(branchFunction)>0]
            [warmingFunctions.append(bf) for bf in branchFunctions if bf != None and  len(bf) > 0]
        return warmingFunctions