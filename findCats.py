#!/usr/bin/python

import sys
import argparse
import json
from random import sample
from collections import OrderedDict

class Cat(object):

  def __init__(self, tag):
    self.tag=tag
    self.moves = 0
    self.location = None
    self.stationsVisited = set()
    self.reunited = False

  def getMoves(self):
    return self.moves

  def setLocation(self, location):
    self.location = location

  def getLocation(self):
    return self.location

  def getTag(self):
    return self.tag

  def isReunited(self):
    return self.reunited

  def reunite(self):
    self.reunited = True

  def move(self, availableLocations):
    oldLocation=self.location
    if(len(availableLocations)>0):
      location = sample(availableLocations,1)
      self.location = location[0]
    self.stationsVisited.add(self.location)
    self.moves+=1
    if(debug): print "Cat %i moved from %i to %i" % (self.tag, oldLocation, self.location)
    return [oldLocation, self.location]

class Owner(object):

  def __init__(self, tag):
    self.moves = 0
    self.catTag = tag
    self.stationsVisited = set()
    self.location = None
    self.reunited = False

  def getCatTag(self):
    return self.catTag

  def getMoves(self):
    return self.moves

  def setLocation(self, location):
    self.location = location

  def getLocation(self):
    return self.location

  def isReunited(self):
    return self.reunited

  def reunite(self):
    self.reunited = True

  def move(self, availableLocations):
    # Discounts stations we visited before ########################
    preferredLocations = availableLocations-self.stationsVisited
    if(len(preferredLocations)>0):
      availableLocations = preferredLocations
    ###############################################################
    oldLocation=self.location
    if(len(availableLocations)>0):
      location = sample(availableLocations,1)
      self.location = location[0]
    self.stationsVisited.add(self.location)
    self.moves+=1
    if(debug): print "Owner %i moved from %i to %i" % (self.catTag, oldLocation, self.location)
    return [oldLocation, self.location]

class Station(object):

  def __init__(self, stationId, stationName = "Unnamed"):
    self.state = "open"
    self.id = stationId
    self.name = stationName
    self.connections = set()
    self.catsInStation = set()
    self.catsSeen = set()
    self.ownersInStation = set()
    self.ownersSeen = set()
    self.trafficCount = 0
    self.maxTrafficCount = 0

  def getId(self):
    return self.id

  def addConnection(self, connection):
    self.connections.add(connection)

  def removeConnection(self, connection):
    self.connections.discard(connection)

  def getConnections(self):
    return self.connections

  def catArrived(self, catTag):
    self.trafficCount+=1
    self.catsSeen.add(catTag)
    self.catsInStation.add(catTag)

  def catDeparted(self, catTag):
    self.catsInStation.discard(catTag)

  def ownerArrived(self, ownerId):
    self.trafficCount+=1
    self.ownersSeen.add(ownerId)
    self.ownersInStation.add(ownerId)
    if(len(self.ownersInStation)+len(self.catsInStation)>self.maxTrafficCount): self.maxTrafficCount=len(self.ownersInStation)+len(self.catsInStation)

  def ownerDeparted(self, ownerId):
    self.ownersInStation.discard(ownerId)

  def getCatsSeen(self):
    return self.catsSeen

  def getOwnersSeen(self):
    return self.ownersSeen

  def getTrafficCount(self):
    return self.trafficCount

  def getCatsInStation(self):
    return self.catsInStation

  def getOwnersInStation(self):
    return self.ownersInStation

  def getMaxTrafficCount(self):
    return self.maxTrafficCount

  def checkForLove(self):
    return self.ownersInStation & self.catsInStation

  def checkForLoveAllTime(self):
    return self.ownersSeen & self.catsSeen

  def close(self):
    self.state = "closed"

  def preClose(self):
    self.state = "closing"

  def open(self):
    self.state = "open"

  def printAll(self):
    print "ID: %s\t\tName: %-*s\tState: %s\tConnections: %s" % (self.id, 30, self.name, self.state, " ".join(str(e) for e in self.connections))

  def getName(self):
    return self.name

  def setName(self, name):
    self.name = name

  def getState(self):
    return self.state


