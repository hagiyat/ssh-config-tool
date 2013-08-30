# coding: utf-8

import os
import json

class SSH_config_generator:

	# 設定初期化
	def __init__(self, app_config_file):
		config_json = self.__get_json_from_file(app_config_file)
		self.__app_config = config_json.get('config')
		self.__base_config = config_json.get('base')

	# jsonファイルリストを生成
	def __get_jsons(self, path):
		return os.listdir(path)

	# jsonファイルからデータを取得
	def __get_json_from_file(self, file_name):
		f = open(file_name)
		data = json.load(f)
		f.close
		return data

	# ベースファイルとマージした結果を返す
	def __merge_to_base(self, in_json_config):
		result = []
		for config in in_json_config:
			tmp = self.__base_config.copy()
			for key, value in config.iteritems():
				tmp[key] = value
			result.append(tmp)
		return result

	# 各ファイルを読んで出力データを生成
	def __make_config(self):
		config_list = []
		files = self.__get_jsons(self.__app_config.get('jsons_path'))
		for file in files:
			try:
				file = self.__app_config.get('jsons_path') + '/' + file
				in_json_config = self.__get_json_from_file(file)
				config_list += self.__merge_to_base(in_json_config)
			except Exception as e:
				print "error: file=%s info=%s" % (file, e.message)

		return config_list

	# ファイル出力
	def __output_config_file(self, config_list):
		output = open(self.__app_config.get('output_file'), 'w')
		for config in config_list:
			# hostとhostnameだけ先頭に持ってくる
			host = config.pop("Host")
			host_name = config.pop("HostName")
			output.write("Host %s\n" % host)
			output.write("  HostName %s\n" % host_name)
			for key, value in config.iteritems():
				output.write("  %s %s\n" % (key, value))

		output.close()

	# 生成処理実行
	def generate(self):
		try:
			config_list = self.__make_config()
			self.__output_config_file(config_list)
			print "設定ファイルの生成に成功しました"
		except Exception as e:
			print e
			print "設定ファイルの生成に失敗しました"


generator = SSH_config_generator('config.json')
generator.generate()

