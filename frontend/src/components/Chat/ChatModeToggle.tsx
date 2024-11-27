import React from "react";
import { ToggleButton, ToggleButtonGroup } from "@mui/material";

interface ChatModeToggleProps {
  mode: "latest" | "glossary";
  onChange: (mode: "latest" | "glossary") => void;
}

const ChatModeToggle: React.FC<ChatModeToggleProps> = ({ mode, onChange }) => {
  const handleModeChange = (event: React.MouseEvent<HTMLElement>, newMode: "latest" | "glossary") => {
    if (newMode !== null) {
      onChange(newMode);
    }
  };

  return (
    <ToggleButtonGroup
      value={mode}
      exclusive
      onChange={handleModeChange}
      sx={{
        display: "inline-flex", // 子要素の幅に合わせる
        width: "auto", // 横幅を自動調整
        borderWidth: "2px",
        borderColor: "primary.light",
        borderRadius: "16px", // 全体の角丸を統一
        overflow: "hidden", // ボタン間の重なりを防ぐ
      }}
    >
      <ToggleButton
        value="latest"
        sx={{
          borderRadius: "16px",
          textTransform: "none", // ボタン内のテキストをそのまま表示
          fontSize: "14px",
          fontWeight: "bold",
          boxShadow: "0px 2px 3px rgba(0, 0, 0, 0.1)",
          "&.Mui-selected": {
            backgroundColor: "primary.main",
            color: "primary.light",
            "&:hover": {
              backgroundColor: "secondary.main",
            },
          },
        }}
      >
        情報検索モード
      </ToggleButton>
      <ToggleButton
        value="glossary"
        sx={{
          borderRadius: "16px",
          textTransform: "none",
          fontSize: "14px",
          fontWeight: "bold",
          boxShadow: "0px 2px 3px rgba(0, 0, 0, 0.1)",
          "&.Mui-selected": {
            backgroundColor: "primary.main",
            color: "primary.light",
            "&:hover": {
              backgroundColor: "secondary.main",
            },
          },
        }}
      >
        用語解説モード
      </ToggleButton>
    </ToggleButtonGroup>

  );
};

export default ChatModeToggle;
