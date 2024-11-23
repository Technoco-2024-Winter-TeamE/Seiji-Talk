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
          "& .MuiOutlinedInput-root": {
            borderRadius: "20px", // 入力フォームを丸く
          },
        }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={onSend}
        disabled={loading}
        sx={{
          minWidth: "56px",
          minHeight: "56px",
          borderRadius: "50%", // ボタンを丸く
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <SendIcon />
      </Button>
    </Box>
  );
};

export default ChatInput;
