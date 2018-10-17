##############################################
# This is the python file for Flickr crawling
# Author @ Chia-Hui Liu (GitHub: chiahuiliu)
# the Flickr we are interested: 146634855@N06
#!/usr/bin/env python3
##############################################

# import packages
import flickrapi
import json
import pandas as pd
import numpy as np
import urllib.request
from progressbar import ProgressBar


def build_connection():
	'''
	This function is used to build the connection and authorization from Flickr
	'''
	api_key = ### your api key here ###
	api_secret = ### your api secret here ###
	flickr = flickrapi.FlickrAPI(api_key,api_secret,cache=True)
	return flickr

def check_num_records(flickr, user_accont):
	'''
	check how many records
	'''
	page_obj = flickr.photos.search(user_id=user_accont, format='json', extras='url_c',per_page=1)
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
	'''
	Used to get photo's id, title, and url
	'''
	photo_list = res['photos']['photo']
	res_list=[]
	for each_dict in photo_list:
		res_list.append([each_dict.get('id'), each_dict.get('title'), each_dict.get('url_c')])
	df = pd.DataFrame(res_list, columns=['id', 'title', 'url'])
	return df

def concat_brief_df(big_df,df):
	'''
	concat results
	'''
	big_df = big_df.append(df, ignore_index=True)
	return big_df

def download_photos(record_info_df):
	'''
	Download photos and set id as the filename
	P.S. The reason why I'm not taking title as the filename is that title is not unique.
	'''
	pbar = ProgressBar()
	for i in pbar(range(len(record_info_df))):
		filename = record_info_df['id'].loc[i]
		try:
			f = open('results/'+str(filename)+'.jpg', 'wb')
			f.write(urllib.request.urlopen(record_info_df['url'].loc[i]).read())
			f.close()
		except:
			print(str(i) + ": no url")

def get_meta(each_photo_id):
	crawl_info_res = []
	obj = flickr.photos.getInfo(photo_id=each_photo_id, format='json')
	obj = obj.decode('utf8').replace("'", '"')
	data = json.loads(obj)
	res = json.dumps(data, indent=4, sort_keys=True)
	res = json.loads(res)
	crawl_info_res.append(res)
	return crawl_info_res

def process_meta(each_meta):
	'''
	Convert crawled results to pandas dataframe
	'''
	meta_dict = dict(each_meta['photo'])
	revised_dict = {}
	temp_res = []
	for k,v in meta_dict.items():
		if isinstance(v,dict):
			for k1, v1 in v.items():
				if isinstance(v1,dict):
					for k2, v2 in v1.items():
						if '_' in k2 and '_' in k1:
							temp_key = str(k+k1+k2)
						elif '_' in k2 and '_' not in k1:
							temp_key = str(k+'_'+k1+k2)
						else:
							temp_key = str(k+'_'+k1+'_'+k2)
						revised_dict[temp_key] = v2
				elif isinstance(v1,list):
					if len(v1)>0:
						dict_v1 = dict(v1[0])
						for k2, v2 in dict_v1.items():
							if '_' in k2 and '_' in k1:
								temp_key = str(k+k1+k2)
							elif '_' in k2 and '_' not in k1:
								temp_key = str(k+'_'+k1+k2)
							else:
								temp_key = str(k+'_'+k1+'_'+k2)
							revised_dict[temp_key] = v2
					else:
						temp_key = str(k+'_'+k1)
						revised_dict[temp_key] = ''
				elif '_' in k1:
					temp_key = str(k+k1)
					revised_dict[temp_key] = v1
				else:
					temp_key = str(k+'_'+k1)
					revised_dict[temp_key] = v1
		else:
			revised_dict[k] = v
	columns_list = list(revised_dict.keys())
	values = ([str(x) for x in revised_dict.values()])
	temp_df = pd.DataFrame(values)
	# transpose
	temp_res_df = temp_df.T
	temp_res_df.columns = columns_list
	return temp_res_df

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

	# save the resutls to csv file
	record_info_df.to_csv('flickr_brief_record.csv', index=False)
	'''
	Step 2. Download all the pictures
	'''
	# download_photos(record_info_df)
	'''
	Step 3. Get informative data
	'''
	crawl_meta = []
	final_res = pd.DataFrame()
	for per_id in (range(len(record_info_df))):
		crawl_meta.append(get_meta(record_info_df['id'].loc[per_id]))
	for each_meta in crawl_meta:
		temp_df = process_meta(each_meta[0])
		if len(final_res) < 1:
			final_res = temp_df
		else:
			final_res = pd.concat([final_res,temp_df])
	final_res.to_csv('final_flickr_results_v5.csv', ignore_index=True)
