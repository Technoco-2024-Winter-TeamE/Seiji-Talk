# Flask アプリケーションのセットアップと起動手順

## 必要環境
- **Python**: バージョン3.10以上推奨
- **ツール**: `pip`, `virtualenv`, `curl`, `jq`
- **データベース**: MySQL
---


## MySQLのインストール

アプリケーションでMySQLを使用するため、ローカルマシンにMySQLサーバーをインストールしてください。

### **Linuxの場合**
```bash
sudo apt update
sudo apt install mysql-server


MySQLサービスを起動
sudo systemctl start mysql
#　できなければこっちで
sudo service mysql start

状態の確認（activeか）
sudo systemctl status mysql
sudo service mysql status


mysql_secure_installationを使用して、MySQLの初期設定を行います。


sudo mysql_secure_installation

設定内容の例:
rootパスワードの設定: 推奨される強力なパスワードを設定。
匿名ユーザー削除: y
リモートログインの無効化: y
テストデータベースの削除: y
設定変更の反映: y

MySQLにログイン
以下のコマンドでMySQLにログインします。

sudo mysql -u root -p

#　おそらくそのままenterで通る

パスワード認証に切り替え
以下のコマンドで認証方式を変更し、パスワードを設定します。


ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;
password の部分を、好きなものに変更してください・

パスワード認証が有効になったか確認します。

SELECT user, host, plugin FROM mysql.user WHERE user = 'root';

その後のログイン方法

mysql -u root -p

## 


## Google認証のキー取得

google_config.jsonをダウンロード
OPENAI_API_KEYをvenvの環境変数に登録



##  初回セットアップ


#ここからはターミナル1で

プロジェクトディレクトリに移動 Flaskプロジェクトのディレクトリに移動します。

cd /path/to/your/project

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
source venv/bin/activate  
# Windowsの場合: venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt



##(3) データベースとユーザーを作成
#以下のコマンドを入力してください。各コマンドの後にEnterを押します。

MySQLサービスを起動（起動してなければ）
sudo systemctl start mysql

MySQLサービスの確認
sudo systemctl status mysql

データベースに接続
mysql -u root -p

-- データベースの作成
CREATE DATABASE Seiji_Talk CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

# 注意！config.pyのURLは変更して下さい（ユーザ名・password・データベース名）
# OpenAIのAPIキーをvenv環境の環境変数として入れておいてください


# データベースのマイグレーションを実行

flask db upgrade

# Flaskアプリケーションを起動
python app.py


# MySQLサービスを停止する(データサーバー側で)

sudo systemctl stop mysql


↓これはいらんかな

初期化: 
flask db init
マイグレーション生成: 
flask db migrate -m "Initial migration"

-- ユーザーの作成
CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'password';

-- 権限の付与
GRANT ALL PRIVILEGES ON unko.* TO 'flask_user'@'localhost';
FLUSH PRIVILEGES;


-- データベースの削除
SHOW DATABASES;
DROP DATABASE データベース名;


動作確認用

curl -X POST https://localhost:5000/api/questions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ya29.a0AeDClZA6Xt-aqioIlLDIvIRIOxCZFrVReP1Gg-fUbHA1CCpi-L7b-V5SlVLu4o0HRzdrZlVp7YjDIsz-4TlzJqs16mlRIYc98aPHQFjUQkgjEXtOomQEUMMaiPjf7kChmo183L9OxQHD70pf0n9YDbQT7X8Zc9HURS0aCgYKAXkSARMSFQHGX2Mi2pAettyBlVyfrnddcpZmWQ0170" \
--insecure \
-d '{
    "message": "このAPIの動作確認をしたい。",
    "mode": "word"
}'



curl -X GET https://localhost:5000/api/questions/8126940e-ea96-4567-b26f-f3490c66dc01 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ya29.a0AeDClZA6Xt-aqioIlLDIvIRIOxCZFrVReP1Gg-fUbHA1CCpi-L7b-V5SlVLu4o0HRzdrZlVp7YjDIsz-4TlzJqs16mlRIYc98aPHQFjUQkgjEXtOomQEUMMaiPjf7kChmo183L9OxQHD70pf0n9YDbQT7X8Zc9HURS0aCgYKAXkSARMSFQHGX2Mi2pAettyBlVyfrnddcpZmWQ0170" \
--insecure 



curl -X POST https://localhost:5000/api/questions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ya29.a0AeDClZDsuK67XFWoMAW1Xn89U-elS7xBo_ptZjSgF3uY7wWdfbuS2v-XOIyPkdqMpn6Fc58UbIdVL9ZAGNZhFKaCddhwZU7eWPvsCeynUwtRu1z468V93inVVeuJ6OGqtmRaO7Ocl_reb9YvacQW6Te3Rix6IU4wTYEaCgYKAc0SARMSFQHGX2Misn-N7YbQOBjg7khiePvY0Q0170" \
--insecure \
-d '{
    "message": "直接請求権について教えて",
    "mode": "word"
}'


curl -X GET "https://localhost:5000/api/questions/history?offset=0&limit=4" -H "Authorization: Bearer ya29.a0AeDClZA1cwGtMPZueaJlDnyzsUIwOFsg-H5zh40cURYLAmov1t3zcDdoe3fURbaarU0T12p8PZXpqwipmxkepeqQ1IddGU8NplMKkqjs7s5qp8DCujTMLaUAVcYpRpga3EhKtSz3Tn3xI09_77P51aRQgX6mPRS99w8aCgYKAaUSARMSFQHGX2Mi8X3Wks4UUM35v_2X3Mc9WQ0170" --insecure