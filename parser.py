import os
import json
import bs4
import traceback

def clean(string): 
    if string: 
        return str(string).replace('<td>', '').replace('</td>', '') 
    else: 
        return '' 


def get_data():
    with open("json/character_misc.json", encoding="utf-8") as json_data: 
        data = json.load(json_data, strict=False) 
    for el in data: 
        os.system(f"curl {el['online_webpage']}/ > newjsons/{el['name']}.html") 


def parse_jsons(): 
    for html in sorted(os.listdir("newjsons")): 
        with open(f"newjsons/{html}") as f: 
            if 'html' not in html: 
                continue 
            content = f.read() 
            bs = bs4.BeautifulSoup(content) 
            try: 
                table = bs.find_all('table')[0] 
                rows = table.find_all('tr') 
                moves = [] 
                for row in rows: 
                    #print(row) 
                    try: 
                        inpu, pos, damage, startup, block, hit, counter, notes = row.find_all('td') 
                        moves.append({ 
            "Command": clean(inpu), 
            "Hit level": clean(pos), 
            "Damage": clean(damage), 
            "Start up frame": clean(startup), 
            "Block frame":  clean(block), 
            "Hit frame": clean(hit), 
            "Counter hit frame": clean(counter), 
            "Notes": clean(notes) 
                        }) 
                    except: 
                        print(html) 
                        continue 
                file_ = open(f'newjsons/{html.replace(".html", "")}.json', 'w') 
                js_ = json.dump(moves, file_) 
            except: 
                traceback.print_exc() 
                print(html) 
                break 
    print("done") 
