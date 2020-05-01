from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

r_outside = Room(title="Outside Cave Entrance",
               description="North of you, the cave mount beckons")

r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
passages run north and east.""")

r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm.""")

r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
to north. The smell of gold permeates the air.""")

r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""")

class World:

    def init_grid(self):
        self.height = 10
        self.grid = [None] * self.height
        self.width = 10
        self.previous_room = None

        for i in range(len(self.grid)):
            self.grid[i] = [None] * self.width

    def generate_rooms(self):
        for i in range(self.width):
            for j in range(self.height):
                room_name = "Room" + str(i) + str(j)
                self.grid[i,j] = Room(title=room_name, description=room_name)
                self.grid[i,j].save()

    def make_random_connections(self):
        for i in range(80):
            row_num = randint(1,10)
            col_num = randint(1,10)
            direction_list = ["s", "n", "e", "w"]
            direction = random.choice(direction_list)
            if (direction == s) and (j < 10):
                new_room = self.grid[i, j+1]
            elif (direction == n) and (j > 1):
                new_room = self.grid[i, j-1]
            elif (direction == w) and (i > 1):
                new_room = self.grid[i-1, j]
            elif (direction == e) and (i < 10):
                new_room = self.grid[i+1, j]
            self.grid[row_num, col_num].connectRooms(new_room, direction)

world = World()

r_outside.save()
r_foyer.save()
r_overlook.save()
r_narrow.save()
r_treasure.save()

# Link rooms together
r_outside.connectRooms(r_foyer, "n")
r_foyer.connectRooms(r_outside, "s")

r_foyer.connectRooms(r_overlook, "n")
r_overlook.connectRooms(r_foyer, "s")

r_foyer.connectRooms(r_narrow, "e")
r_narrow.connectRooms(r_foyer, "w")

r_narrow.connectRooms(r_treasure, "n")
r_treasure.connectRooms(r_narrow, "s")

players=Player.objects.all()
for p in players:
  p.currentRoom=r_outside.id
  p.save()

