##############################################
# This is the python file for Flickr crawling
# Author @ Chia-Hui Liu (GitHub: chiahuiliu)
# the Flickr we are interested: 146634855@N06
##############################################

# import packages
import flickrapi
import json
import pandas as pd
import urllib.request
from progressbar import ProgressBar


def build_connection():
	# This function is used to build the connection and authorization from Flickr
	api_key = ### your api key here ###
	api_secret = ### your api secret here ###
	flickr = flickrapi.FlickrAPI(api_key,api_secret,cache=True)
	return flickr

def check_num_records(flickr, user_accont):
	# check how many records
	page_obj = flickr.photos.search(user_id=user_accont,
                           format='json',
                           extras='url_c',
                           per_page=1)
	page_obj = page_obj.decode('utf8').replace("'", '"')
	page_json = json.loads(page_obj)
	pages = json.dumps(page_json, indent=4, sort_keys=True)
	pages = json.loads(pages)
	total_records = pages['photos']['pages']
	return total_records

def get_record_info(flickr, user_accont, p):
	'''
	This is used to get all record information
	'''
	obj = flickr.photos.search(user_id=user_accont, format='json', extras='url_c', per_page=500, page=p)
	obj = obj.decode('utf8').replace("'", '"')
	data = json.loads(obj)
	res = json.dumps(data, indent=4, sort_keys=True)
	res = json.loads(res)
	return res

def process_results(res):
    photo_list = res['photos']['photo']
    res_list=[]
    for each_dict in photo_list:
        res_list.append([each_dict.get('id'),
        each_dict.get('title'),
        each_dict.get('url_c')
        ])

    df = pd.DataFrame(res_list, columns=['id', 'title', 'url'])
    # print(df.sample(5))
    return df

def concat_brief_df(big_df,df):
    big_df = big_df.append(df, ignore_index=True)
    return big_df

def download_photos(record_info_df):
	pbar = ProgressBar()
	for i in pbar(range(len(record_info_df))):
		filename = record_info_df['id'].loc[i]
		try:
			f = open('results/'+str(filename)+'.jpg', 'wb')
			f.write(urllib.request.urlopen(record_info_df['url'].loc[i]).read())
			f.close()
		except:
			print(str(i) + ": no url")


if __name__ == "__main__":
	'''
	Step 1. Connect and get authorization of Flickr, and get the brief metadata
	'''
	print("Building and asking authorization...")
	flickr = build_connection()
	print("Getting record counts....")
	records = check_num_records(flickr, '146634855@N06')
	total_page = int(records/500)+1
	print("Getting record information...")

	# Here, the variable record_info contains the id, title, and the link
	record_info_df = pd.DataFrame(columns=['id', 'title', 'url'])

	pbar1 = ProgressBar()
	for per_page in pbar1(range(total_page)):
		temp_df = process_results(get_record_info(flickr, '146634855@N06', per_page))
		record_info_df = concat_brief_df(record_info_df, temp_df)

	print(record_info_df.head(20))
	# save the resutls to csv file
	record_info_df.to_csv('flickr_brief_record.csv', index=False)
	'''
	Step 2. Download all the pictures
	'''
	download_photos(record_info_df)
	'''
	Step 3. Get informative data
	'''
