
# 🖧 Client–Server Communication & Producer–Consumer (Python)

This repository contains two mini‑projects implemented in Python:

1. **Client–Server TCP communication (Sockets)**
2. **Producer–Consumer system using shared resources**

Both projects are simple demonstrations of inter‑process communication (IPC) and networking concepts.

---

# 📂 Repository Structure

```
Client-Server-communication/
│
├── client_server/
│   ├── LAB2_client.py       # TCP client
│   ├── LAB2_server.py       # TCP server
│   └── LAB2_HeaderFile.py   # Shared definitions
│
├── consumer_producer/
│   ├── LAB2_producer.py     # Producer
│   ├── LAB2_consumer.py     # Consumer
│   └── LAB2_HeaderFile.py   # Shared configuration
│
└── __pycache__/             # Auto-generated Python cache files
```

---

# 🚀 How to Run the Client–Server Project

### 1️⃣ Start the Server
```
cd client_server
python LAB2_server.py
```

The server will open a TCP socket and wait for incoming client connections.

### 2️⃣ Start the Client (in a second terminal)
```
cd client_server
python LAB2_client.py
```

The client connects to the server and exchanges messages defined in `LAB2_HeaderFile.py`.

---

# 🏭 How to Run the Producer–Consumer Project

### 1️⃣ Open two terminals.

### **Terminal A — Producer**
```
cd consumer_producer
python LAB2_producer.py
```

### **Terminal B — Consumer**
```
cd consumer_producer
python LAB2_consumer.py
```

The producer generates data and writes it into a shared structure.  
The consumer reads and processes the data.

---

# ⚙️ Requirements

Install Python 3.10+

---

# 📘 Summary

This repository demonstrates:
✔ Basic TCP/IP networking (client–server model)  
✔ Socket programming in Python  
✔ Inter‑process communication  
✔ Producer–consumer synchronization concepts  


