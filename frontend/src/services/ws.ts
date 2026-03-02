import { ref } from "vue";
import { Conversation, Message, User } from "../type";

const messages = ref<Message[]>([]);
const online = ref<User[]>([]);
const conversation = ref<Conversation | null>(null)
const isConnected = ref(false);


let ws: WebSocket | null = null;
let reconnectTimer: number | null = null;
let pingInterval: number | null = null;

let reconnectAttempts = 0;
let manuallyClosed = false;
  

const connect = () => {
  if (ws?.readyState === WebSocket.OPEN ||
      ws?.readyState === WebSocket.CONNECTING) {
    return;
  }

  manuallyClosed = false;

  ws = new WebSocket("ws://localhost:8000/api/ws");

  ws.onopen = () => {
    isConnected.value = true;
    reconnectAttempts = 0;

    pingInterval = window.setInterval(() => {
      ws?.send(JSON.stringify({ type: "ping" }));
    }, 25000);
  };

  ws.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data);

      switch (data.type) {

        case "chat_message":
          if (conversation.value) { 
            messages.value.push(data)
          }
          break
        
        case "chat_messages":
          if (conversation.value) { 
            messages.value = data['messages']
          }
          break
      
        case "online_list":
          online.value = data.users
          break
      
        case "user_online":
          online.value.push(data.user)
          break

        case "handshake":
          conversation.value = data.conversation
          break

        case "user_offline":
          online.value =
            online.value.filter(u => u.id !== data.user.id)
          break
      }
    } catch {
      console.error("error ws message");
    }
  };

  ws.onclose = () => {
    isConnected.value = false;

    if (pingInterval) {
      clearInterval(pingInterval);
      pingInterval = null;
    }

    if (manuallyClosed) return;

    const timeout = Math.min(30000, 500 * 2 ** reconnectAttempts++);
    reconnectTimer = window.setTimeout(connect, timeout);
  };

  ws.onerror = () => ws?.close();
};

const send = (message: string) => {
  ws?.send(
    JSON.stringify({
      type: "chat_message",
      conversation_id: conversation.value?.id,
      to: conversation.value?.partner.id,
      message: message,
    })
  );
};

const sendHandshake = (partner_id: string) => {
  ws?.send(
    JSON.stringify({
      type: "handshake",
      partner_id: partner_id,
    })
  );
};

const disconnect = () => {
  manuallyClosed = true;

  if (reconnectTimer) clearTimeout(reconnectTimer);
  if (pingInterval) clearInterval(pingInterval);

  ws?.close();
  ws = null;
  isConnected.value = false;
};

const clearMessages = () => {
  messages.value = [];
};

export function useWebSocket() {

  return {
    messages,
    online,
    conversation,
    isConnected,
    connect,
    disconnect,
    send,
    sendHandshake,
    clearMessages,
  };
}