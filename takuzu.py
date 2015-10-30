import config
import model
import solvers
import time

try:
    solve = getattr(solvers, config.method).solve
except:
    print('Unknown solver: {}'.format(config.method))
    sys.exit(-1)

for filename in config.files:
    takuzu = model.Takuzu(filename = filename)
    start = time.time()
    takuzu = solve(takuzu)
    end = time.time()

    if config.animated:
        print = config.animate

    print('{}\nSolved in {:.02f} seconds'.format(takuzu, end - start))
