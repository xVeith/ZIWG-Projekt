from django.shortcuts import render
from django.http import HttpResponse
from .models import Combinations
from .models import Enchants
from .models import Items
from .models import Conflicts
import copy
allCombinations = Combinations.objects.all()
allEnchants = Enchants.objects.all()
allItems = Items.objects.all()
allConflicts = Conflicts.objects.all()
bestResults = []


def index(request):
    return HttpResponse("Hello, world. You're at the main  page.")


def main_page(request):
    context = {'Combinations': allCombinations,
               'Enchants': allEnchants,
               'Items': allItems}
    return render(request, 'main_page.html', context)


def form_page(request):
    chosenItem = request.POST['chosenItem']

    count = 0
    ownedType1Count = request.POST['ownedType1Count']
    ownedType2Count = request.POST['ownedType2Count']
    ownedType3Count = request.POST['ownedType3Count']
    ownedType4Count = request.POST['ownedType4Count']
    ownedType5Count = request.POST['ownedType5Count']
    ownedType6Count = request.POST['ownedType6Count']
    ownedType7Count = request.POST['ownedType7Count']
    ownedType8Count = request.POST['ownedType8Count']
    ownedType9Count = request.POST['ownedType9Count']
    ownedType10Count = request.POST['ownedType10Count']
    count += int(ownedType1Count)
    count += int(ownedType2Count)
    count += int(ownedType3Count)
    count += int(ownedType4Count)
    count += int(ownedType5Count)
    count += int(ownedType6Count)
    count += int(ownedType7Count)
    count += int(ownedType8Count)
    count += int(ownedType9Count)
    count += int(ownedType10Count)

    if(count > 10):
        registration_successful = 1
        wrong = 1
        context = {'Combinations': allCombinations,
                   'Enchants': allEnchants, 'Items': allItems, 'wrong': wrong, 'registration_successful' : registration_successful}
        return render(request, 'main_page.html', context)

    owned_items = []
    if (int(ownedType1Count) > 0):
        ownedItemType1 = request.POST['ownedItemType1']
        owned_items.append([ownedItemType1, ownedType1Count])
    if (int(ownedType2Count) > 0):
        ownedItemType2 = request.POST['ownedItemType2']
        owned_items.append([ownedItemType2, ownedType2Count])
    if (int(ownedType3Count) > 0):
        ownedItemType3 = request.POST['ownedItemType3']
        owned_items.append([ownedItemType3, ownedType3Count])
    if (int(ownedType4Count) > 0):
        ownedItemType4 = request.POST['ownedItemType4']
        owned_items.append([ownedItemType4, ownedType4Count])
    if (int(ownedType5Count) > 0):
        ownedItemType5 = request.POST['ownedItemType5']
        owned_items.append([ownedItemType5, ownedType5Count])
    if (int(ownedType6Count) > 0):
        ownedItemType6 = request.POST['ownedItemType6']
        owned_items.append([ownedItemType6, ownedType6Count])
    if (int(ownedType7Count) > 0):
        ownedItemType7 = request.POST['ownedItemType7']
        owned_items.append([ownedItemType7, ownedType7Count])
    if (int(ownedType8Count) > 0):
        ownedItemType8 = request.POST['ownedItemType8']
        owned_items.append([ownedItemType8, ownedType8Count])
    if (int(ownedType9Count) > 0):
        ownedItemType9 = request.POST['ownedItemType9']
        owned_items.append([ownedItemType9, ownedType9Count])
    if (int(ownedType10Count) > 0):
        ownedItemType10 = request.POST['ownedItemType10']
        owned_items.append([ownedItemType10, ownedType10Count])

    is_even_possible = 0
    for i in range(len(owned_items)):
        if (chosenItem == owned_items[i][0]):
            is_even_possible = 1
            break

    if (is_even_possible == 0):
        wrong = 2
        registration_successful = 2 
        context = {'Combinations': allCombinations,
                   'Enchants': allEnchants, 
                   'Items': allItems, 
                   'wrong': wrong,
                   'registration_successful' : registration_successful }
        return render(request, 'main_page.html', context)

    needed_items = []
    for i in range(len(owned_items)):
        if (chosenItem == owned_items[i][0] and chosenItem != 'Book'):
            needed_items.append(owned_items[i])
        if (owned_items[i][0] == 'Book'):
            needed_items.append(owned_items[i])

    possible_enchants = []
    for i in range(len(needed_items)):
        for j in range(int(needed_items[i][1])):
            compatible_enchants = findCompatibleEnchants(
                needed_items[i][0], allCombinations, allEnchants)
            item = Item(needed_items[i][0], compatible_enchants)
            possible_enchants.append(item)

    context = {'chosenItem': chosenItem,
               'owned_items': owned_items,
               'possible_enchants': possible_enchants
               }
    return render(request, 'form_page.html', context)


