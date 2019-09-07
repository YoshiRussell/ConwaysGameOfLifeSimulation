import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


"""This game of life is built on a grid of nine squares, every cell has eight
    neighboring cells. A given cell (i,j) in the simulation is accessed on a
    grid [i][j]. The value of a given cell at a given instant of time depends
    on the state of its neighbors at the previous time step. """

"""There are four rules:
    1) If a cell is ON and has fewer than two neighbors that are ON it turns OFF
    2) If a cell is ON and has either two or three neighbors that are ON it stays ON
    3) If a cell is ON and has more than three neighbors that are ON it turns OFF
    4) If a cell is OFF and has exactly three neighbors that are ON it turns ON"""

"""These rules are meant to mirror some basic ways that a group of organisms might
    fare over time: underpopulation/overpopulation kill cells by turning cells OFF,
    and ideal scenarios of three ON neighbors which leads to the repoduction of a 
    new cell to turn ON."""


# >> To represent whether a cell is alive(ON) or dead(OFF) on the grid, you'll
#    use values 255 and 0 for ON and OFF respectively. You'll display the current
#    state of the grid using the imshow() method in matplotlib
ON = 255
OFF = 0
vals = [ON, OFF]


def random_grid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)


def add_glider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider


# >> We need to think about how to implement the toroidal boundary conditions.
# >> First, let's see what happens at the right edge of a grid of size NxN
#    > The cell at the end of row i is accessed as grid[i][N-1].
#      Its neighbor to the right is grid[i][N], but according to the toroidal
#      boundary, the value should be grid[i][0]
def update(frame_num, img, grid, N):
    """copy grid since we require 8 neighbors for calculation
        and go line by line"""
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):

            # >> compute 8-neighbor sum using toroidal boundary conditions
            # >> x and y wrap around so taht the simulation takes place
            #    on a toroidal surface
            total = int((grid[i, (j-1) % N] + grid[i, (j+1) % N] +
                         grid[(i-1) % N, j] + grid[(i+1) % N, j] +
                         grid[(i-1) % N, (j-1) % N] + grid[(i-1) % N, (j+1) % N] +
                         grid[(i+1) % N, (j-1) % N] + grid[(i+1) % N, (j+1) % N])/255)

            # apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    new_grid[i, j] = OFF
            else:
                if total == 3:
                    new_grid[i, j] = ON

    # update data
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img,


def main():

    # >> command line arguments are in sys.argv[1], sys.argv[2], ...
    # >> sys.argv[0] is the script name and can be ignored
    # parse argument
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life Simulation")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # >> set grid
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # >> set animation update interval
    update_interval = 50
    if args.interval:
        update_interval = int(args.interval)

    # declare grid
    grid = np.array([])

    # check if "glider" demo flag is specified
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        add_glider(1, 1, grid)
    else:

        # populate grid with random on/off - more off than on
        grid = random_grid(N)

    # set up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10,
                                  interval=update_interval,
                                  save_count=50)

    # number of frames, set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


# call main
if __name__ == '__main__':
    main()




