import bs4
import os
import requests
import sys

for size in [6, 8, 10, 12, 14]:
    for level in [1, 2, 3, 4]:
        nr = 0
        while True:
            nr += 1
            response = requests.get('http://www.binarypuzzle.com/puzzles.php', params = {
                'level': level,
                'size': size,
                'nr': nr
            })
            soup = bs4.BeautifulSoup(response.text, 'lxml')

            # If we're more than the number of options, skip
            puzzle_count = len(list(soup.find('select', {'name': 'nr'}).find_all('option')))
            if nr > puzzle_count:
                break

            # Get the raw values as a single list
            values = [
                cel.text.strip() or '.'
                for cel in soup.find_all('div', {'class': 'puzzlecel'})
            ]

            path = os.path.join(
                '..',
                'puzzles',
                '{size}x{size}'.format(size = size),
                [None, 'easy', 'medium', 'hard', 'very-hard'][level],
                '{nr:03d}.takuzu'.format(nr = nr)
            )
            print(path)

            try:
                os.makedirs(os.path.dirname(path))
            except:
                pass

            with open(path, 'w') as fout:
                for row in range(size):
                    fout.write(''.join(values[row * size : (row + 1) * size]))
                    fout.write('\n')
