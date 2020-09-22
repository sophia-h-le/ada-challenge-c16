import csv
import models
from operator import attrgetter


def filter_data(columns, row):
    ENERGYSTARScore = row[columns.index('ENERGYSTARScore')]
    if ENERGYSTARScore == '':
        return False

    YearBuilt = row[columns.index('YearBuilt')]
    if int(YearBuilt) < 1920:
        return False

    BuildingName = row[columns.index('BuildingName')]
    if 'CENTER' in BuildingName:
        return False

    return True

def parse_file(filename):
    print('Starting parsing file:')
    list_of_buildings = []
    # Parsing file
    with open(filename) as file_raw:
        print(f'Opening file {filename}')
        data_raw = csv.reader(file_raw, delimiter=',')
        print('Iterating over each line in the file:')
        firstline = True
        columns = []
        for row in data_raw:
            if firstline:
                columns = row
                # print(columns)
                firstline = False
                continue
            # filter data
            if filter_data(columns, row) == False:
                continue

            OSEBuildingID = row[columns.index('OSEBuildingID')]
            # Question 1
            BuildingName = row[columns.index('BuildingName')]
            NumberofFloors = int(row[columns.index('NumberofFloors')])
            # Question 2
            ENERGYSTARScore = int(row[columns.index('ENERGYSTARScore')])
            SiteEUI = float(row[columns.index('SiteEUI(kBtu/sf)')])
            NaturalGas = row[columns.index('NaturalGas(kBtu)')]
            # Question 3
            Neighborhood = row[columns.index('Neighborhood')]
            Electricity = int(row[columns.index('Electricity(kBtu)')])
            # Question 4
            PropertyGFABuildings = int(row[columns.index('PropertyGFABuilding(s)')])
            PrimaryPropertyType = row[columns.index('PrimaryPropertyType')]
            LargestPropertyUseType = row[columns.index(
                'LargestPropertyUseType')]
            SecondLargestPropertyUseType = row[columns.index(
                'SecondLargestPropertyUseType')]
            ThirdLargestPropertyUseType = row[columns.index(
                'ThirdLargestPropertyUseType')]
            PropertyType = [
                PrimaryPropertyType,
                LargestPropertyUseType,
                SecondLargestPropertyUseType,
                ThirdLargestPropertyUseType]

            # instance a Building
            building = models.Building(
                OSEBuildingID,
                BuildingName,
                NumberofFloors,
                ENERGYSTARScore,
                SiteEUI,
                NaturalGas,
                Neighborhood,
                Electricity,
                PropertyGFABuildings,
                PropertyType)
            
            list_of_buildings.append(building)

    print('Finish parsing file and filter data.')
    print(f'list_of_buildings length is {len(list_of_buildings)}')
    return list_of_buildings

def question_1(list_of_buildings):
    print('Solving question 1:')
    building_with_largest_NumberofFloors = max(
        list_of_buildings, key=attrgetter('NumberofFloors'))
    print(building_with_largest_NumberofFloors.OSEBuildingID)
    print(
        'The building with the largest number of floors is {0} with {1} floors.'.format(
            building_with_largest_NumberofFloors.BuildingName,
            building_with_largest_NumberofFloors.NumberofFloors))

def question_2(list_of_buildings):
    print('Solving question 2:')
    threshold = 97
    # sum(i > 5 for i in j)
    nums_of_building_energy = sum(building.ENERGYSTARScore >= threshold for building in list_of_buildings)
    print('The number of buildings with ENERGYSTARScore of at least {0} is {1}.'.format(
        threshold, nums_of_building_energy))

def filter_natural_gas(list_of_buildings):
    print('Filtering buildings that used natural gas:')
    list_of_buildings_used_naturalgas = []
    for building in list_of_buildings:
        if building.NaturalGas != False:
            list_of_buildings_used_naturalgas.append(building)
    return list_of_buildings_used_naturalgas

def get_median_SiteEUI(list_of_buildings_used_naturalgas):
    length = len(list_of_buildings_used_naturalgas)
    median_SiteEUI = (list_of_buildings_used_naturalgas[int(length / 2)].SiteEUI + list_of_buildings_used_naturalgas[int((length / 2) + 1/2)].SiteEUI) / 2
    return median_SiteEUI

def question_3(list_of_buildings):
    print('Solving question 3:')
    list_of_buildings_used_naturalgas = filter_natural_gas(list_of_buildings)
    list_of_buildings_used_naturalgas.sort(key = attrgetter('SiteEUI'))
    median_SiteEUI = get_median_SiteEUI(list_of_buildings_used_naturalgas)
    print(f'The median of SiteEUI among buildings using natural gas is {median_SiteEUI}.')

def filter_neighborhood(list_of_buildings):
    neighborhood = 'BALLARD'
    list_of_buildings_in_neighborhood = []
    for building in list_of_buildings:
        if building.Neighborhood == neighborhood:
            list_of_buildings_in_neighborhood.append(building)
    return list_of_buildings_in_neighborhood

def get_threshold_building(filename):
    #TODO: refactor
    threshold_building_name = 'BIOMED FAIRVIEW RESEARCH CENTER'
    with open(filename) as file_raw:
        data_raw = csv.reader(file_raw, delimiter=',')
        firstline = True
        columns = []
        for row in data_raw:
            if firstline:
                columns = row
                # print(columns)
                firstline = False
                continue

            if threshold_building_name in row:
                threshold_building_electricity = int(row[columns.index('Electricity(kBtu)')])
                print('Building {0} used the amount of Electricity of {1} kBtu.'.format(
                    threshold_building_name, threshold_building_electricity))
                return threshold_building_electricity

def question_4(filename, list_of_buildings):
    print('Solving question 4:')
    threshold_building_electricity = get_threshold_building(filename)
    list_of_buildings_in_neighborhood = filter_neighborhood(list_of_buildings)
    for building in list_of_buildings_in_neighborhood:
        if building.Electricity > threshold_building_electricity:
            print('Building {0} used the amount of Electricity of {1} kBtu.'.format(
                building.BuildingName, building.Electricity
            ))

def filter_property_type_block_list(list_of_buildings, block_list):
    print('Filtering buildings that are not offices or hospitals:')
    list_of_buildings_not_offices_or_hospitals = []
    for building in list_of_buildings:
        chosen = True
        for property_type in building.PropertyType:
            if not chosen:
                continue
            for block_type in block_list:
                if block_type in property_type:
                    chosen = False
                    break
        if chosen:
            list_of_buildings_not_offices_or_hospitals.append(building)
    return list_of_buildings_not_offices_or_hospitals

def question_5(list_of_buildings):
    print('Solving question 5:')
    football_field_area = 57600 #square feet
    threshold_property_area = 15 * football_field_area
    print(f'Threshold property area is {threshold_property_area} square feet.')
    list_of_large_buildings = []
    block_list = ['Hospital', 'Office']
    list_of_buildings_not_offices_or_hospitals = filter_property_type_block_list(list_of_buildings, block_list)
    
    for building in list_of_buildings_not_offices_or_hospitals:
        if building.PropertyGFABuildings > threshold_property_area:
            list_of_large_buildings.append(building)

    for building in list_of_large_buildings:
        print('Building with ID {0}, name {1}, total floor area {2} square feet.'.format(
            building.OSEBuildingID, building.BuildingName, building.PropertyGFABuildings
        ))

def ada_data_challenge(filename):
    list_of_buildings = parse_file(filename)
    question_1(list_of_buildings)
    question_2(list_of_buildings)
    question_3(list_of_buildings)
    question_4(filename, list_of_buildings)
    question_5(list_of_buildings)