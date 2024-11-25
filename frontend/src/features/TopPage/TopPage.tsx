import React, { useState, useEffect } from "react";
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
  const [visibleLeft, setVisibleLeft] = useState<number>(0);
  const [visibleRight, setVisibleRight] = useState<number>(0);
  const [leftFinished, setLeftFinished] = useState<boolean>(false);
  const [mainContentVisible, setMainContentVisible] = useState<boolean>(false);

  const handleLogin = () => {
    navigate("/chat");
  };

  const leftBubbles = [speechBubbleLeft1, speechBubbleLeft2, speechBubbleLeft3, speechBubbleLeft4];
  const rightBubbles = [speechBubbleRight1, speechBubbleRight2, speechBubbleRight3, speechBubbleRight4];

  useEffect(() => {
    // 左側の吹き出しを順番に表示
    const leftInterval = setInterval(() => {
      setVisibleLeft((prev) => {
        if (prev < leftBubbles.length) {
          return prev + 1;
        } else {
          clearInterval(leftInterval);
          setLeftFinished(true);
          return prev;
        }
      });
    }, 300);

    return () => clearInterval(leftInterval);
  }, [leftBubbles.length]);

  useEffect(() => {
    if (leftFinished) {
      // 右側の吹き出しを順番に表示
      const rightInterval = setInterval(() => {
        setVisibleRight((prev) => {
          if (prev < rightBubbles.length) {
            return prev + 1;
          } else {
            clearInterval(rightInterval);
            setTimeout(() => setMainContentVisible(true), 500); // メインコンテンツ表示の遅延
            return prev;
          }
        });
      }, 300);

      return () => clearInterval(rightInterval);
    }
  }, [leftFinished, rightBubbles.length]);

  return (
    <Container
      maxWidth={false}
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
              width: "270px",
              marginLeft: index % 2 === 1 ? "180px" : "40px",
              opacity: visibleLeft > index ? 1 : 0, // フェードイン
              transform: visibleLeft > index ? "translateY(0)" : "translateY(20px)", // 浮き上がり
              transition: "opacity 0.5s ease, transform 0.5s ease",
            }}
          />
        ))}
      </Box>

      {/* メインコンテンツ */}
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          zIndex: 2,
          backgroundColor: "#FFFFFF",
          padding: "24px 40px",
          borderRadius: "24px",
          boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
          opacity: mainContentVisible ? 1 : 0,
          transform: mainContentVisible ? "translateY(0)" : "translateY(20px)",
          transition: "opacity 0.8s ease, transform 0.8s ease",
        }}
      >
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

        <Box display="flex" justifyContent="center" sx={{ marginBottom: 4 }}>
          <Button
            variant="contained"
            startIcon={<Google />}
            size="large"
            sx={{
              borderRadius: 12,
              padding: "14px 28px",
              textTransform: "none",
              fontSize: "18px",
              color: "#EEEEEE",
              backgroundColor: "#393E46",
              "&:hover": {
                backgroundColor: "#222831",
              },
            }}
            onClick={handleLogin}
          >
            Googleでログイン
          </Button>
        </Box>

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
              width: "270px",
              marginLeft: index % 2 === 0 ? "180px" : "40px",
              opacity: visibleRight > index ? 1 : 0,
              transform: visibleRight > index ? "translateY(0)" : "translateY(20px)",
              transition: "opacity 0.5s ease, transform 0.5s ease",
            }}
          />
        ))}
      </Box>
    </Container>
  );
};

export default TopPage;
