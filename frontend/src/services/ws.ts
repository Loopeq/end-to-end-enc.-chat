const connection = new WebSocket(`${import.meta.env.VITE_WS_URL}/api/ws`)

export default connection