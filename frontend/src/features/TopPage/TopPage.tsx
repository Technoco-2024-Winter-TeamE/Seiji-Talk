import React from "react";
import { Typography, Button, Box, Paper, Container } from "@mui/material";
import { Google } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import logo from "../../assets/images/logo.png";

const TopPage: React.FC = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate("/chat");
  };

  return (
    <Container
      maxWidth={false} // 横幅を画面いっぱいに広げる
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        backgroundColor: "background.default",
        padding: 4,
        position: "relative",
      }}
    >
      {/* 吹き出し (左) */}
      <Paper
        elevation={3}
        sx={{
          position: "absolute",
          left: "10%",
          top: "20%",
          padding: 2,
          maxWidth: 300,
          backgroundColor: "#e3f2fd",
          borderRadius: "16px",
          "&:before": {
            content: '""',
            position: "absolute",
            top: "50%",
            left: "-10px",
            width: 0,
            height: 0,
            borderStyle: "solid",
            borderWidth: "10px 10px 10px 0",
            borderColor: "transparent #e3f2fd transparent transparent",
          },
        }}
      >
        <Typography variant="body1" fontWeight="bold" color="#1e88e5">
          「現在の総理大臣は誰？」
        </Typography>
        <Typography variant="body2" color="textSecondary">
          最新情報モードで調べると...
        </Typography>
      </Paper>

      {/* 吹き出し (右) */}
      <Paper
        elevation={3}
        sx={{
          position: "absolute",
          right: "10%",
          top: "40%",
          padding: 2,
          maxWidth: 300,
          backgroundColor: "#f3e5f5",
          borderRadius: "16px",
          "&:before": {
            content: '""',
            position: "absolute",
            top: "50%",
            right: "-10px",
            width: 0,
            height: 0,
            borderStyle: "solid",
            borderWidth: "10px 0 10px 10px",
            borderColor: "transparent transparent transparent #f3e5f5",
          },
        }}
      >
        <Typography variant="body1" fontWeight="bold" color="#8e24aa">
          「与党って何？」
        </Typography>
        <Typography variant="body2" color="textSecondary">
          用語解説モードで確認しましょう！
        </Typography>
      </Paper>

      {/* ヘッダー部分 */}
      <Box
        component="img"
        src={logo} // ロゴ画像を指定
        alt="せいじトークロゴ"
        sx={{
          width: "400px", // ロゴの幅を調整
          marginBottom: 2,
        }}
      />
      <Typography
        variant="h5"
        color="textPrimary"
        sx={{ marginBottom: 4, textAlign: "center" }}
      >
        選挙・政治に対する疑問を、1つずつ解決していきましょう。
      </Typography>

      {/* ログインボタン */}
      <Box display="flex" justifyContent="center">
        <Button
          variant="contained"
          startIcon={<Google />}
          size="large"
          sx={{
            borderRadius: 8,
            padding: "10px 20px",
            textTransform: "none",
            fontSize: "16px",
            color: "#EEEEEE",
            backgroundColor: "#393E46",
            "&:hover": {
              backgroundColor: "#222831", // ホバー時の背景色
            },
          }}
          onClick={handleLogin}
        >
          Googleでログイン
        </Button>
      </Box>

      {/* フッター */}
      <Typography
        variant="body2"
        color="textPrimary"
        sx={{ marginTop: 4, textAlign: "center" }}
      >
        © 2024 せいじトーク All Rights Reserved.
      </Typography>
    </Container>
  );
};

export default TopPage;
