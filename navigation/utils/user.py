from graphs.bras_basah import B1, Concourse, WholeStation
from utils.handler import Direction

update_count_threshold = 5

class User:
    def __init__(self,
                 id,
                 current_platform,
                 previous_node,
                 current_node,
                 destination):

        assert current_platform in ['concourse', 'b1'], "Invalid current platform"
        self.id = id
        self.current_platform = current_platform
        self.previous_node = previous_node
        self.current_node = current_node
        self.destination = destination
        self.graph, self.nodes = self.get_graph.visualize_graph()

    @property
    def get_graph(self):
        return WholeStation()
        # b1_model = B1()
        # concourse_model = Concourse()
        # return concourse_model if self.current_platform == 'concourse' else b1_model

    def update(self,
               current_platform,
               previous_node,
               current_node,
               destination):

        self.current_platform = current_platform
        self.previous_node = previous_node
        self.current_node = current_node
        self.destination = destination
        self.graph, self.nodes = self.get_graph.visualize_graph()

        print(f"Current Platform: {self.current_platform}\t Previous Node: {self.previous_node}\t Current Node: {self.current_node}")


# Junction class which is tied at the user level
class Junction:
    def __init__(self, name):
        self.name = name
        self.corners = [float('-inf') for _ in range(4)]
        self.update_count = 0
        self.flag = False

    def __str__(self):
        return f"Junction: {self.name}, corners: {self.corners}, flag: {self.flag}"

    def __repr__(self):
        return f"Junction: {self.name}, corners: {self.corners}, flag: {self.flag}"

    def update_corner(self, corner: int, val: int):
        self.corners[corner] = val
        self.update_count += 1
        print(f"corners updated: {self.corners}")
        return self.prompt_direction()
        
    ##  get the two closest corners, and return the direction
    #   0, 1 -> North
    #   1, 2 -> East
    #   2, 3 -> South
    #   3, 0 -> West
    def prompt_direction(self):
        # only prompt the direction if the update count is greater than the threshold and no direction has been prompted yet
        if self.update_count >= update_count_threshold and not self.flag:
            return None
        # get the two closest corners by going through the list and finding the two smallest values
        max1, max2 = get_max_two_indices(self.corners)
        if self.corners[max2] == float('-inf'):
            return None
        
        # return the direction based on the two closest corners
        self.flag = True
        if max1 in [0, 1] and max2 in [0, 1]:
            return "N"
        elif max1 in [1, 2] and max2 in [1, 2]:
            return "E"
        elif max1 in [2, 3] and max2 in [2, 3]:
            return "S"
        elif max1 in [3, 0] and max2 in [3, 0]:
            return "W"
        else:
            self.flag = False
            print(f"invalid corners: {max1} and {max2} to determine direction of user at {self.name}")
            return None            
        

class UserTracker:
    def __init__(self):
        self.user_mapping = {}

    def track_user(self, user: User):
        self.user_mapping[user] = {}

    def update(self, user: User, junction: str, corner: int, strength: int):
        # check if the junction exists in the user_junction_mapping
        if junction not in self.user_mapping[user]:
            self.user_mapping[user][junction] = Junction(junction)
        # update the junction corner value
        user_position = self.user_mapping[user][junction].update_corner(corner, strength)
        if user_position:
            print(f"User {user.id} is currently coming from {user_position} at junction {junction}")
            user.current_node = junction # update the current position of the user
            # print(f"User {user.id} is currently at junction {junction}")
            if user.current_node == user.destination:    
                print("Reached Destination")
                exit(0) # exit the program for end of simulation
            else:  
                destination = Direction(user)
                direction, _ = destination.handler()
                print(f"User {user.id} should head {direction} next")
    


def get_max_two_indices(arr: list[int]) -> tuple[int, int]:
    max1 = 0
    max2 = 0
    for i in range(len(arr)):
        if arr[i] > arr[max1]:
            max1 = i
    for i in range(len(arr)):
        if i != max1 and arr[i] >= arr[max2]:
            max2 = i
    return max1, max2

  