.ssh/configを分割管理する
=======================

 - pythonの練習

 - sshの接続先が多くなってきたので、分割管理できるようにした

使い方
------

 - hosts以下にjsonでホストの設定を書く

 最低限、HostとHostNameだけ書けばOK。
 足りない分はconfig.jsonで補う

 - python make_ssh_config.py

 - できあがったconfigを、.ssh/configにコピー


直近の予定
-----

 - hostsに追加するjsonを、どこかのホストにお邪魔して検索・生成する仕組みを作る

できた！
-----

 - jsonファイルを走査してファイルに書き込む処理をyieldで作る
