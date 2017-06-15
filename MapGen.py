import subprocess
import json
import sys

def parseExtended(fileName,count):
    with open(fileName) as json_data:
        parse = json.load(json_data)

        if parse['Result'] == "UNSATISFIABLE":
            print "UNSAT result"
            return

        for i in range(count):
            tiles = {}
            maxX = 1
            maxY = 1
            solution = parse['Call'][0]["Witnesses"][i]['Value']
            for tile in solution:
                if len(tile.split("(")) == 3:
                    vals = tile.split("(")[2].split(",")
                    x = int(vals[0])
                    y = int(vals[1][:-1])
                    ID = vals[2][:-1]
                    maxX = x if x > maxX else maxX
                    maxY = y if y > maxY else maxY
                    key = str(x-1) + "," + str(y-1)
                    if ID != "0":
                        tiles[key] = {"x": x-1, "y": y-1, "id": ID, "width" : 1, "height" : 1}
                elif len(tile.split("(")) == 4:
                    coord = tile.split("(")[2].split(",")
                    x = int(coord[0])
                    y = int(coord[1][:-1])
                    maxX = x if x > maxX else maxX
                    maxY = y if y > maxY else maxY
                    ID = tile.split("(")[3].split(")")[0].split(",")
                    width = int(ID[1])
                    height = int(ID[2])
                    #Base Tile is located at (x - xSize, y - ySize)
                    key = str(x-width) + "," + str(y-height)
                    if key in tiles:
                        tiles[key]["width"] = width if tiles[key]["width"] < width else tiles[key]["width"]
                        tiles[key]["height"] = height if tiles[key]["height"] < height else tiles[key]["height"]
                    else:
                        tiles[key] = {"x": x-width, "y": y-height, "id": ID[0], "width" : width, "height" : height}

            with open('.\\data\\maps\\new_map' + str(i) + '.dat', 'w') as f:
                f.write("properties{\nx = 0,\ny = 0,\n")
                f.write("width = " + str(8*maxX) + ",\n")
                f.write("height = " + str(8*maxY) + ",\n")
                f.write(' min_layer = 0,\nmax_layer = 2,\nworld = "outside_world",\ntileset = "1",\nmusic = "same",\n}\n')
                for idx in tiles:
                    t = tiles[idx]
                    f.write("tile{\nlayer = 0,\n")
                    f.write("x = " + str(t["x"] *8) + ",\n")
                    f.write("y= " + str(t["y"] *8) + ",\n")
                    f.write("width = " + str(t["width"] *8) + ",\n")
                    f.write("height = " + str(t["height"] *8) + ",\n")
                    f.write("pattern = " + t["id"] + ",\n}\n")
    print "Done!"

##Use Case: MapGen.py [MapCount] [Width] [Height] [paramFile] [outPutJSON]
    
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if sys.argv[1] == "help" or sys.argv[1][-1] == "h":
    print "Use Case: MapGen.py [MapCount] [Width] [Height] [paramFile] [outPutJSON]"
    print "All parameters must be present and in order"
    sys.exit(0)

if len(sys.argv) != 6:
    print "Missing argument!"
    sys.exit(0)

mapCount = int(sys.argv[1])
outPutFile = sys.argv[-1]
subprocess.call("clingo-python allTiles.lp buildWaves.lp generateMap.lp " + sys.argv[4] + " --const width=" + sys.argv[2] + " --const height=" + sys.argv[3] + " --project " + str(mapCount) + " --outf=2 > " + outPutFile + " & exit 0", shell=True)

print "clingo-python allTiles.lp buildWaves.lp generateMap.lp " + sys.argv[4] + " --const width=" + sys.argv[2] + " --const height=" + sys.argv[3] + " --project " + str(mapCount) + " --outf=2 > " + outPutFile + " & exit 0"
parseExtended(outPutFile,mapCount)