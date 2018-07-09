import os
import numpy as np
from datetime import timedelta
import time

# global paths
tiramisu_base_dir = '/gpfs/projects/bsc28/tiramisu_semantic_transfer/'
base_imgs_path = tiramisu_base_dir + 'imgs/'

data_path = '/gpfs/projects/bsc28/DATASETS/Imagenet_val50k/ILSVRC_12_val'

imgs = np.load('/gpfs/projects/bsc28/DATASETS/Imagenet_val50k/imagenet2012_val_synset_codes_as_array.npz')['imgs']
synsets = np.load('/gpfs/projects/bsc28/DATASETS/Imagenet_val50k/imagenet2012_val_synset_codes_as_array.npz')['ss']

image_file_paths = '/gpfs/projects/bsc28/tiramisu_semantic_transfer/synset_partitions/'


def create_link(synset_data):
	_path = base_imgs_path + str(synset_data['name']) + '/train/'
	try:
		os.makedirs(_path)
	except:
		pass

	source_target_path = _path

	ss_img_path = os.path.join(source_target_path, str(synset_data['name']))
	no_ss_img_path = os.path.join(source_target_path, 'no_' + str(synset_data['name']))

	try:
		os.makedirs(ss_img_path)
	except:
		pass
	try:
		os.makedirs(no_ss_img_path)
	except:
		pass

	for i in range(len(imgs)):
		img, synset = imgs[i], synsets[i]
		if img in synset_data['imgs']:
			try:
				os.symlink(os.path.join(data_path, img),
				           os.path.join(source_target_path, str(synset_data['name']), img))
			except:
				pass
		else:
			try:
				os.symlink(os.path.join(data_path, img),
				           os.path.join(source_target_path, 'no_' + str(synset_data['name']), img))
			except:
				pass


def create_folders(image_file_paths):
	synset_files = list(os.walk(image_file_paths))[0][2]
	# print(synset_files)
	for file in synset_files[26:]:
		ss_data = np.load(image_file_paths + file)
		print(ss_data['name'])
		create_link(ss_data)
	print('links created :D ')


def main():
	create_folders(image_file_paths)


if __name__ == '__main__':
	init = time.time()
	main()
	print('time:', timedelta(seconds=time.time() - init))