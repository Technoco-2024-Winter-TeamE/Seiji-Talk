import React, { useState } from "react";
import ChatHistory from "../../components/Chat/ChatHistory";
import ChatInput from "../../components/Chat/ChatInput";
import ChatModeToggle from "../../components/Chat/ChatModeToggle";
import { ChatMessage } from "../../types/ChatMessage";

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState<"latest" | "glossary">("latest");
  const [loading, setLoading] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;

    const newMessage: ChatMessage = {
      id: `${Date.now()}`,
      role: "user",
      mode,
      message: input,
    };

    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    setLoading(true);
    setTimeout(() => {
      const assistantMessage: ChatMessage = {
        id: `${Date.now() + 1}`,
        role: "assistant",
        mode,
        message:
          mode === "latest"
            ? "最新情報モードでの回答例です。"
            : "与党とは、議会で多数の議席を占めて、内閣を組織している政党のことです。",
        sources:
          mode === "latest"
            ? [
                { title: "参考記事1", url: "#" },
                { title: "参考記事2", url: "#" },
              ]
            : undefined,
        keywords:
          mode === "glossary" ? ["野党", "議会制民主主義", "内閣", "政党"] : undefined,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setLoading(false);
    }, 1000);
  };

  const handleKeywordClick = (keyword: string) => {
    setInput(`${keyword}とは何ですか？`);
    setMode("glossary");
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "background.default",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          width: "60%",
          maxWidth: "800px",
          minWidth: "400px",
          height: "90vh",
          backgroundColor: "primary.light",
          borderRadius: "8px",
          boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)",
        }}
      >
        {/* チャット履歴 */}
        <ChatHistory messages={messages} onKeywordClick={handleKeywordClick} />
        
        {/* 入力エリア */}
        <div
          style={{
            borderTop: "1px solid #ddd",
            padding: "16px",
            display: "flex",
            flexDirection: "column",
            gap: "8px",
          }}
        >
          <ChatModeToggle mode={mode} onChange={setMode} />
          <ChatInput
            value={input}
            onChange={setInput}
            onSend={handleSend}
            loading={loading}
            placeholder={
              mode === "latest"
                ? "質問を入力してください..."
                : "用語を入力してください..."
            }
          />
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
