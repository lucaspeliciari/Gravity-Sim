from classes.barnes_hut.cube import Cube

BODY_LIMIT_PER_NODE = 1


class Node:
    def __init__(self,
                 # x: int,
                 # y: int,
                 # z: int,
                 # width: int,
                 # height: int,
                 # depth: int,
                 cube: Cube = Cube(0,0,0,0,0,0),
                 branch: int = 0,
                 level: int = 0  # used to be called depth
                 ):
        # self.x = x
        # self.y = y
        # self.z = z
        # self.width = width
        # self.height = height
        # self.depth = depth

        self.cube = cube

        self.bodies = []
        self.children = []
        self.divided = False

        self.branch = branch
        self.level = level

    def insert(self, body):
        if not self.contains(body):
            return False

        if len(self.bodies) < BODY_LIMIT_PER_NODE:
            self.bodies.append(body)
            return True
        if not self.divided:
            self.subdivide()

        return (self.children[0].insert(body) or
                self.children[1].insert(body) or
                self.children[2].insert(body) or
                self.children[3].insert(body) or
                self.children[4].insert(body) or
                self.children[5].insert(body) or
                self.children[6].insert(body) or
                self.children[7].insert(body))

    def contains(self, body):
        # return self.x <= body.x < self.x + self.width and \
        #        self.y <= body.y < self.y + self.height and \
        #        self.z <= body.z < self.z + self.depth
        return self.cube.x <= body.x < self.cube.x + self.cube.width and \
               self.cube.y <= body.y < self.cube.y + self.cube.height and \
               self.cube.z <= body.z < self.cube.z + self.cube.depth

    def subdivide(self):  # subdivide in 8 cubes, seems to work, but has a few bugs like not being centered around (0,0,0)
        self.divided = True
        # x, y, z = self.x, self.y, self.z
        # new_width, new_height, new_depth = self.width // 2, self.height // 2, self.depth // 2
        x, y, z = self.cube.x, self.cube.y, self.cube.z
        new_width, new_height, new_depth = self.cube.width // 2, self.cube.height // 2, self.cube.depth // 2

        zero_front = Node(Cube(x + new_width, y, z, new_width, new_height, new_depth), branch=0, level=self.level + 1)
        zero_rear = Node(Cube(x + new_width, y, z + new_depth, new_width, new_height, new_depth), branch=1,
                         level=self.level + 1)
        one_front = Node(Cube(x, y, z, new_width, new_height, new_depth), branch=2, level=self.level + 1)
        one_rear = Node(Cube(x, y, z + new_depth, new_width, new_height, new_depth), branch=3, level=self.level + 1)
        two_front = Node(Cube(x, y + new_height, z, new_width, new_height, new_depth), branch=4, level=self.level + 1)
        two_rear = Node(Cube(x, y + new_height, z + new_depth, new_width, new_height, new_depth), branch=5,
                        level=self.level + 1)
        three_front = Node(Cube(x + new_width, y + new_height, z, new_width, new_height, new_depth), branch=6,
                           level=self.level + 1)
        three_rear = Node(Cube(x + new_width, y + new_height, z + new_depth, new_width, new_height, new_depth), branch=7,
                          level=self.level + 1)
        self.children = [zero_front, zero_rear, one_front, one_rear, two_front, two_rear, three_front, three_rear]

        for body in self.bodies:
            for child in self.children:
                if child.contains(body):
                    child.insert(body)

    def get_cubes(self):  # tough in 3d
        cubes = [(self.cube, self.level)]  # testing colors based on level (fka depth)
        if self.divided:
            for child in self.children:
                for cube in child.get_cubes():
                    cubes.append(cube)
        return cubes

    def get_all_bodies(self):
        bodies = []
        if self.divided:
            for child in self.children:
                bodies += child.get_all_bodies()
        elif len(self.bodies) > 0:
            for body in self.bodies:
                bodies.append(body)
        return bodies

    def get_deepest(self):
        depths = []
        if not self.divided:
            depths.append(self.level)
        else:
            for child in self.children:
                depths.append(child.get_deepest())
        return max(depths)

    def get_number_all_bodies(self):  # is this superfluous? just use len(get_all_bodies)
        number_bodies = 0
        if not self.divided:
            number_bodies = len(self.bodies)
        else:
            for child in self.children:
                number_bodies += child.get_number_all_bodies()
        return number_bodies

    def get_number_specific_bodies(self, level, branch):  # wrong
        number_bodies = 0
        if level == self.level:
            if branch == self.branch:
                number_bodies += len(self.bodies)
        elif self.divided:
            for child in self.children:
                number_bodies += child.get_number_specific_bodies(level, branch)
        return number_bodies

    def get_specific_bodies(self, level, branch):  # wrong
        bodies = []
        if level == self.level:
            if branch == self.branch:
                if self.divided:
                    for child in self.children:
                        bodies += child.get_specific_bodies(self.level, branch)
                        # for body in child.bodies:
                        #     bodies.append(body)
                else:
                    for body in self.bodies:
                        bodies.append(body)
        elif self.divided:
            for child in self.children:
                bodies += child.get_specific_bodies(self.level + 1, branch)
        return bodies

    def intersect(self, other_cube):
        # shouldn't this be and instead of or?
        return not (other_cube.x > self.cube.x + self.cube.width or
                    other_cube.x + other_cube.width < self.cube.x or
                    other_cube.y > self.cube.y + self.cube.height or
                    other_cube.y + other_cube.height < self.cube.y)

    def query(self, other_cube):
        if not self.intersect(other_cube):  # if the
            return False

    def update(self, bodies):
        self.bodies.clear()
        self.children.clear()
        self.divided = False
        for body in bodies:
            self.insert(body)

    def get_center_of_mass(self, level, branch):  # test test test
        bodies = self.get_specific_bodies(level, branch)
        # print([a.name for a in bodies])
        x = 0
        y = 0
        z = 0
        total_mass = 0

        if len(bodies) <= 0:
            return False  # might cause problems later

        for body in bodies:
            x += body.x * body.mass
            y += body.y * body.mass
            z += body.z * body.mass
            total_mass += body.mass

        x /= total_mass
        y /= total_mass
        z /= total_mass

        return x, y, z

    # def __str__(self):
