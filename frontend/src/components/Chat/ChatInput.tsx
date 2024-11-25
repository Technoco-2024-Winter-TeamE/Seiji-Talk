import React, { useState } from "react";
import { Box, TextField, Button } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  loading: boolean;
  placeholder: string; // プレースホルダーを動的に受け取る
}

const ChatInput: React.FC<ChatInputProps> = ({ value, onChange, onSend, loading, placeholder }) => {
  const [isComposing, setIsComposing] = useState(false); // IME中かどうかの状態

  const handleKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    if (event.key === "Enter" && !isComposing && !loading) {
      event.preventDefault(); // フォームのリフレッシュを防止
      onSend();
    }
  };

  const handleCompositionStart = () => setIsComposing(true); // IME開始
  const handleCompositionEnd = () => setIsComposing(false); // IME終了

  return (
    <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
      <TextField
        fullWidth
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown} // エンターキーイベントを追加
        onCompositionStart={handleCompositionStart} // IME開始
        onCompositionEnd={handleCompositionEnd} // IME終了
        placeholder={placeholder} // 動的に受け取る
        variant="outlined"
        sx={{
          borderRadius: "20px",
          boxShadow: "0px 2px 3px rgba(0, 0, 0, 0.1)",
          "& .MuiOutlinedInput-root": {
            borderRadius: "20px",
            backgroundColor: "white",
            "&:hover .MuiOutlinedInput-notchedOutline": {
              borderColor: "primary.main",
            },
            "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
              borderColor: "primary.main", // フォーカス時のボーダーカラー
              borderWidth: "2px", // フォーカス時のボーダーの太さ
            },
          },
          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "primary.light", // 通常時のボーダーカラー
            borderWidth: "2px", // ボーダーの太さ
          },
        }}
      />

      <Button
        variant="contained"
        onClick={onSend}
        disabled={loading}
        sx={{
          minWidth: "56px",
          minHeight: "56px",
          borderRadius: "50%", // ボタンを丸く
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          color: "primary.light",
          backgroundColor: "primary.main",
          "&:hover": {
            backgroundColor: "secondary.main", // ホバー時の背景色
          },
        }}
      >
        <SendIcon />
      </Button>
    </Box>
  );
};

export default ChatInput;
