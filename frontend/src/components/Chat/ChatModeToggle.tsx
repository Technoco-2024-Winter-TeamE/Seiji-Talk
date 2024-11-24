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
    >
      <ToggleButton
        value="latest"
        sx={{
          borderRadius: "16px", // 個別のボタンの角を丸く
          textTransform: "none", // ボタン内のテキストをそのまま表示
          fontSize: "14px",
          fontWeight: "bold",
          "&.Mui-selected": {
            backgroundColor: "primary.main",
            color: "primary.light",
            "&:hover": {
              backgroundColor: "secondary.main",
            },
          },
        }}
      >
        最新情報モード
      </ToggleButton>
      <ToggleButton
        value="glossary"
        sx={{
          borderRadius: "16px", // 個別のボタンの角を丸く
          textTransform: "none",
          fontSize: "14px",
          fontWeight: "bold",
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
