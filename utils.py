import csv
import models
from operator import attrgetter
import statistics


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
    # read file
    with open(filename) as file_raw:
        print(f'Opening file {filename}')
        data_raw = csv.reader(file_raw, delimiter=',')
        print('Iterating over each line in the file:')
        firstline = True
        columns = []
        for row in data_raw:
            if firstline:
                columns = row
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
            PropertyGFABuildings = int(
                row[columns.index('PropertyGFABuilding(s)')])
            PrimaryPropertyType = row[columns.index('PrimaryPropertyType')]
            LargestPropertyUseType = row[columns.index(
                'LargestPropertyUseType')]
            SecondLargestPropertyUseType = row[columns.index(
                'SecondLargestPropertyUseType')]
            ThirdLargestPropertyUseType = row[columns.index(
                'ThirdLargestPropertyUseType')]
            PropertyTypes = [
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
                PropertyTypes)

            list_of_buildings.append(building)

    print('Finish parsing file and filter data.')
    print(f'list_of_buildings length is {len(list_of_buildings)}')
    return list_of_buildings


def find_buildings_with_largest_number_of_floors(
        list_of_buildings, max_number_of_floors):
    list_of_buildings_with_largest_number_of_floors = []
    for building in list_of_buildings:
        if building.NumberofFloors == max_number_of_floors:
            list_of_buildings_with_largest_number_of_floors.append(building)
            continue
        if building.NumberofFloors > max_number_of_floors:
            max_number_of_floors = building.NumberofFloors
            list_of_buildings_with_largest_number_of_floors.clear()
            list_of_buildings_with_largest_number_of_floors.append(building)
            continue
    return list_of_buildings_with_largest_number_of_floors


def question_1(list_of_buildings):
    print('Solving question 1:')
    max_number_of_floors = 0
    list_of_buildings_with_largest_number_of_floors = find_buildings_with_largest_number_of_floors(
        list_of_buildings, max_number_of_floors)
    print('Building(s) with the largest number of floors:')
    for building in list_of_buildings_with_largest_number_of_floors:
        print(
            'Id {0}, name {1}, with {2} floors.'.format(
                building.OSEBuildingID,
                building.BuildingName,
                building.NumberofFloors))


def question_2(list_of_buildings):
    print('Solving question 2:')
    energy_star_score_threshold = 97
    nums_of_building_energy = sum(
        building.ENERGYSTARScore >= energy_star_score_threshold for building in list_of_buildings)
    print(
        'The number of buildings with ENERGYSTARScore of at least {0} is {1}.'.format(
            energy_star_score_threshold,
            nums_of_building_energy))


def filter_natural_gas(list_of_buildings):
    print('Filtering buildings that used natural gas:')
    list_of_buildings_used_naturalgas = []
    for building in list_of_buildings:
        if building.NaturalGas:
            list_of_buildings_used_naturalgas.append(building)
    return list_of_buildings_used_naturalgas


def question_3(list_of_buildings):
    print('Solving question 3:')
    list_of_buildings_used_naturalgas = filter_natural_gas(list_of_buildings)
    list_of_gas_used = []
    for building in list_of_buildings_used_naturalgas:
        list_of_gas_used.append(building.SiteEUI)
    median_SiteEUI = statistics.median(list_of_gas_used)

    print(
        f'The median of SiteEUI among buildings using natural gas is {median_SiteEUI} kBtu.')

    # list_of_gas_used.sort()
    # n = len(list_of_gas_used)
    # if n % 2 != 0:
    #     median_SiteEUI = list_of_gas_used[int(n / 2)]
    # else:
    #     median_SiteEUI = (list_of_gas_used[int(n / 2)] + list_of_gas_used[int(n / 2 - 1)]) / 2
    # print(
    #     f'The median of SiteEUI among buildings using natural gas is {median_SiteEUI}.')


def filter_neighborhood(list_of_buildings, neighborhood):
    # neighborhood = 'BALLARD'
    list_of_buildings_in_neighborhood = []
    for building in list_of_buildings:
        if building.Neighborhood == neighborhood:
            list_of_buildings_in_neighborhood.append(building)
    return list_of_buildings_in_neighborhood


def get_threshold_building(filename, threshold_building_name):
    with open(filename) as file_raw:
        data_raw = csv.reader(file_raw, delimiter=',')
        firstline = True
        columns = []
        for row in data_raw:
            if firstline:
                columns = row
                firstline = False
                continue

            if threshold_building_name in row:
                threshold_building_electricity = int(
                    row[columns.index('Electricity(kBtu)')])
                print('Building {0} used the amount of Electricity of {1} kBtu.'.format(
                    threshold_building_name, threshold_building_electricity))
                return threshold_building_electricity


def filter_electricity_use(list_of_buildings, threshold_building_electricity):
    list_of_building_used_more_electricity = []
    for building in list_of_buildings:
        if building.Electricity > threshold_building_electricity:
            list_of_building_used_more_electricity.append(building)
    return list_of_building_used_more_electricity


def question_4(filename, list_of_buildings):
    print('Solving question 4:')
    neighborhood = 'BALLARD'
    threshold_building_name = 'BIOMED FAIRVIEW RESEARCH CENTER'

    threshold_building_electricity = get_threshold_building(
        filename, threshold_building_name)
    list_of_buildings_in_neighborhood = filter_neighborhood(
        list_of_buildings, neighborhood)
    list_of_buildings_used_more_electricity = filter_electricity_use(
        list_of_buildings_in_neighborhood, threshold_building_electricity)

    for building in list_of_buildings_used_more_electricity:
        print(
            'Building id {0}, name {1} used the amount of Electricity of {2} kBtu.'.format(
                building.OSEBuildingID,
                building.BuildingName,
                building.Electricity))


def filter_property_type_block_list(list_of_buildings, block_list):
    print('Filtering buildings that are not offices or hospitals:')
    list_of_buildings_not_block_listed = []
    for building in list_of_buildings:
        chosen = True
        for property_type in building.PropertyTypes:
            if not chosen:
                continue
            for block_type in block_list:
                if block_type in property_type:
                    chosen = False
                    break
        if chosen:
            list_of_buildings_not_block_listed.append(building)
    return list_of_buildings_not_block_listed


def filter_property_floor_area_building(
        list_of_buildings, floor_area_threshold):
    list_of_large_buildings = []
    for building in list_of_buildings:
        if building.PropertyGFABuildings > floor_area_threshold:
            list_of_large_buildings.append(building)
    return list_of_large_buildings


def question_5(list_of_buildings):
    print('Solving question 5:')
    football_field_area = 57600  # square feet
    floor_area_threshold = 15 * football_field_area
    print(f'Threshold property area is {floor_area_threshold} square feet.')

    block_list = ['Hospital', 'Office']
    list_of_buildings_not_offices_or_hospitals = filter_property_type_block_list(
        list_of_buildings, block_list)

    list_of_large_buildings = filter_property_floor_area_building(
        list_of_buildings_not_offices_or_hospitals, floor_area_threshold)

    for building in list_of_large_buildings:
        print('Building id {0}, name {1}, total floor area for buildings {2} square feet.'.format(
            building.OSEBuildingID, building.BuildingName, building.PropertyGFABuildings
        ))


def ada_data_challenge(filename):
    list_of_buildings = parse_file(filename)
    question_1(list_of_buildings)
    question_2(list_of_buildings)
    question_3(list_of_buildings)
    question_4(filename, list_of_buildings)
    question_5(list_of_buildings)
