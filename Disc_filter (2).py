import pickle
import pandas as pd

with open('file.pkl', 'rb') as file:
    mylist = pickle.load(file)

print(mylist)

list_of_filtered_posts = []
for list in mylist:
    filtered_list = list['list of users 2']
    post_id = list['post_id']
    new_filtered_list = [i for i in filtered_list if 'bdate' in i and len(i['bdate']) > 6 and int(i['bdate'][-4:]) >= 2000]
    list_of_likes = len(new_filtered_list)
    post_link = str('https://vk.com/tinkoffbank?w=wall-20225241_' + str(post_id))
    filtered_bdate_post = {'post': post_id, 'link': post_link,  'likes_count': list_of_likes}
    list_of_filtered_posts.append(filtered_bdate_post)

final_dataframe = pd.DataFrame(list_of_filtered_posts)

final_dataframe.sort_values(by=['likes_count'], ascending=False).to_csv('file1.csv', index=False)

print(final_dataframe.sort_values(by=['likes_count'], ascending=False))

