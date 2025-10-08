
import  traci
import logging
import pandas as pd

from sumolib import checkBinary


sumoBinary = checkBinary('sumo-gui')

edge_id=['2460','2461','-2460','-2461']

def main():
        i=1
        startSim()
        while shouldContinueSim():


        # avoidEdge(edge_id)

         traci.simulationStep()
        traci.close()


def GetRoute(i):
    if i%10==0:
      print(f"当前时间第{i}秒")
      for vehicle_id in traci.vehicle.getIDList():
        print("车辆" + f"{vehicle_id}" + "的路径为" + str(traci.vehicle.getRoute(vehicle_id)))
      print("-----------------------------------------------------------------------")

def SetRoute(i):
    if i == 35:
        for j in range(1, 7):
            traci.vehicle.setRoute(f'trip_{j}', new_route1)
    if i == 80:
        for j in range(3, 6):
            traci.vehicle.setRoute(f'trip_{j}', new_route2)

def find_invalid_routes():
    invalid_routes = {}
    invalid_veh_ids = []
    for i in range(1, 9698):

      veh_id=f"trip_{i}"

      route = traci.vehicle.getRoute(veh_id)
      if len(route) > 1:
          # 使用列表推导式获取相邻值的元组列表
          adjacent_pairs = [(route[j], route[j + 1]) for j in range(len(route) - 1)]
          for pair in  adjacent_pairs :
              if len(traci.simulation.findRoute(pair[0], pair[1]).edges) == 0:
                  invalid_routes[veh_id] = route
                  invalid_veh_ids.append(veh_id)
                  break
    for veh_id in invalid_veh_ids:
        print(f"Vehicle with invalid route: {veh_id}")






def startSim():

    traci.start(
        [
            sumoBinary,

            '--net-file', './config/map.net.xml', 
            '--route-files', './config/test.xml',
            '--delay', '200',
            '--gui-settings-file', './config/viewSettings.xml',
            '--tripinfo-output','./config/tripinfo_4.xml',
            '--fcd-output','./config/fcd.xml',
            '--vehroute-output','./config/vehroute.xml',
            '--netstate-dump','./config/dump.xml',





                           
            '--ignore-route-errors',
            '--log', 'logfile1.log',







            '--start'
        ])
def avoidEdge( edgesId):

    """Sets an edge's travel time for a vehicle infinitely high, and reroutes the vehicle based on travel time.
    Args:
        vehId (Str): The ID of the vehicle to reroute.
        edgeId (Str): The ID of the edge to avoid.
    """
    for vehId in  traci.vehicle.getIDList():
        for edgeId in edgesId:
          if   traci.vehicle.getRoadID(vehId)!= str(edgesId)[2:-2]:
            traci.vehicle.setAdaptedTraveltime(
            vehId, edgeId, float('inf'))
            traci.vehicle.rerouteTraveltime(vehId)
def getOurDeparted(filterIds=[]):
    """Returns a set of filtered vehicle IDs that departed onto the network during this simulation step.
    Args:
        filterIds ([String]): The set of vehicle IDs to filter for.
    Returns:
        [String]: A set of vehicle IDs.
    """
    newlyDepartedIds = traci.simulation.getDepartedIDList()
    filteredDepartedIds = newlyDepartedIds if len(
        filterIds) == 0 else set(newlyDepartedIds).intersection(filterIds)
    return filteredDepartedIds
def setVehColor(vehId, color):
    """Changes a vehicle's color.
    Args:
        vehId (String): The vehicle to color.
        color ([Int, Int, Int]): The RGB color to apply.
    """
    traci.vehicle.setColor(vehId, color)

def shouldContinueSim():
    """Checks that the simulation should continue running.
    Returns:
        bool: `True` if there are any vehicles on or waiting to enter the network. `False` otherwise.
    """
    numVehicles = traci.simulation.getMinExpectedNumber()
    return True if numVehicles > 0 else False

if __name__ == "__main__":
    main()
