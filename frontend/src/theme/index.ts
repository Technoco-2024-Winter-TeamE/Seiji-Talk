// src/theme/index.ts
import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      light: "#EEEEEE", // 一番薄い色
      main: "#00ADB5", // 基本色
      dark: "#393E46", // 濃い色
      contrastText: "#222831", // テキストカラー
    },
    secondary: {
      main: "#007A82", // セカンダリカラー
    },
    background: {
      default: "#EEEEEE", // 背景色
    },
    text: {
      primary: "#222831", // テキスト色
      secondary: "#609966", // サブテキスト色
    },
  },
  typography: {
    fontFamily: "'Roboto', 'Noto Sans JP', sans-serif",
    h1: {
      fontSize: "2rem",
      fontWeight: "bold",
    },
    h2: {
      fontSize: "1.75rem",
      fontWeight: "bold",
    },
    body1: {
      fontSize: "1rem",
    },
  },
  shape: {
    borderRadius: 8, // 全体の角丸を統一
  },
});

export default theme;
