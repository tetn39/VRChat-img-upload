@echo off

:: 文字コード変更
chcp 65001


:: 仮想環境作るマン
echo 仮想環境無かったら作るよ(すでにあるなら大丈夫!)
python -m venv venv

:: 仮想環境をアクティベート
call venv\Scripts\activate

:: 必要なライブラリをインストール
echo ライブラリ無かったらインストールするよ
pip install -r requirements.txt

:: Pythonコードを実行
chcp 65001
echo bot起動するよ
python main.py

:: 仮想環境を終了
deactivate
