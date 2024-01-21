import curses
import requests
from bs4 import BeautifulSoup

# Function to scrape user data
def scrape_user_data(username):
    url = f'https://leetcode.com/{username}/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('div', class_='text-label-1 dark:text-dark-label-1 break-all text-base font-semibold').text.strip()
        problems_solved_elements = soup.find_all('span', class_='mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1')
        easy_solved, medium_solved, hard_solved = [int(problem.text.strip()) for problem in problems_solved_elements[:3]]
        total_solved = easy_solved + medium_solved + hard_solved
        return {
            'name': name.split()[0],
            'easy_solved': easy_solved,
            'medium_solved': medium_solved,
            'hard_solved': hard_solved,
            'total_solved': total_solved
        }
    else:
        return None

# Function to initialize ncurses and display data
def display_data(stdscr, user_data):
    stdscr.clear()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    title_color = curses.color_pair(1)
    
    column_titles = ["Rank", "Name", "Total", "Easy", "Medium", "Hard"]
    for idx, title in enumerate(column_titles):
        stdscr.addstr(0, idx * 10, title, title_color) # Adjusted starting position
    
    sorted_users = sorted(user_data.items(), key=lambda item: item[1]['total_solved'], reverse=True)
    for row, (username, user) in enumerate(sorted_users, start=1):
        stdscr.addstr(row, 0, str(row), curses.A_BOLD)
        stdscr.addstr(row, 10, user['name'])
        stdscr.addstr(row, 20, str(user['total_solved']))
        stdscr.addstr(row, 30, str(user['easy_solved']))
        stdscr.addstr(row, 40, str(user['medium_solved']))
        stdscr.addstr(row, 50, str(user['hard_solved']))
    
    stdscr.refresh()
    stdscr.getkey()

usernames = ['shaharechaitanya3', 'ritikahotwani24' ]
user_data = {}
for username in usernames:
    data = scrape_user_data(username)
    if data:
        user_data[username] = data

curses.wrapper(display_data, user_data)
