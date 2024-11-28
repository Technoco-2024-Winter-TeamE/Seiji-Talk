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
-H "Authorization: Bearer ya29.a0AeDClZByXIM3DY67QxV56Wig48IdA8yNnLIjEyrJXpKpfhu03wHwAFj_hO6jGbe1zGAnGDQyT4tXYkxP9QFM68C6L-PzyPY3xnrLDccWhLMQCN47mzgOoZ_CN5X7AwUAj-dUTevgq0pVkHpaySZfTv65Kp7DMqJwvzwaCgYKAWsSARMSFQHGX2Mi366wEt4SPhYlWTaDhQyUyw0170" \
--insecure \
-d '{
    "message": "徳島県知事はだれですか",
    "mode": "latest"
}'



curl -X GET https://localhost:5000/api/questions/b3658dba-e9e7-4d44-851b-466ea45b810e \
-H "Content-Type: application/json" \
-H "Authorization: Bearer ya29.a0AeDClZBpWI7BP2dCXjcX2xGUzwFE707eXmWxvJ5VEA5TxCK5pyva2bAAagd076K1YNXxW_jtMPLyfxnfhXz0hBrew-s2g0k7h86PJaHSGBWaaTHpYxNGs0D0IJTmEc0IniFQuXDdVltoaqOW3yVVpgJEp5l1raXF9jgaCgYKAQcSARMSFQHGX2MiX5ku1HCSJhshpR-pLaW5DQ0170" \
--insecure 



curl -X POST https://localhost:5000/api/questions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer " \
--insecure \
-d '{
    "message": "直接請求権について教えて",
    "mode": "word"
}'


curl -X GET "https://localhost:5000/api/questions/history?offset=0&limit=4" -H "Authorization: Bearer ya29.a0AeDClZBpWI7BP2dCXjcX2xGUzwFE707eXmWxvJ5VEA5TxCK5pyva2bAAagd076K1YNXxW_jtMPLyfxnfhXz0hBrew-s2g0k7h86PJaHSGBWaaTHpYxNGs0D0IJTmEc0IniFQuXDdVltoaqOW3yVVpgJEp5l1raXF9jgaCgYKAQcSARMSFQHGX2MiX5ku1HCSJhshpR-pLaW5DQ0170" --insecure