from itertools import combinations
import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for user in range(0, numUsers):
            self.addUser(user)
        # Create friendships
        totalFriendships = numUsers * avgFriendships
        times_to_call_addfriendship = totalFriendships // 2

        # print(times_to_call_addfriendship)

        userIds = range(1, numUsers + 1 )
        friendship_combinations = combinations(userIds, 2)

        # print(list(friendship_combinations))

        friends = []

        for user in userIds:
            for friend in range(user + 1, numUsers + 1):
                friends.append((user, friend))

        # print(len(friends))
        random.shuffle(friends)
        # print(friends)

        friends_to_make = friends[0:times_to_call_addfriendship]

        for friendship in friends_to_make:
            self.addFriendship(friendship[0], friendship[1])

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # so this is more or less a destination BFT but with a little twist, we are aren't going to destination but rather finding ALL the connections, recording the visited dictionary and the return it
        # sounds simple enough so as always we start with a Q
        q = Queue()
        # then we start with the userID since this is the starting node
        q.enqueue([userID])
        # here we make a new dictionary since we are returing a dictionary
        visited = {}  # Note that this is a dictionary, not a set
        # and again we want to record all the paths, find the shortest one, and use that to determine the shortest path
        all_paths = []
        # so while there is ANYTHING in the q
        while q.size() > 0:
            # we first take the first node in the queue and stick it in the path
            path = q.dequeue()
            # then we use this wonderful python magic to find the last node in the path 
            user = path[-1]
            # if the user is not in the visited which it shouldn't be
            if user not in visited:
                # we now want to insert it so we take the index of the user and fill it in with the path of the current node
                visited[user] = path
                # so now for looping through the list of friendships with the user as a peramiter
                for new_user in self.friendships[user]:
                    # we make a copy of the current path that we made
                    new_path = list(path)
                    # we then append the new user or path in to the path
                    new_path.append(new_user)
                    # so now that we have updated list so to speak as "new_path" we want to reenter it into the queue so we can start the loop again.
                    q.enqueue(new_path)
        # !!!! IMPLEMENT ME
        # then we return the visited path which now shows all paths from user to all it's friends! :D
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(10, 2)
    print(sg.friendships)
    connections = sg.getAllSocialPaths(1)
    print(connections)
