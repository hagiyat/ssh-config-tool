# coding: utf-8

import os, json

class SSH_config_generator:

	# 設定初期化
	def __init__(self, app_config_file):
		config_json = self.__get_json_from_file(app_config_file)
		self.__app_config = config_json.get('config')
		self.__base_config = config_json.get('base')


	# jsonファイルからデータを取得
	def __get_json_from_file(self, file_name):
		f = open(file_name)
		data = json.load(f)
		f.close
		return data

	# 各ファイルを読んで出力データを生成
	def __get_config(self):
		files = os.listdir(self.__app_config.get('jsons_path'))
		for file in files:
			yield self.__get_config_from_file(file)

	# ファイルから書き込む情報を取得
	def __get_config_from_file(self, file):
		file = self.__app_config.get('jsons_path') + '/' + file
		in_json_config = self.__get_json_from_file(file)
		return self.__merge_to_base(in_json_config)

	# ベースファイルとマージした結果を返す
	def __merge_to_base(self, in_json_config):
		#result = []
		for config in in_json_config:
			merged_config = self.__base_config.copy()
			merged_config.update(config)
			yield merged_config

	# ファイル出力
	def __output_config_file(self, output, merged_config_generator):
		# hostとhostnameだけ先頭に持ってくる
		for config in merged_config_generator:
			host = config.pop("Host")
			host_name = config.pop("HostName")
			output.write("Host %s\n" % host)
			output.write("  HostName %s\n" % host_name)
			for key, value in config.iteritems():
				output.write("  %s %s\n" % (key, value))

	# 生成処理実行
	def generate(self):
		try:
			output = open(self.__app_config.get('output_file'), 'w')
			config_generator = self.__get_config()
			for merged_config_generator in config_generator:
				self.__output_config_file(output, merged_config_generator)
			output.close()
			print "設定ファイルの生成に成功しました"

		except Exception as e:
			print e
			print "設定ファイルの生成に失敗しました"


generator = SSH_config_generator('config.json')
generator.generate()

