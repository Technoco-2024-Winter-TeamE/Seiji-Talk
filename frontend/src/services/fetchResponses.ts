import { ChatMessage } from "../types/ChatMessage";

const fetchResponses = async (mode: "latest" | "glossary", input: string): Promise<ChatMessage> => {
  if (mode === "latest") {
    return {
      id: `${Date.now() + 1}`,
      mode,
      role: "assistant",
      message: "最新情報モードでの回答例です。",
    };
  } else if (mode === "glossary") {
    return {
      id: `${Date.now() + 1}`,
      mode,
      role: "assistant",
      message: "与党とは、議会で多数の議席を占めて内閣を組織している政党のことです。",
    };
  }
  throw new Error("Invalid mode");
};

export default fetchResponses;