def calculating(request):
    itemCount = request.POST['itemCount']
    itemType = request.POST['itemName']
    usersItems = []
    for i in range(int(itemCount)):
        enchants = []
        enchant1 = request.POST[str(i+1)+'ownedEnchant1']
        if (enchant1 != '-------------'):
            enchants.append(Enchant(enchant1[0:-2], int(enchant1[-1:])))
        enchant2 = request.POST[str(i+1)+'ownedEnchant2']
        if (enchant2 != '-------------'):
            enchants.append(Enchant(enchant2[0:-2], int(enchant2[-1:])))
        enchant3 = request.POST[str(i+1)+'ownedEnchant3']
        if (enchant3 != '-------------'):
            enchants.append(Enchant(enchant3[0:-2], int(enchant3[-1:])))
        usersItems.append(Item(request.POST[str(i+1)+'item'], enchants))

    selectedItems = []

    for item in usersItems:
        check = 0
        for enchant in item.enchants:
            if (check > 0):
                break
            for combination in allCombinations:
                if (itemType == combination.item_name.name and enchant.name == combination.enchant_name.name):
                    selectedItems.append(item)
                    check = check+1
                    break
    # ------------------ 3. Making all combinations that are possible to get in survival Minecraft --------------------------------
    limitedItems = []
    bestResults.clear()
    for item in selectedItems:
        if (item.name == itemType):					# musimy zaczac od takiego itemka, jaki chcemy miec finalny wynik
            # tworzymy obiekt baseItem jako itemek bazowy, do ktorego bedziemy dodawac
            baseItem = copy.deepcopy(item)
            index = selectedItems.index(item)
            limitedItems = selectedItems[:index] + selectedItems[index+1:]
            # zeby nie przeszukiwac wszystkich razem z tym przed chwila wybranym
            path = []
            if (len(limitedItems) > 0):
                depth = 0
                path.append(item)
                combine(Recursive(depth, limitedItems, baseItem, path))

    selectedResults = present()
    context = {'bestResults': selectedResults}
    return render(request, 'result_page.html', context)


def findCompatibleEnchants(item_name, allCombinations, allEnchants):
    compatible_enchants = []
    for c in allCombinations:
        if c.item_name.name == item_name:
            for e in allEnchants:
                if c.enchant_name.name == e.name:
                    for j in range(1, 6):
                        if j <= e.max_level:
                            ench = Enchant(e.name, j)
                            compatible_enchants.append(ench)
    return compatible_enchants


class Enchant:
    def __init__(self, name, level):
        self.name = name
        self.level = level


class Item:
    def __init__(self, name, enchants):
        self.name = name
        self.enchants = enchants


class Result:
    def __init__(self, Item, score, path):
        self.Item = Item
        self.score = score
        self.path = path


class Recursive:
    def __init__(self, depth, limitedItems, baseItem, path):
        self.depth = depth
        self.limitedItems = limitedItems
        self.baseItem = baseItem
        self.path = path


