'''
	Author: Henri Tikkala - tikkala.henri@gmail.com
'''
import os
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive

def pydrive_upload(fname):
	gauth = GoogleAuth()
	gauth.LocalWebserverAuth()
	drive = GoogleDrive(gauth)

	#fname = 'smthng-2017_05_09_20:18.jpg'
	
	
	file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
	if len(file_list) == 0:
			folderfile = drive.CreateFile({
				'title' : 'NatureCam_pics',
				'mimeType' : 'application/vnd.google-apps.folder'
			})
			folderfile.Upload()			
			print(folderfile['id'])
		
	#print file_list
	for folderfile in file_list:
		if folderfile['title'] == 'NatureCam_pics':
			id = folderfile['id']
			#print id
		else:
			folderfile = drive.CreateFile({
				'title' : 'NatureCam_pics',
				'mimeType' : 'application/vnd.google-apps.folder'
			})
			folderfile.Upload()			
			#print folderfile['id']

	file1 = drive.CreateFile({'title': fname, 
		"parents":  [{"id": folderfile['id']}]
	})
	file1.SetContentFile(fname)
	file1.Upload() # Files.insert()
	print('Created file %s in GoogleDrive with mimeType %s' % (file1['title'],file1['mimeType']))
	os.remove(fname)
	# Created file with mimeType image

	#file2 = drive.CreateFile({'id': file1['id']})
	#print('Downloading file %s from Google Drive' % file2['title'])
	#file2.GetContentFile('world.png')  # Save Drive file as a local file


#pydrive_upload('smthng-2017_05_09_20:18.jpg')
