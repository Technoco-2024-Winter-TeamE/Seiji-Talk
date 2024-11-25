import React from "react";
import { Typography, Button, Box, Container } from "@mui/material";
import { Google } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import logo from "../../assets/images/logo.png";
import speechBubbleLeft1 from "../../assets/images/speech-bubble-left-1.png"; 
import speechBubbleLeft2 from "../../assets/images/speech-bubble-left-2.png"; 
import speechBubbleLeft3 from "../../assets/images/speech-bubble-left-3.png"; 
import speechBubbleLeft4 from "../../assets/images/speech-bubble-left-4.png"; 
import speechBubbleRight1 from "../../assets/images/speech-bubble-right-1.png";
import speechBubbleRight2 from "../../assets/images/speech-bubble-right-2.png";
import speechBubbleRight3 from "../../assets/images/speech-bubble-right-3.png";
import speechBubbleRight4 from "../../assets/images/speech-bubble-right-4.png";

const TopPage: React.FC = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate("/chat");
  };

  const leftBubbles = [speechBubbleLeft1, speechBubbleLeft2, speechBubbleLeft3, speechBubbleLeft4];
  const rightBubbles = [speechBubbleRight1, speechBubbleRight2, speechBubbleRight3, speechBubbleRight4];

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
      {/* 左側の吹き出し */}
      <Box
        sx={{
          position: "absolute",
          left: 0,
          marginLeft: "40px",
          display: "flex",
          flexDirection: "column",
          gap: 2,
          zIndex: 1,
        }}
      >
        {leftBubbles.map((src, index) => (
          <Box
            key={`left-bubble-${index}`}
            component="img"
            src={src}
            alt={`吹き出し 左 ${index + 1}`}
            sx={{
              width: "270px", // 吹き出しのサイズ
              marginLeft: index % 2 === 1 ? "180px" : "40px", // 2番目と4番目を中心側にずらす
            }}
          />
        ))}
      </Box>

      {/* 中央のコンテンツ */}
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          zIndex: 2,
        }}
      >
        {/* ロゴ */}
        <Box
          component="img"
          src={logo}
          alt="せいじトークロゴ"
          sx={{
            width: "700px",
            marginBottom: 6,
          }}
        />
        <Typography
          variant="h4"
          color="textPrimary"
          sx={{ marginBottom: 4, textAlign: "center" }}
        >
          選挙や政治に対する疑問を、<br />
          1つずつ解決していきましょう。
        </Typography>

        {/* ログインボタン */}
        <Box display="flex" justifyContent="center" sx={{ marginBottom: 4 }}>
          <Button
            variant="contained"
            startIcon={<Google />}
            size="large"
            sx={{
              borderRadius: 12, // ボタンの角を少し丸く
              padding: "14px 28px", // ボタンの内側余白を拡大
              textTransform: "none",
              fontSize: "18px", // フォントサイズを少し大きく
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
      </Box>

      {/* 右側の吹き出し */}
      <Box
        sx={{
          position: "absolute",
          right: 0,
          marginRight: "80px",
          display: "flex",
          flexDirection: "column",
          gap: 2,
          zIndex: 1,
        }}
      >
        {rightBubbles.map((src, index) => (
          <Box
            key={`right-bubble-${index}`}
            component="img"
            src={src}
            alt={`吹き出し 右 ${index + 1}`}
            sx={{
              width: "270px", // 吹き出しのサイズ
              marginLeft: index % 2 === 0 ? "180px" : "40px", // 2番目と4番目を中心側にずらす
            }}
          />
        ))}
      </Box>
    </Container>
  );
};

export default TopPage;
