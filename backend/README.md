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
sudo systemctl status mysql

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

パスワード認証に切り替え
以下のコマンドで認証方式を変更し、パスワードを設定します。


ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;
YourSecurePassword の部分を、好きなものに変更してください・

パスワード認証が有効になったか確認します。

SELECT user, host, plugin FROM mysql.user WHERE user = 'root';

その後のログイン方法

mysql -u root -p

##  初回セットアップ


#ここからはターミナル1で

プロジェクトディレクトリに移動 Flaskプロジェクトのディレクトリに移動します。

cd /path/to/your/project

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

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
CREATE DATABASE Seiji_talk CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

注意！config.pyのURLは変更して下さい（ユーザ名・password・データベース名）

# データベースのマイグレーションを実行
flask db upgrade

# Flaskアプリケーションを起動
python app.py



# MySQLサービスを停止する(データサーバー側で)

sudo systemctl stop mysql


↓これはいらんかな

初期化: flask db init
マイグレーション生成: flask db migrate -m "Initial migration"

-- ユーザーの作成
CREATE USER 'flask_user'@'localhost' IDENTIFIED BY 'password';

-- 権限の付与
GRANT ALL PRIVILEGES ON unko.* TO 'flask_user'@'localhost';
FLUSH PRIVILEGES;