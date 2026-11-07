export class WebSocketService {
  private ws: WebSocket | null = null;
  private listeners: ((event: any) => void)[] = [];

  connect(url = `ws://${window.location.host}/ws/assistant`) {
    try {
      this.ws = new WebSocket(url);
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.listeners.forEach((fn) => fn(data));
        } catch (e) {}
      };
      this.ws.onclose = () => {
        setTimeout(() => this.connect(url), 3000);
      };
    } catch (e) {}
  }

  addListener(callback: (event: any) => void) {
    this.listeners.push(callback);
  }

  send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(typeof data === 'string' ? data : JSON.stringify(data));
    }
  }
}

export const wsService = new WebSocketService();
