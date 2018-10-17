# UT-PCL-Flickr
This is the repository for Flickr project for UT PCL Scholar catalog

## Goal
For the Flickr Crawling project, we are interested in crawling all the image metadata such as photos, descriptions, dates, etc. to have further insights on the specific Flickr account - University of Texas Biodiversity Collections. We corporate with the University of Texas Biodiversity Collections to help them get more data insights on their Flickr account, and also build a catalog for UT Libraries.

## Process
### Prerequisites
1. Required Python packages
  - flickrapi
  - json
  - urllib
  - lxml
  - xml
2. Flickr key and secret
To be legally authorized to crawl the information on Flickr, you’ll need Flickr key and secret. The following steps are the way you obtain your Flickr key and secret. Please sign in to Flickr before you get started.
  - Go to [The app garden](https://www.flickr.com/services/api/misc.api_keys.html) on Flickr.
  - Click on `Apply for your key online now`.
  - There are non-commercial/commercial keys for you to choose, please choose the one that applies the best to you. (In this project, I used a non-commercial key as we are not making money on it.)
  - Fill out all the information and then click on `SUBMIT` button.
  - Now you’ll see the key and secret have been generated for you. Please copy the key and secret you’ve got from Flickr.

### Code
Function explanations (sorted according to the squence of use)
1. `build_connection()`: used to build the connection and authorization from Flickr
2. `check_num_records()`: check how many records for the specific Flickr account
3. `get_record_info()`: get the brief record info (for the purpose of downloading)
4. `process_results()`: used to get photo's id, title, and url
5. `concat_brief_df()`: convert all the results into a big pandas DataFrame (columns: id, title, url)
6. `download_photos()`: download photos and set id as the filename
7. `get_meta()`: get meta information for each photo
8. `process_meta()`: convert meta results into pandas dataframe
9. 

## Results
1. Photos: We are able to download all the photos under the account “University of Texas Biodiversity Collection” on Flickr. 
2. Image metadata has 39 columns, the ordering also corresponds to the columns in the csv.
(If you want to check the results, please contact Colleen Lyon(c.lyon@austin.utexas.edu) for permission.

### Explanations for the columns
#### The basic info
- `id`: The unique sequence number of the specific photo
- `title`: The title of the image
- `url`: The link to the image
#### Owner Info
- `owner_id`: The unique sequence number of the owner of the photo.
- `owner_realname`: The real name of the owner (University of Texas Biodiversity Collections)
- `owner_username`: The username stored in Flickr (Waller Creek Working Group)
#### Photo Information
- `description`: Photo description
- `notes`: If there is, it’s the noted added by its owner
- `comments`: Comments of the photo
- `tags`: Tags of the photo
- `media_type`: The media type of the results, in this case, all are “photo”
- `original_format`: The original type of file, in this case, all are “jpg”
- `rotation`: How many degrees rotated, e.g. 0 if not being rotated, 90 means the file was rotated by 90 degrees clockwise
#### Dates (All the format of the dates are YYYY-MM-DD HH-MM-SS)
- `dates_taken`: The date of the image was taken
- `dates_posted`: The date of the image was posted on Flickr
- `date_uploaded`: The date of the image was FIRST uploaded on Flickr
- `dates_lastupdate`: The last updated date on Flickr
- `dates_takengranularity`: The accuracy to which we know the date to be true. At present, the following granularities are used:

| Code     | Format |
| :---:      | :---:       |
| 0 | Y-m-d H:i:s         |
| 4     | Y-m        |
| 6 | Y         |
| 8     | Circa…        |
- `dates_takenunknown`: In Boolean format, TRUE if the dates of the photo is unknown, otherwise, they should be FALSE
#### Stats
- `view_count`: The count of how many times the image was viewed on Flickr
- `isfavorite`: Which will tell you if the currently authenticated user has marked the photo as a favorite
#### Location
- `location_country`: The country of the photo taken, e.g. United States
- `location_region`: The region of the photo taken, e.g. Texas
- `location_county`: The county of the photo taken e.g. Travis
- `location_city`: The county of the photo taken e.g. Austin
- `location_latitude`: The latitude of the photo taken
- `location_longitude`: The longitude of the photo taken
- `location_neighbourhood`: The nearby place of the photo taken e.g. Hyde Park, University of Texas-Austin
- `location_context`: The context of the location. Unfortunately, all the data in this project does not have this information
#### License & Authorization
- `editability_canaddmeta`: In Boolean format, whether the data can be added with metadata under authorized permission of edition
- `editability_cancomment`: In Boolean format, whether the data can be added comments under authorized permission of edition
- `public_editability_canaddmeta`: In Boolean format, whether the data can be added with metadata by the public
- `safety_level`: The safety level of the image (original code: 0 for safe, 1: moderate, 2 for restricted, the final results has been converted to string format for reader-friendly purpose)
- `right_canblog`: Whether or not you can put the media for public distribution purpose, such as blog
- `right_candownload`: Whether or not you can download the media
- `right_canprint`: Whether or not you can print out the media
- `right_canshare`: Whether or not you can share the media in public
- `license`: The license of the image, below is the table for the original code and corresponding type of license. For reader-friendly purpose, I’ve converted the code to textual format.

| Original Code     | License |
| :---:      | :---       |
| 0 | All Rights Reserved        |
| 1 | [Attribution-NonCommercial-ShareAlike License](https://creativecommons.org/licenses/by-nc-sa/2.0/)  |
| 2 | [Attribution-NonCommercial License](https://creativecommons.org/licenses/by-nc/2.0/)    |
| 3 | [Attribution-NonCommercial-NoDerivs License](https://creativecommons.org/licenses/by-nc-nd/2.0/)    |
| 4 |[Attribution License](https://creativecommons.org/licenses/by/2.0/)    |
| 5 |[Attribution-ShareAlike License](https://creativecommons.org/licenses/by-sa/2.0/)     |
| 6 | [Attribution-NoDerivs License](https://creativecommons.org/licenses/by-nd/2.0/)       |
| 7 | [No known copyright restrictions](https://www.flickr.com/commons/usage/)       |
| 8 | [United States Government Work](http://www.usa.gov/copyright.shtml)  |
| 9 | [Public Domain Dedication (CC0)](https://creativecommons.org/publicdomain/zero/1.0/)       |
| 10 | [Public Domain Mark](https://creativecommons.org/publicdomain/mark/1.0/)       |
