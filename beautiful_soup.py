from bs4 import BeautifulSoup
import re

def parse(path_to_file):
    html = open(path_to_file, 'r', encoding='utf-8')
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find('div', id="bodyContent")
    
    # кол-во картинок с width >= 200
    amount_img = sum(1 for tag in 
        body.find_all('img', {"width": re.compile(r".*")}) 
        if int(tag['width']) >= 200)
    
    # кол-во заголовков, где text[0] = 'E', 'C' или 'T'
    amount_headers = sum(1 for tag 
                         in body.find_all(re.compile(r"^[h]")) 
                         if re.match(r'[ETC]', tag.get_text()) != None)
    
    # длина макс последовательности ссылок без тегов внутри
    max_link = 1
    link = body.find_next('a')
    while link:
        max_in_link = 1
        if link.next_sibling is not None \
                and '\n' not in link.next_sibling:
            for tag in link.find_next_siblings():
                if tag.name == 'a':
                    if tag.next_sibling is not None \
                    and '\n' in tag.next_sibling:
                        break
                    max_in_link += 1
                else:
                    break
        max_link = max(max_link, max_in_link)
        link = link.find_next('a')
    
    # Количество списков, не вложенных в другие списки
    lists = 0
    html_lists = body.find_all(['ul', 'ol'])
    for html_list in html_lists:
        if not html_list.find_parents(['ul', 'ol']):
            lists += 1
            
    html.close()

    return [amount_img, amount_headers, max_link, lists]