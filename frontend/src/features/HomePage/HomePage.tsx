import React from "react";
import { Container, Typography, Button, Box } from "@mui/material";
import { Link } from "react-router-dom";

const HomePage: React.FC = () => {
  return (
    <Container maxWidth="sm" style={{ textAlign: "center", marginTop: "50px" }}>
      <Typography variant="h3" gutterBottom>
        せいじトーク
      </Typography>
      <Typography variant="body1" paragraph>
        政治について簡単に質問できるアプリ。自分の考えに合った政党がどこなのかもわかる！
        たくさん調べ、勉強や投票に役立てよう！
      </Typography>
      <Box
        display="flex"
        justifyContent="center"
        gap={2}
        marginTop={4}
        flexDirection={{ xs: "column", sm: "row" }}
      >
        <Link to="/chat" style={{ textDecoration: "none" }}>
          <Button variant="contained" color="primary" size="large">
            質問をする
          </Button>
        </Link>
        <Button variant="outlined" color="primary" size="large">
          自分に合った政党診断
        </Button>
      </Box>
    </Container>
  );
};

export default HomePage;
