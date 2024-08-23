from typing import Union, Tuple
import math
import networkx as nx
from graphs.bras_basah import B1, Concourse


class Direction:
    def __init__(self,
                 user):
        self.user = user
        self.graph = user.graph
        self.node_location = user.nodes

    def handler(self) -> tuple[str, str]:
        previous_node = self.user.previous_node
        destination = self.user.destination
        shortest_path = nx.shortest_path(self.graph,
                                         source=previous_node,
                                         target=destination)

        previous_node, current_node, next_node = shortest_path[0], shortest_path[1], shortest_path[2]
        return self.get_direction(previous_node, current_node, next_node)

    def get_direction(self,
                      previous_node: str,
                      current_node: str,
                      next_node: str):
        previous_x, previous_y = self.node_location[previous_node]
        current_x, current_y = self.node_location[current_node]
        next_x, next_y = self.node_location[next_node]

        # Get current orientation
        previous_direction = math.degrees(math.atan2(current_x - previous_x, current_y - previous_y))
        next_direction = math.degrees(math.atan2(next_x - current_x, next_y - current_y))

        if current_node in ['LIFT', 'LIFT_B1'] and not next_node in ['LIFT', 'LIFT_B1']:
            return 'Straight', next_node

        elif current_node in ['LIFT_B1'] and next_node in ['LIFT']:
            return 'Take Lift Up', next_node

        elif current_node in ['LIFT'] and next_node in ['LIFT_B1']:
            return 'Take Lift Down', next_node

        elif next_direction == previous_direction:
            return 'Straight', next_node

        elif next_direction - previous_direction == 90:
            return 'Right', next_node

        elif next_direction - previous_direction == -90:
            return 'Left', next_node

        elif previous_direction == -90 and next_direction == 180:
            return 'Left', next_node

        elif previous_direction == 180 and next_direction == -90:
            return 'Right', next_node

        else:
            print(previous_direction, next_direction)
            raise Exception


# Static Mapping of junction index to the actual junction name string
junction_mapping = {
    0: 'EXIT A',
    1: 'EXIT B',
    2: 'INT 1',
    3: 'GANTRY 1',
    4: 'L11',
    5: 'L12',
    6: 'L13',
    7: 'LIFT',
    8: 'L14',
    9: 'L15',
    10: 'GANTRY 2',
    11: 'INT 2',
    12: 'EXIT C',
    13: 'EXIT D',
    14: 'D1',
    15: 'D2',
    16: 'D3',
    17: 'D4',
    18: 'D5',
    19: 'D6',
    20: 'D7',
    21: 'D8',
    22: 'D9',
    23: 'D10',
    24: 'D11',
    25: 'H1',
    26: 'H2',
    27: 'H3',
    28: 'H4',
    29: 'H5',
    30: 'H6',
    31: 'H7',
    32: 'H8',
    33: 'H9',
    34: 'H10',
    35: 'H11',
    36: 'L1',
    37: 'L2',
    38: 'L3',
    39: 'L4',
    40: 'L5',
    41: 'LIFT_B1'
}


def parse_data(data: str) -> list[int]:
    try:
        # expected relevant data : "b:<VAL>-<VAL>;u:<VAL>;s:<VAL>;<checksum>"
        if data[0] != "b":
            return None
        
        # split the data into the three parts
        tokens = data.split(";")
        # get the user id
        user_id = int(tokens[1].split(":")[1])
        # get the junction id
        junction_id = int(tokens[0].split(":")[1].split("-")[0])
        # get the corner id
        corner_id = int(tokens[0].split(":")[1].split("-")[1])
        # get the strength value
        strength = int(tokens[2].split(":")[1])
        checksum = int(tokens[3])
        if checksum != (junction_id + corner_id + strength):
            raise ValueError("data corrupted: checksum failed for: " + str(data) + f", checksum: {checksum}, expected: {junction_id + corner_id + strength}")
        
        if junction_id not in junction_mapping:
            raise ValueError(f"Invalid junction id: {junction_id}")

        return [user_id, junction_mapping[junction_id], corner_id, strength]
            
    except Exception as e:
        print(f"Error in parsing data: {e}")
        return None
    
