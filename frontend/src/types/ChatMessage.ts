export interface ChatMessage {
    id: string;
    mode: "latest" | "glossary";
    role: "user" | "assistant";
    message: string;
    sources?: { title: string; url: string }[];
    keywords?: string[];
}