def combine(recursive):
    if (recursive.depth < 6):
        for item in recursive.limitedItems:
            if ( recursive.depth == 0 ):
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            baseItemNew = copy.deepcopy(recursive.baseItem)
            check3 = 0
            for enchant in item.enchants:
                for combination in allCombinations:
                    # jezeli enchant moze zostac dodany do przedmiotu
                    if (recursive.baseItem.name == combination.item_name.name and enchant.name == combination.enchant_name.name):
                        check = 0
                        for enchantB in baseItemNew.enchants:
                            # ZWIEKSZENIE POZIOMU ENCHANTU jezeli taki enchant juz jest na przedmiocie
                            if (enchantB.name == enchant.name):
                                check = check+1
                                if (enchantB.level > enchant.level):
                                    break
                                elif (enchant.level > enchantB.level):
                                    check3 = check3 + 1
                                    enchantB.level = enchant.level
                                    break
                                else:
                                    for enchantAll in allEnchants:
                                        if (enchantB.name == enchantAll.name and enchantAll.max_level > enchantB.level):
                                            check3 = check3 + 1
                                            enchantB.level = enchantB.level+1
                                            break
                            else:  # JEZELI KOLIDUJE Z JAKIMS ENCHANTEM NA PRZEDMIOCIE NP. MENDING Z INFINITY
                                check1 = -1
                                check2 = -2
                                for conflict in allConflicts:
                                    if (enchant.name == conflict.enchant_name.name):
                                        check1 = conflict.conflict_group
                                    elif (enchantB.name == conflict.enchant_name.name):
                                        check2 = conflict.conflict_group
                                    if (check1 == check2):
                                        check = check+1
                                        break
                        if (check == 0):
                            # bo ani nie znalazlo takiego enchantu na przedmiocie bazowym, ani nie znalazlo na nim zadnego kolidujacego enchantu
                            check3 = check3 + 1
                            baseItemNew.enchants.append(enchant)
                        break
# ------------------ 4. Evaluating the value of every created combination --------------------------------
            score = 0
            for enchant in baseItemNew.enchants:
                for combination in allCombinations:
                    if (baseItemNew.name == combination.item_name.name and enchant.name == combination.enchant_name.name):
                        score += combination.rating * enchant.level
            if ( score > 10 ):
                print(score)
            pathNew = copy.deepcopy(recursive.path)
            if ( check3 > 0 ):
                pathNew.append(item)
            bestResults.append(Result(baseItemNew, score, pathNew))
            index = recursive.limitedItems.index(item)

            limitedItemNew = recursive.limitedItems[:index] + recursive.limitedItems[index+1:]
            depthNew = copy.deepcopy(recursive.depth)
            if ( len(limitedItemNew) > 0 ):
                combine(Recursive(depthNew+1, limitedItemNew, baseItemNew, pathNew))


# 5. Presenting 3 combinations that scored the highest to the user​
def present():
    selectedResults = []
    bestResultsSorted = sorted(bestResults, key=lambda x: x.score, reverse=True)
    for bestResult in bestResultsSorted:
        if not selectedResults:        # jezeli lista jest pusta
            selectedResults.append(bestResult)
        else:                        # jezeli nie jest pusta
            enchantsList = []
            for enchant in bestResult.Item.enchants:
                enchantsList.append(enchant.name)        # tworzymy liste nazw enchantow na potencjalnym przedmiocie wynikowym do dodania
            check = 0
            for selectedResult in selectedResults:
                enchantsListSelected = []
                for enchant in selectedResult.Item.enchants:
                    enchantsListSelected.append(enchant.name)
                if ( sorted(enchantsList) == sorted(enchantsListSelected) ):    # jezeli nowy item zawiera takie same enchanty (sprawdzamy nazwy enchantow) w obojetnej kolejnosci
                    check = check +1
            if ( check == 0 and len(selectedResults) < 3 ):
                selectedResults.append(bestResult)
            elif ( check == 0 ):
                lowest = selectedResults[0]
                for selectedResult in selectedResults:
                    if ( selectedResult.score < lowest.score ):
                        lowest = selectedResult
                if ( bestResult.score > lowest.score ):
                    selectedResults.remove(lowest)
                    selectedResults.append(bestResult)
    selectedResultsSorted = sorted(selectedResults, key=lambda x: x.score, reverse=True)
    return selectedResultsSorted
