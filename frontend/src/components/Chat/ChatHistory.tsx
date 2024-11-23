import React, { useEffect, useRef } from "react";
import { Box, Typography } from "@mui/material";
import { ChatMessage } from "../../types/ChatMessage";

interface ChatHistoryProps {
  messages: ChatMessage[];
  onKeywordClick: (keyword: string) => void;
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages, onKeywordClick }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 新しいメッセージが追加された際にスクロールする
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <Box
      sx={{
        flex: 1,
        overflowY: "auto",
        padding: "16px",
        backgroundColor: "#f9f9f9",
      }}
    >
      {messages.map((message) => (
        <Box
          key={message.id}
          sx={{
            display: "flex",
            flexDirection: message.role === "user" ? "row-reverse" : "row",
            alignItems: "flex-start",
            marginBottom: "16px",
          }}
        >
          {/* アイコン */}
          <Box
            sx={{
              width: "36px",
              height: "36px",
              borderRadius: "50%",
              backgroundColor: message.role === "user" ? "#1e88e5" : "#6c757d",
              color: "#fff",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              marginRight: message.role === "user" ? 0 : "8px",
              marginLeft: message.role === "user" ? "8px" : 0,
            }}
          >
            {message.role === "user" ? "U" : "A"}
          </Box>

          {/* メッセージ内容 */}
          <Box
            sx={{
              backgroundColor: message.role === "user" ? "#1e88e5" : "#fff",
              color: message.role === "user" ? "#fff" : "#000",
              padding: "12px",
              borderRadius: "8px",
              maxWidth: "70%",
              boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.1)",
            }}
          >
            <Typography variant="body1">{message.message}</Typography>
            {/* 参考ソースやキーワードを表示 */}
            {message.sources && (
              <Box sx={{ marginTop: "8px" }}>
                <Typography variant="caption" sx={{ fontWeight: "bold" }}>
                  参考ソース:
                </Typography>
                {message.sources.map((source, index) => (
                  <Typography
                    key={index}
                    component="a"
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{ display: "block", color: "#1e88e5", textDecoration: "underline" }}
                  >
                    {source.title}
                  </Typography>
                ))}
              </Box>
            )}
            {message.keywords && (
              <Box sx={{ marginTop: "8px", display: "flex", flexWrap: "wrap", gap: "8px" }}>
                {message.keywords.map((keyword, index) => (
                  <Box
                    key={index}
                    onClick={() => onKeywordClick(keyword)}
                    sx={{
                      backgroundColor: "#e3f2fd",
                      color: "#1e88e5",
                      padding: "4px 8px",
                      borderRadius: "16px",
                      cursor: "pointer",
                      fontSize: "12px",
                      fontWeight: "bold",
                      "&:hover": {
                        backgroundColor: "#bbdefb",
                      },
                    }}
                  >
                    {keyword}
                  </Box>
                ))}
              </Box>
            )}
          </Box>
        </Box>
      ))}
      {/* 自動スクロール用の要素 */}
      <div ref={messagesEndRef} />
    </Box>
  );
};

export default ChatHistory;
