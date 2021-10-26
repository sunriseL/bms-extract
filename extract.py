import os
import argparse
import re
import shutil
from tqdm import tqdm
from sys import exit
import subprocess


def question(prompt):
	ans = ""
	while ans != "y" and ans != "n":
		ans = input("{} [Y|n] ".format(prompt)).lower()
	if ans == "y": return True
	else: return False


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--directory", help="存放BMS工程以及切音的目录")
	parser.add_argument("-o", "--output_directory", help="导出目录（相对于工程目录）")
	parser.add_argument("-f", "--file", help="指定的BMS工程（相对于工程目录）")
	parser.add_argument("--oggenc", help="oggenc.exe的位置")
	args = parser.parse_args()

	''' 初始化导出参数 '''
	is_convert2ogg = False
	is_output_unused_file = False

	dir = args.directory if args.directory else "."
	oggenc = args.oggenc if args.oggenc else "oggenc.exe"

	print("工作目录：{}".format(dir))

	while True:
		try:
			files = os.listdir(dir)
			if args.file:
				if not os.path.exists(os.path.join(dir, args.file)):
					print("错误: 文件 {} 并不存在".format(os.path.join(dir, args.file)))
					raise Exception()
				bms_file = args.file

			else:
				bms_files = [file for file in files if file.endswith(".bms")]
				if len(bms_files) == 0:
					# print("错误: 目录 {} 并不包含BMS工程文件".format(dir))
					raise Exception("错误: 目录 {} 并不包含BMS工程文件".format(dir))
					raise Exception()

				if len(bms_files) > 1:
					print("错误：在目录 {} 内找到了{}个BMS工程文件:".format(dir, len(bms_files)))
					raise Exception()
				else:
					bms_file = bms_files[0]
		except Exception as e:
			print(e)
			dir = input("目录 {} 无法进行操作，请重新输入目录：".format(dir))
		else:
			break

	print("确认BMS工程文件: {}".format(os.path.join(dir, bms_file)))

	with open(os.path.join(dir, bms_file), "r") as f:
		lines = f.readlines()
	wav_lines = [line for line in lines if "WAV" in line]
	wav_dic = {}
	for line in wav_lines:
		v = line.strip().split(" ")[1]
		k = line[4:6]
		wav_dic[k] = v

	data_set = set()
	for line in lines:
		m = re.match("^#\d{3}01:", line)
		if m:
			data = line.strip().split(":")[1]
			datum = re.findall('.{2}', data)
			for data in datum:
				if data == "00": continue
				data_set.add(data) 

	unused_wavs = [wav_dic[i] for i in wav_dic if not i in data_set]
	print("发现以下文件被导入进BMS工程文件但未被使用：{}".format(",".join(unused_wavs)))
	is_output_unused_file = question("是否一起导出？")

	data_set = data_set if is_output_unused_file else wav_dic.keys()

	wavs = [wav_dic[key] for key in data_set if wav_dic[key].endswith("wav")]
	if len(wavs) > 0:
		if os.path.exists(oggenc): 
			is_convert2ogg = question("发现存在wav文件，是否转换为ogg文件导出？（同时更新BMS工程文件）")
		else:
			print("警告: 发现存在wav文件但未发现oggenc.exe，因此无法进行转换")

	output_directory = args.output_directory if args.output_directory else "extract"

	print("导出目录：{}".format(os.path.join(dir, output_directory)))
	if not os.path.exists(os.path.join(dir, output_directory)): os.mkdir(os.path.join(dir, output_directory))

	
	for data in tqdm(data_set, desc="导出进度"):
		input_filename = wav_dic[data]
		if is_convert2ogg: output_filename = ".".join([input_filename[:input_filename.find(".")], "ogg"])
		else: output_filename = input_filename

		if os.path.exists(os.path.join(dir, output_directory, output_filename)): continue

		input_file_path = os.path.join(dir, input_filename)
		output_file_path = os.path.join(dir, output_directory, output_filename)



		if is_convert2ogg and input_filename.endswith(".wav"): 
			subprocess.run("{} {} -q10 -o {}".format(oggenc, input_file_path, output_file_path), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		else: shutil.copy(input_file_path, output_file_path)
	
	if is_convert2ogg:
		with open(os.path.join(dir, output_directory, bms_file), "w") as f:
			for line in lines:
				if "WAV" in line:
					line = line.replace(".wav", ".ogg")
				f.write(line)
	else: shutil.copy(os.path.join(dir, bms_file), os.path.join(dir, output_directory))
	




if __name__ == "__main__":
	main()
