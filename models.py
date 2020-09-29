class Building(object):
    def __init__(
            self,
            OSEBuildingID,
            BuildingName,
            NumberofFloors,
            ENERGYSTARScore,
            SiteEUI,
            NaturalGas,
            Neighborhood,
            Electricity,
            PropertyGFABuildings,
            PropertyTypes):
        self.OSEBuildingID = OSEBuildingID
        self.BuildingName = BuildingName
        self.NumberofFloors = NumberofFloors
        self.ENERGYSTARScore = ENERGYSTARScore
        self.SiteEUI = SiteEUI
        self.NaturalGas = NaturalGas
        self.Neighborhood = Neighborhood
        self.Electricity = Electricity
        self.PropertyGFABuildings = PropertyGFABuildings
        self.PropertyTypes = PropertyTypes
