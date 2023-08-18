import os
from typing import List, Dict

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties, FontManager

InfluencerDictType = Dict[str, int]

InfluencerListType = List[InfluencerDictType]
df_posts = None
df_users = None
df = None
current_directory = os.getcwd()
print("Current working directory:", current_directory)
try:
    csv_users_posts_file = current_directory + '/src/user_posts.csv'
    df_posts = pd.read_csv(csv_users_posts_file)

    # load users 
    csv_users_file = current_directory + '/src/users.csv'
    df_users = pd.read_csv(csv_users_file)

    df  = pd.merge(df_posts, df_users, left_on='person_id', right_on='id', how='inner')

except FileNotFoundError:
    raise FileNotFoundError("CSV file not found :/")

def calculate_engagement(total_likes: int, total_comments: int, total_num_followers: int):
   
    ratio = (total_likes + total_comments) / total_num_followers
   
    percent = ratio * 100
    
    
    return percent

    # helper function to return the average score et al for general 
def general_results(data: pd.DataFrame): 
    df2 = data.assign(avg_gen=calculate_engagement(data['like_count'].astype(int), data['comment_count'].astype(int), data['ig_num_followers'].astype(int)))

    grouped_data_general = df2.assign(engagement_general=df2.groupby('person_id')['avg_gen'].transform('mean').apply(lambda x: '{:.2f}'.format(x)) + '%')
   
    return grouped_data_general

    # helper function to return the average score et al for specific ppl who mention 
def specific_results(data: pd.DataFrame): 
    # Group the data by 'person_id' 
    grouped_data_specific = data.groupby('person_id')
    filtered_groups = []
    
# loop through grouped data 
   
    persons_posts_list = []
    persons_post_hashtag_list = []
    person_posts_mention_list = []
    for person_id, group in grouped_data_specific:
        
        posts_count = 0
        post_hashtag_count = 0
        post_mention_count = 0
        for _, row in group.iterrows(): 
            
            if "#bubbleroom" in str(row['caption_text']) or "#bubbleroomstyle" in str(row['caption_text']):
                    posts_count += 1
                    post_hashtag_count = str(row['caption_text']).count('#bubbleroom') + str(row['caption_text']).count('#bubbleroomstyle')
                   
                    dict_posts_for_person_id = {person_id: posts_count}
                    dict_post_hashtags_for_person_id = {person_id: post_hashtag_count}
                    # count the total number of posts made by an influencer 
                    if any(person_id in d for d in persons_posts_list):
                        persons_posts_list = [{key: posts_count if key == person_id else value for key, value in d.items()} for d in persons_posts_list]
                    else: 
                        persons_posts_list.append(dict_posts_for_person_id)
                    # count the total number of hashtags for an influencer
                    if any(person_id in d for d in persons_post_hashtag_list):
                        persons_post_hashtag_list = [{key: d[person_id] + post_hashtag_count if key == person_id else value for key, value in d.items()} for d in persons_post_hashtag_list]
                    else: 
                        persons_post_hashtag_list.append(dict_post_hashtags_for_person_id)
                   
                    filtered_groups.append(row)
            elif  "@bubbleroom" in str(row['caption_text']): 
                posts_count += 1
                post_mention_count = str(row['caption_text']).count('@bubbleroom')
               
                dict_posts_for_person_id = {person_id: posts_count}
                dict_posts_mentions_for_person_id = {person_id: post_mention_count}
                 # count the total number of posts made by an influencer 
                if any(person_id in d for d in persons_posts_list):
                        persons_posts_list = [{key: posts_count if key == person_id else value for key, value in d.items()} for d in persons_posts_list]
                else: 
                        persons_posts_list.append(dict_posts_for_person_id)
                #count the total number of mentions by an influencer 
                if any(person_id in d for d in person_posts_mention_list):
                        person_posts_mention_list = [{key:  d[person_id] + post_mention_count if key == person_id else value for key, value in d.items()} for d in person_posts_mention_list]
                else: 
                        person_posts_mention_list.append(dict_posts_mentions_for_person_id)

                filtered_groups.append(row)

        posts_count = 0
        post_mention_count = 0
        post_hashtag_count = 0
    print("INFLUENCERS POSTS")
    print(persons_posts_list)
    print("--------------------")  

    print("INFLUENCERS MENTIONS")
    print(person_posts_mention_list)
    print("--------------------")  

    print("INFLUENCERS HASHTAGS")
    print(persons_post_hashtag_list)
    print("--------------------")  

    res = pd.DataFrame()   
    for series in filtered_groups:
        res = res._append(series, ignore_index=True)
    
    
    df2 = res.assign(avg_gen=calculate_engagement(res['like_count'].astype(int), res['comment_count'].astype(int), res['ig_num_followers'].astype(int)))

    df3 = df2.assign(engagement_specific=df2.groupby('person_id')['avg_gen'].transform('mean').apply(lambda x: '{:.2f}'.format(x)) + '%')
    
    return (df3, persons_posts_list, persons_post_hashtag_list, person_posts_mention_list)
    

