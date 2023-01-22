import requests
import time
import pickle
import datetime


access_token = 'vk1.a.thN3M7NRaUNPknDm1e1_7Az4hnw2LyMPj4mjrVs-CmjyaMExSA6BkglY_GwpyUM_4WSmTU1565eDkWmZlHym8zF6E2-NXkXE8HYwS8XPqP7bZLLd7d8zwvoLYVnqtnFKWq8bIo8S0X3yhGXHj6ozWRAu33XQfXTlKfM3n62usNLd3Gfqc0g5L1F5OghcOYpO'
owner_id = '-20225241'
count = 100
offset = 0

f = open("file.pkl", "wb")


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
for post1 in final_filter:
    id1 = post1['id']
    ID_list.append(id1)


def get_all_liked_lists(access_token, owner_id, liked_object_id, count=1000, offset=0, friends_only=0):
    time.sleep(0.5)
    api_query = getjson('https://api.vk.com/method/likes.getList',
                        {'access_token': access_token, 'type': 'post', 'owner_id': owner_id, 'item_id': liked_object_id,
                         'filter': 'likes', 'friends_only': friends_only, 'count': count, 'v': '5.131'})
    Users_count = api_query['response']['count']
    List_of_users = api_query['response']['items']
    return Users_count, List_of_users


User_lists_collection = []
for item in ID_list:
    liked_object_id = item
    User_list_of_responses = get_all_liked_lists(access_token, owner_id, liked_object_id)
    Final_list = {'items': liked_object_id, 'count': User_list_of_responses[0],
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
    person_bdate = get_all_users_bdate(access_token, owner_id, user_id)
    final_list_postid_and_users_with_bd = {'post_id': list1['items'], 'list of users 2': person_bdate}
    global_list.append(final_list_postid_and_users_with_bd)

pickle.dump(global_list, f)

f.close()

print(global_list)
