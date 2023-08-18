import os 
from typing import List, Dict
from datetime import datetime
from itertools import dropwhile, takewhile

import pandas as pd
import instaloader

L = instaloader.Instaloader()

InfluencerDictType = Dict[str, int]
InfluencerListType = List[InfluencerDictType]

class Scraper: 
    def __init__(self) -> None:
      
        self.df_posts = None
        self.df_users = None
        self.columns=['ig_username', 'caption_text', 'taken_at']
        self.df = pd.DataFrame(columns=self.columns)
        self.df_list = []
       
        self.session_id = os.environ.get("session_id")
        self.current_directory = os.getcwd()
        print("Current working directory:", self.current_directory)
        try:
      
            # load users 
            csv_users_file = self.current_directory + '/src/users.csv'
            self.df_users = pd.read_csv(csv_users_file)

            
        except FileNotFoundError:
            raise FileNotFoundError("CSV file not found :/")
    
    def __get_ig_users(self): 
         influencers = self.df_users['ig_username'].tolist()
         return influencers
    
    def get_ig_users_info_for_brand(self):
         SINCE = datetime(2023, 7, 1)
         UNTIL = datetime(2023, 7, 31)
         influencers: List[str] = self.__get_ig_users()
        
         
         try: 
              # loop through influencer and set the profile name
              # loop through their posts and do profile.get_followers(), .get_followees() and save the name 
                for influencer in influencers[:50]: 
                     
                    profile = instaloader.Profile.from_username(L.context,influencer)
                    if not profile.is_private:
                        user_posts =  profile.get_posts()  
                    
                        k = 0  # initiate k

                        for post in user_posts:
                            postdate = post.date
                        
                        
                            if postdate > UNTIL:
                                continue
                            elif postdate <= SINCE:
                                k += 1
                                if k == 50:
                                    break
                                else:
                                    continue
                            else:
                                
                                data = {
                                    'ig_username': influencer,
                                    'caption_text': post.caption,
                                    'taken_at': postdate
                                }
                                print(postdate)
                                
                                self.df_list.append(data)
                                #L.get_json()
                                # if you want to tune k, uncomment below to get your k max
                                #k_list.append(k)
                                k = 0
                self.df = pd.DataFrame(self.df_list, columns=self.columns)
                print(self.df)
       
         except Exception as e: 
              print(self.df_list)
              print("----------------")
              if len(self.df_list) > 0: 
                   self.df = pd.DataFrame(self.df_list, columns=self.columns)
                   print(self.df)
              print("SOMETHING GOT FUCKED", e)
         print(self.df_list)
         return self.df

   
    # helper function to return the average score et al for specific ppl who mention 
    def __specific_results(self, data: pd.DataFrame): 
    # Group the data by 'person_id' 
        grouped_data_specific = data.groupby('ig_username')
      
# loop through grouped data 
   
        persons_posts_list = []
        persons_post_hashtag_list = []
        person_posts_mention_list = []
        for ig_username, group in grouped_data_specific:
        
            posts_count = 0
            post_hashtag_count = 0
            post_mention_count = 0
            for _, row in group.iterrows(): 
            
                if "#bubbleroom" in str(row['caption_text']) or "#bubbleroomstyle" in str(row['caption_text']):
                        posts_count += 1
                        post_hashtag_count = str(row['caption_text']).count('#bubbleroom') + str(row['caption_text']).count('#bubbleroomstyle')
                    
                        dict_posts_for_person_id = {ig_username: posts_count}
                        dict_post_hashtags_for_person_id = {ig_username: post_hashtag_count}
                        # count the total number of posts made by an influencer 
                        if any(ig_username in d for d in persons_posts_list):
                            persons_posts_list = [{key: posts_count if key == ig_username else value for key, value in d.items()} for d in persons_posts_list]
                        else: 
                            persons_posts_list.append(dict_posts_for_person_id)
                        # count the total number of hashtags for an influencer
                        if any(ig_username in d for d in persons_post_hashtag_list):
                            persons_post_hashtag_list = [{key: d[ig_username] + post_hashtag_count if key == ig_username else value for key, value in d.items()} for d in persons_post_hashtag_list]
                        else: 
                            persons_post_hashtag_list.append(dict_post_hashtags_for_person_id)
                    
                elif  "@bubbleroom" in str(row['caption_text']): 
                    posts_count += 1
                    post_mention_count = str(row['caption_text']).count('@bubbleroom')
                
                    dict_posts_for_person_id = {ig_username: posts_count}
                    dict_posts_mentions_for_person_id = {ig_username: post_mention_count}
                    # count the total number of posts made by an influencer 
                    if any(ig_username in d for d in persons_posts_list):
                            persons_posts_list = [{key: posts_count if key == ig_username else value for key, value in d.items()} for d in persons_posts_list]
                    else: 
                            persons_posts_list.append(dict_posts_for_person_id)
                    #count the total number of mentions by an influencer 
                    if any(ig_username in d for d in person_posts_mention_list):
                            person_posts_mention_list = [{key:  d[ig_username] + post_mention_count if key == ig_username else value for key, value in d.items()} for d in person_posts_mention_list]
                    else: 
                            person_posts_mention_list.append(dict_posts_mentions_for_person_id)

                   

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

     
        
        
        return ( persons_posts_list, persons_post_hashtag_list, person_posts_mention_list)
    
 
    def group_by_ig_username(self,data: pd.DataFrame) -> tuple[pd.DataFrame, InfluencerListType, InfluencerListType, InfluencerListType]: 
    # Group the data by 'person_id' 
        influencer_posts,influencer_posts_with_hashtag, influencer_posts_with_mentions = self.__specific_results(data)
       
        return (data,influencer_posts,influencer_posts_with_hashtag, influencer_posts_with_mentions)



    # add columns like posts, post mentions and score
    def add_influencer_score_columns(_, data: pd.DataFrame, influencer_posts: InfluencerListType,influencer_posts_with_hashtag: InfluencerListType, influencer_posts_with_mentions: InfluencerListType ) -> pd.DataFrame: 
        for post in influencer_posts: 
            
            for ig_username in post: 
                
                if ig_username in data['ig_username'].values: 
                    
                        data.loc[data['ig_username'] == ig_username, 'posts'] = post[ig_username]
                        data['posts'] = data['posts'].fillna(0)

        for post in influencer_posts_with_hashtag: 
            
            for ig_username in post: 
                
                if ig_username in data['ig_username'].values: 
                    
                        data.loc[data['ig_username'] == ig_username, 'post hashtags'] = post[ig_username]             
                        data['post hashtags'] = data['post hashtags'].fillna(0)
            
        for post in influencer_posts_with_mentions: 
            
            for ig_username in post: 
                
                if ig_username in data['ig_username'].values: 
                    
                        data.loc[data['ig_username'] == ig_username, 'post mentions'] = post[ig_username]             
                        data['post mentions'] = data['post mentions'].fillna(0)
        
        data['score'] = data['posts'] + data['post hashtags'] + data['post mentions']
        data = data.drop_duplicates(subset='ig_username')
        data.rename(columns={'ig_username': 'influencers'}, inplace=True)

        print("FINAL DATA")
        print(data)
        print("-------------------")
        return data
