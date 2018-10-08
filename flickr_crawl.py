##############################################
# This is the python file for Flickr crawling
# Author @ Chia-Hui Liu (GitHub: chiahuiliu)
##############################################

# import packages
import flickrapi
import json
import pandas as pd
import urllib.request

def build_connection():
	# This function is used to build the connection and authorization from Flickr
	api_key = ### your api key here ###
	api_secret = ### your api secret here ###
	flickrapi = flickrapi.FlickrAPI(api_key,api_secret,cache=True)
	return flickrapi


res_cols = ['photo_id', 'height', 'width', 'owner', 'ispublic',
	'isfriend', 'isfamily', 'secret', 'server', 'title', 'url']

big_df = pd.DataFrame(columns=res_cols)

def flickr_search(keyward,p):
    print("Searching public photos...")
    obj = flickr.photos.search(user_id=keyward,
                           format='json',
                           extras='url_c',
                           per_page=500,
                           page =p
                           )
    obj = obj.decode('utf8').replace("'", '"')
    #print(obj)
    print("Converting results...")
    data = json.loads(obj)
    res = json.dumps(data, indent=4, sort_keys=True)
    res = json.loads(res)
    return res

def process_results(res):
    photo_list = res['photos']['photo']
    print("Processing results: " + str(len(photo_list)) + " in total...")
    res_list=[]
    for each_dict in photo_list:
        res_list.append([each_dict.get('id'),
        each_dict.get('height_c'),
        each_dict.get('width_c'),
        each_dict.get('owner'),
        each_dict.get('ispublic'),
        each_dict.get('isfriend'),
        each_dict.get('isfamily'),
        each_dict.get('secret'),
        each_dict.get('server'),
        each_dict.get('title'),
        each_dict.get('url_c')
        ])

    df = pd.DataFrame(res_list, columns=['photo_id', 'height', 'width', 'owner', 'ispublic', 'isfriend', 'isfamily', 'secret', 'server', 'title', 'url'])
    # print(df.sample(5))
    return df

def concat_df(big_df,df):
    big_df = big_df.append(df, ignore_index=True)
    return big_df


for i in range(1,8):
    print("=======page "+ str(i)+"========")
    temp_df = process_results(flickr_search('146634855@N06', i))
    big_df = concat_df(big_df, temp_df)

def get_photo_info(each_photo_id):
    crawl_info_res = []
    print("Getting photo Info...")
    obj = flickr.photos.getInfo(photo_id=each_photo_id, format='json')
    obj = obj.decode('utf8').replace("'", '"')
    data = json.loads(obj)
    res = json.dumps(data, indent=4, sort_keys=True)
    res = json.loads(res)
    crawl_info_res.append(res)
    return crawl_info_res

def process_PhotoInfo_res(crawl_info_res):
	photo_dict = res['photo']

	return res_df

def concat_final_df(temp_df, final_df):
    final_df = final_df.append(temp_df, ignore_index=True)

final_df = pd.DataFrame(columns=['comments',
                                'dates_lastupdate',
                                'dates_posted',
                                'dates_taken',
                                'dates_takengranularity',
                                'dates_takenunknown',
                                'dateuploaded',
                                'description',
                                'editability_canaddmeta',
                                'editability_cancomment',
                                'farm',
                                'geoperms_iscontact',
                                'geoperms_isfamily',
                                'geoperms_isfriend',
                                'geoperms_ispublic',
                                'id',
                                'isfavorite',
                                'license',
                                'location_context',
                                'location_country',
                                'location_county',
                                'location_city', #locality
                                'location_region',
                                'location_latitude',
                                'location_longitude',
                                'location_neighbourhood',
                                'media_type', # media
                                'notes',
                                'originalformat',
                                'originalsecret',
                                'owner_id',
                                'owner_realname',
                                'owner_username',
                                'has_people',
                                'public_editability_canaddmeta',
                                'public_editability_cancomment',
                                'rotation',
                                'safety_level',
                                'secret',
                                'server',
                                'tags',
                                'title',
                                'url',
                                'right_canblog',
                                'right_candownload',
                                'right_canprint',
                                'right_canshare',
                                'view_count',
                                'visibility_isfamily',
                                'visibility_isfriend',
                                'visibility_ispublic'
                                ])

for each_photo_id in list(big_df.photo_id.astype(str))[:3]:
	(get_photo_info(each_photo_id))
