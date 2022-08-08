def getWarmingFunctions(stateFullObj, functionName):
    # if functionName is not the start function, we do not need to check the workflow for warming functions,
    # because we are sure warming functions are checked before
    if stateFullObj['StartAt'] != functionName:
        return []
    else:
        return getAllWarmingFunctions(stateFullObj, functionName)


def getAllWarmingFunctions(stateFullObj):
    states = stateFullObj["States"]
    warmingFunctions = [stateFullObj['StartAt']]

    for ـ, state in states.items():
        if state['Type'] == 'Choice':
            for choice in state['Choices']:
                warmingFunctions.append(choice['Next'])

            if 'Default' in state:
                warmingFunctions.append(state['Default'])

        if state['Type'] == 'Parallel':
            warmingFunctions.append(state['Next'])

            for branch in state['Branches']:
                branchWarmingFunctions = getAllWarmingFunctions(branch)
                warmingFunctions.extend(branchWarmingFunctions)

        if 'Next' in state and state["Next"] != '':
            warmingFunctions.append(state['Next'])

    return list(set(warmingFunctions))