def filter_by_date() -> pd.DataFrame: 
    
    # Convert the 'date' column to datetime type
    df["taken_at"] = pd.to_datetime(df["taken_at"])
    
    # extract the month you are targeting into a variable
    target_month = 1     
    target_year = 2021
    # Filter the DataFrame for a particular month
    filtered_df = df[(df['taken_at'].dt.month == target_month) & (df['taken_at'].dt.year == target_year)]

    return filtered_df

def group_by_person_id(data: pd.DataFrame) -> tuple[pd.DataFrame, InfluencerListType, InfluencerListType, InfluencerListType]: 
    # Group the data by 'person_id' 
    grouped_data_specific, influencer_posts,influencer_posts_with_hashtag, influencer_posts_with_mentions = specific_results(data)

    grouped_data_specific = grouped_data_specific.drop('avg_gen', axis=1)
    grouped_data_general = general_results(data).drop('avg_gen', axis=1).drop_duplicates(subset='person_id')
    grouped_data_specific['actual reach'] = grouped_data_specific['ig_num_followers'].sum()
    grouped_data_general['influencers'] = grouped_data_general['ig_username']
    print(grouped_data_general)
    print("-------------------------")
    merged_data = pd.merge(grouped_data_general, grouped_data_specific, on='person_id', how='inner')

    df_with_specified_columns = merged_data[["influencers","engagement_general", "engagement_specific", "actual reach", "person_id"]]
 
   
    return (df_with_specified_columns,influencer_posts,influencer_posts_with_hashtag, influencer_posts_with_mentions)

# add columns like posts, post mentions and score
def add_influencer_score_columns(data: pd.DataFrame, influencer_posts: InfluencerListType,influencer_posts_with_hashtag: InfluencerListType, influencer_posts_with_mentions: InfluencerListType ) -> pd.DataFrame: 
     for post in influencer_posts: 
         
          for person_id in post: 
              
               if person_id in data['person_id'].values: 
                   
                     data.loc[data['person_id'] == person_id, 'posts'] = post[person_id]
                     data['posts'] = data['posts'].fillna(0)

     for post in influencer_posts_with_hashtag: 
         
          for person_id in post: 
              
               if person_id in data['person_id'].values: 
                   
                     data.loc[data['person_id'] == person_id, 'post hashtags'] = post[person_id]             
                     data['post hashtags'] = data['post hashtags'].fillna(0)
        
     for post in influencer_posts_with_mentions: 
         
          for person_id in post: 
              
               if person_id in data['person_id'].values: 
                   
                     data.loc[data['person_id'] == person_id, 'post mentions'] = post[person_id]             
                     data['post mentions'] = data['post mentions'].fillna(0)
     data['score'] = data['posts'] + data['post hashtags'] + data['post mentions']
     data = data.drop('person_id', axis=1)
     print("FINAL DATA")
     print(data)
     print("-------------------")
     return data

def create_pdf(data: pd.DataFrame): 
     
     image_path = current_directory + '/src/cover.png'
     font_path = current_directory + '/src/Roboto-Regular.ttf'
     output_dir = current_directory + "/influencers.pdf"
     # Register the font
       
     custom_font = FontProperties(fname=font_path)

# Add the image to the first page
     with PdfPages(output_dir) as pdf:
    # Add the first page with the image
        fig = plt.figure(figsize=(30, 15))
        plt.imshow(plt.imread(image_path))  # Replace with your image path
        plt.axis('off')  # Turn off axes
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

    # Add subsequent pages with the dataframe
        fig = plt.figure(figsize=(8,4))
        ax = fig.add_subplot(111)
        ax.axis('tight')
        ax.axis('off') 
    
     
   
    
        
        # ax.table(cellText=data.values, colLabels=data.columns, cellLoc='center', loc='center', colWidths=[0.4, 0.4, 0.4, 0.4,0.4,0.4,0.4,0.4])

        table_data = [data.columns] + data.values.tolist()
        table = ax.table(cellText=table_data, colLabels=None, cellLoc='center', loc='center', colWidths=[0.2, 0.2, 0.2, 0.2,0.2,0.2,0.2,0.2])

        # set font 
        for cell in table._cells:
            cell_text = table._cells[cell].get_text()
            cell_text.set_fontproperties(custom_font)

        # make table a bit nicer 

        table.set_fontsize(16)
        table.scale(1.6,1.6)
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

filtered_res = filter_by_date()
res = group_by_person_id(filtered_res)
result = add_influencer_score_columns(*res)

create_pdf(result)
