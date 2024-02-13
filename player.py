import requests
from bs4 import BeautifulSoup

def scrape_player_data(player_name):
    base_url = 'https://www.basketball-reference.com/players/'
    
    player_slug = player_name.lower()  
    split_name = player_slug.split(' ')
    first_name = split_name[0][:2]  
    last_name = split_name[-1][:5]  

    url = f'{base_url}{last_name[0]}/{last_name}{first_name}01.html'
    print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    player_name = soup.select_one('#meta > div > h1 > span').text
    #position = soup.select_one('#meta > div > p:nth-child(4)').text
    position_element = soup.select_one('#meta > div > p:contains("Position")')
    position = position_element.text if position_element else None

    height_weight_element = soup.select_one('#meta > div > p:contains("lb")')
    height_weight = height_weight_element.text if height_weight_element else None

    #height = soup.select_one('#meta > div > p:nth-child(5) > span').text

#Career per game
    per_game_table = soup.find('table', id='per_game')
    headers = per_game_table.select('thead th')  
    rows = per_game_table.select('tbody tr:not(.thead)')
    per_game_stats = []

    for row in rows:
        data = {}
        cells = row.select('td')

        for header, cell in zip(headers[1:], cells):  
            header_text = header.text.strip()
            cell_text = cell.text.strip()
            data[header_text] = cell_text

        per_game_stats.append(data)
    
#Career Totals
    totals_table = soup.find('table', id='totals')
    headers_totals = totals_table.select('thead th')
    rows_totals = totals_table.select('tbody tr')
    totals_stats = []

    for row in rows_totals:
        data = {}
        cells = row.select('td')

        for header, cell in zip(headers_totals[1:], cells):  
            header_text = header.text.strip()
            cell_text = cell.text.strip()
            data[header_text] = cell_text

        totals_stats.append(data)

#Playoffs per game
    playoffs_per_game_table = soup.find('table', id='playoffs_per_game')
    playoffs_per_game_stats = []
    if playoffs_per_game_table is not None:
        headers_playoffs_per_game = playoffs_per_game_table.select('thead th')
        rows_playoffs_per_game = playoffs_per_game_table.select('tbody tr')

        for row in rows_playoffs_per_game:
            data = {}
            cells = row.select('td')

            for header, cell in zip(headers_playoffs_per_game[1:], cells):  
                header_text = header.text.strip()
                cell_text = cell.text.strip()
                data[header_text] = cell_text

            playoffs_per_game_stats.append(data)

    # Return the player data as a dictionary or a custom Player object
    player_data = {
        'name': player_name,
        'position': position,
        'height_weight': height_weight,
        'per_game_stats': per_game_stats,
        'totals_stats': totals_stats,
        'playoffs_per_game_stats': playoffs_per_game_stats,
        
    }
    return player_data

# Get the player's name from user input
player_name = input('Enter the player\'s name: ')

# Scrape the player data based on the user's input
player_data = scrape_player_data(player_name)
print('Player Name:', player_data['name'])
print('Position:', player_data['position'])
print('Height & Weight:', player_data['height_weight'])
print('Regular season Career Averages:', player_data['per_game_stats'])
print('Career Totals:', player_data['totals_stats'])
print('Playoffs Career Averages:', player_data['playoffs_per_game_stats'])