class TFL(object):
  def __init__(self):
    self.stations =  OrderedDict()

  def getAllStations(self, state = "any"):
    if(state == "open"):
      tmp = OrderedDict()
      for key, station in self.stations.iteritems():
        if(station.getState() == "open"):
          tmp[station.getId()] = station
      return tmp
    elif(state == "any"):
      return self.stations

  def getAllTimeMatches(self):
    allMatches = set()
    for key, station in self.stations.iteritems():
      allMatches = allMatches | station.checkForLoveAllTime()
    return allMatches

  def getTotalTrafficCount(self):
    totals=0
    for key, station in self.stations.iteritems():
      totals+=station.getTrafficCount()
    return totals

  def getMaxConcurrentTrafficStation(self):
    max = 0
    stationName = ""
    for key, station in self.stations.iteritems():
      if(station.getMaxTrafficCount() > max): 
        max = station.getMaxTrafficCount()
        stationName = station.getName()
    return [stationName, max] 

  def getMaxTrafficStation(self):
    max=0
    stationName = ""
    for key, station in self.stations.iteritems():
      if(station.getTrafficCount() > max):
        max = station.getTrafficCount()
        stationName = station.getName()
    return [stationName, max]

  def buildStations(self, design, names):
    try:
      with open(design) as json_design:
        try:
          json_connections = json.load(json_design)
          for station in json_connections:
            if int(station[0]) in self.stations: #if station exists - add connection, else create station.
              self.stations[int(station[0])].addConnection(int(station[1]))
            else:
              self.stations[int(station[0])] = Station(int(station[0]))
              self.stations[int(station[0])].addConnection(int(station[1]))
            if int(station[1]) in self.stations: #same as above for connecting station.
              self.stations[int(station[1])].addConnection(int(station[0]))
            else:
              self.stations[int(station[1])] = Station(int(station[1]))
              self.stations[int(station[1])].addConnection(int(station[0]))
        except ValueError:
          print "Failed to Parse JSON"
          exit(1)
    except (OSError, IOError):
      print "Failed to read TFL design file"
      exit(1)
    with open(names) as json_names:
      json_nn = json.load(json_names)
      for station in json_nn: #Give names to all stations that are present in json file.
        self.stations[int(station[0])].setName(station[1])

  def closeStation(self, closingStation):
    if(self.stations[closingStation].getState() == "open"):
      self.stations[closingStation].close()
      if(debug): print "Closing station %s - ID %i" % (self.stations[closingStation].getName(), closingStation)
      for id, station in self.stations.iteritems():
        if(closingStation in station.getConnections()):
          if(debug): print "Removing connection from %s to %i" % (id, closingStation)
          station.removeConnection(closingStation)

  def printAllStations(self):
    for id, station in self.stations.iteritems():
      station.printAll()

def seed(n, stations):
  for i in range(n): # For each pair of cat and owner
    locations = sample(range(len(stations)),2)
    cats[i] = Cat(i)
    cats[i].setLocation(stations.keys()[locations[0]])
    owners[i] = Owner(i)
    owners[i].setLocation(stations.keys()[locations[1]])

def tryMoveCats():
  for key, cat in cats.iteritems():
    if(not cat.isReunited()):
      catPositions = cat.move(network.getAllStations()[cat.getLocation()].getConnections())  # Move and get current, previous locations
      network.getAllStations()[catPositions[0]].catDeparted(cat.getTag())  # Update station records
      network.getAllStations()[catPositions[1]].catArrived(cat.getTag())   # Update station records

def tryMoveOwners():
  for key, owner in owners.iteritems():
    if(not owner.isReunited()):
      ownerPositions = owner.move(network.getAllStations()[owner.getLocation()].getConnections()) # Move and get current, previous locations
      network.getAllStations()[ownerPositions[0]].ownerDeparted(owner.getCatTag()) # Update station records
      network.getAllStations()[ownerPositions[1]].ownerArrived(owner.getCatTag())  # Update station records

def runParser():
  parser = argparse.ArgumentParser()
  parser.add_argument('cats', type=int, help='Number of cats and owners')
  parser.add_argument("--debug", action="store_true", help="DEBUG Verbosity")
  parser.add_argument("--max-moves", type=int, help="Search limit", default=10000)
  return parser.parse_args()

def main():
  args = runParser()
  if(int(args.cats)<1):
    print "You need some lost cats to run this program"
    exit(1)

  global debug, cats, owners, network
  cats = OrderedDict()
  owners = OrderedDict()
  network = TFL()
  network.buildStations("./tfl_connections.json", "./tfl_stations.json")
  happyCats = 0
  turn = 0
  reunitedMoves = 0
  closeCalls = set()
  debug = args.debug

  seed(args.cats, network.getAllStations())  # Randomise locations of cats and owners 

  while turn < args.max_moves and happyCats != args.cats:
    if(debug): print "Turn %i" % (turn)
    # Move cats and owners ########################################################
    tryMoveCats()
    tryMoveOwners()
    ###############################################################################

    # Evaluate if any owner found their cat #######################################
    for key, station in network.getAllStations("open").iteritems():
      matches = station.checkForLove()
      for match in matches:
        print "Owner %i found cat %i - %s is now closed." %(match, match, station.name)
        cats[match].reunite()
        owners[match].reunite()
        reunitedMoves+=(cats[match].getMoves() + owners[match].getMoves())
        happyCats+=1
      if(matches): network.closeStation(key)
    ###############################################################################
    turn+=1

  totalTrafficCount = network.getTotalTrafficCount()
  maxConcurrentTraffic = network.getMaxConcurrentTrafficStation()
  maxTraffic = network.getMaxTrafficStation()
  allMatches = network.getAllTimeMatches()
  for match in allMatches: 
    if(not cats[match].isReunited()): 
      closeCalls.add(match) 

  print "Total number of cats: %i" % (args.cats)
  print "Number of cats found: %i" % (happyCats)
  if(reunitedMoves==0 or happyCats==0):
    print "Average number of movements required to find a cat: not possible to caclulate"
  else:
    print "Average number of movements required to find a cat: %i" % (reunitedMoves/happyCats)
  print "Total TFL journeys: %i" % (totalTrafficCount)
  print "Busiest station by number of journeys: %s with %i journeys" % (maxTraffic[0], maxTraffic[1])
  print "Busiest station by concurrent visitors: %s with %i concurrent visitors" % (maxConcurrentTraffic[0], maxConcurrentTraffic[1])
  print "Close calls (pairs that were at same station but at wrong times and eventually never met): %s" % (", ".join(str(s) for s in closeCalls))


if __name__ == "__main__": main()
