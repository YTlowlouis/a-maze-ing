from mazegen import MazeGenerator

m = MazeGenerator(10, 10)
m.generate()

print(m.get_solution())
print(m.get_maze())
