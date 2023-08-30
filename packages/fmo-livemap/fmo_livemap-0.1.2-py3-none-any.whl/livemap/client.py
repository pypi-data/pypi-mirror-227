import time
import requests

class Polyline:
    def __init__(self, map, name, points, **kwargs):
        self.map = map
        self.name = name
        self.points = points

    def extend(self, points):
        if type(points[0]) is float:
            points = [points]

        for point in points:
            response = requests.post(f"{self.map.url}/polylines/{self.name}/points", json={
                "latitude": point[0],
                "longitude": point[1]
            })
            if not response.ok:
                print(response.reason)
                raise Exception(response.reason)

class Map:
    def __init__(self, url):
        self.url = url

    def polyline(self, name, points):
        response = requests.post(f"{self.url}/polylines", json={"name": name, "points": points})
        if not response.ok:
            raise Exception(response.reason)
        data = response.json()
        return Polyline(self, **data)



gps_data = [
  [38.91168232416608, -76.47992628575723,],
  [38.91167723745552, -76.47998040159345],
  [38.911660346950676, -76.48003362018159],  
  [38.91163193259245, -76.48008505529343],
  [38.91159245603817, -76.48013384887776],
  [38.91154255338108, -76.4801791845924],
  [38.91148818673626, -76.48022588905636],
  [38.91142387753969, -76.48026912019613],
  [38.91135045470874, -76.48030791267406],
  [38.911268963041756, -76.48034139145376],
  [38.91118060039576, -76.48036874891672],
  [38.9110867003822, -76.48038926174374],
  [38.91098871241652, -76.48040230666497],
  [38.9108881794186, -76.48040737474784],
  [38.91078671350825, -76.48040408391331],
  [38.910685970081836, -76.48039218939842],
  [38.9105876206919, -76.48037159191706],
  [38.91049332518039, -76.48034234331065],
  [38.91040470353717, -76.48030464952399],
  [38.9103233079686, -76.48025887079041],
  [38.91025059566554, -76.48020551896194],
]

if __name__ == "__main__":
    map = Map("http://127.0.0.1:5050")

    my_line = map.polyline("myline", [])

    for p in gps_data:
        my_line.extend(p)
        time.sleep(2)