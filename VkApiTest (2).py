import requests
import time
import pickle
import datetime


access_token = 'vk1.a.aqDNjg_0HOiMekTJF10qns9FspCjVrMrhmgvf8Pvv2mdGBH3gEhExCxA1oelFlr_9wn_NmAvgg__hsQoCNQ-yI2jpESX7G-VQLAmn9X-58PDTgiYKWEuZ1ArDuypjRNE-KNbYL7eLauxuMwFqnrHGh0IKndEBu_HFXFJmL0BmYTJJ4nB0J_3Dnp8gVJtqW9-'
owner_id = '-145457488'
count = 100
offset = 0

f = open("file.pkl", "wb")
with open("yes.txt", "r") as file:
    files = file.read()
    emoji = files.split()


def getjson(url, data=None):
    response = requests.get(url, params=data)
    response = response.json()
    return response


def get_all_posts(access_token, owner_id, count=100, offset=0):
    all_posts = []
    while True:
        time.sleep(1)
        wall = getjson('https://api.vk.com/method/wall.get',
                       {'owner_id': owner_id, 'offset': offset, 'count': count, 'access_token': access_token, 'v': '5.131'})
        count_posts = wall['response']['count']
        posts = wall['response']['items']

        all_posts.extend(posts)

        last_post_date = int(datetime.datetime.fromtimestamp(int(all_posts[-1]['date'])).strftime('%Y'))

        if last_post_date == 2021:
            break
        else:
            offset += 100
    return all_posts


def filter_texts(all_posts):
    filtered_data = []
    for post in all_posts:
        try:
            id = post['id']
        except:
            id = ' '
        try:
            text = post['text']
        except:
            text = 'текста нет'
        try:
            likes = post['likes']['count']
        except:
            likes = 0

        filtered_post = {'id': id, 'text': text, 'likes': likes}
        filtered_data.append(filtered_post)

    return filtered_data


all_posts = get_all_posts(access_token, owner_id)

final_filter = filter_texts(all_posts)

ID_list = []
txt_list = []
for post1 in final_filter:
    id1 = post1['id']
    txt = post1['text']
    ID_list.append(id1)
    txt_list.append(txt)

def get_all_liked_lists(access_token, owner_id, liked_object_id, count=1000, offset=0, friends_only=0):
    time.sleep(0.5)
    api_query = getjson('https://api.vk.com/method/likes.getList',
                        {'access_token': access_token, 'type': 'post', 'owner_id': owner_id, 'item_id': liked_object_id,
                         'filter': 'likes', 'friends_only': friends_only, 'count': count, 'v': '5.131'})
    Users_count = api_query['response']['count']
    List_of_users = api_query['response']['items']
    return Users_count, List_of_users


User_lists_collection = []
Final_list = {}
t = 0
for item in ID_list:
    text_id = txt_list[t]
    tsplit = text_id.split()
    t += 1
    emojicount = 0
    tagscount = 0
    wordcount = 0
    linkcount = 0
    for i in range(len(tsplit)):
        tsp = tsplit[i]
        x = tsp.find('#')
        if x != (-1):
            tagscount += 1
            wordcount -= 1
        for j in range(len(tsp)):
            if tsp[j] in emoji:
                emojicount +=1
        if tsp not in emoji:
            wordcount += 1
        y = tsp.find('.')
        if y != (-1) and y != len(tsp)-1:
            linkcount += 1
            wordcount -= 1
    liked_object_id = item
    User_list_of_responses = get_all_liked_lists(access_token, owner_id, liked_object_id)
    Final_list = {'items': liked_object_id, 'text_id': text_id, 'emoji': emojicount, 'tags': tagscount, 'links': linkcount, 'words': wordcount, 'count': User_list_of_responses[0],
                  'list of users': User_list_of_responses[1]}
    User_lists_collection.append(Final_list)


def get_all_users_bdate(access_token, user_ids, fields, count=100, offset=0, friends_only=0):
    time.sleep(0.5)
    api_query_user_info = getjson('https://api.vk.com/method/users.get',
                                  {'access_token': access_token, 'user_ids': user_id, 'fields': 'bdate', 'count': count,
                                   'v': '5.131'})
    User_Birth_date = api_query_user_info['response']
    # User_Birth_date = api_query_user_info['response'][0]
    return User_Birth_date


global_list = []
for list1 in User_lists_collection:
    list_of_users_ids = list1['list of users']
    user_id = str(list_of_users_ids).strip('[]')
    post_text_id = list1['text_id']
    emojis = list1['emoji']
    tags = list1['tags']
    links = list1['links']
    words = list1['words']
    person_bdate = get_all_users_bdate(access_token, owner_id, user_id)
    final_list_postid_and_users_with_bd = {'post_id': list1['items'], 'list of users 2': person_bdate, 'text': post_text_id, 'words': words, 'emojis': emojis, 'tags': tags, 'links': links}
    global_list.append(final_list_postid_and_users_with_bd)

pickle.dump(global_list, f)

f.close()

print(global_list)
