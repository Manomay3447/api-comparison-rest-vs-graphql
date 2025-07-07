# 📊 Comparative Analysis of REST and GraphQL APIs

A full-stack benchmarking system to evaluate and compare the performance of REST and GraphQL APIs under various load conditions. This project provides automated performance measurements, real-time visualizations, system resource tracking, and exportable reports for in-depth analysis.

---

## 🎯 Project Objective

To empirically compare REST and GraphQL API architectures by analyzing:

- Request duration  
- Time-to-first-byte (TTFB)  
- Payload size  
- Record count  
- CPU and memory usage  
- Scalability under load (concurrent users & request volume)

---

## ⚙️ Features

### a) API Performance Measurement
- Measures request duration, TTFB, payload size, and record count.
- REST and GraphQL endpoints hosted on separate ports using Flask.

### b) CPU & Memory Usage Tracking via PIDs
- APIs are launched via `run_all.sh` script.
- Their process IDs (PIDs) are stored and monitored.
- CPU and memory usage recorded via `psutil`.

### c) System-Wide Resource Monitoring
- Tracks total system CPU and memory usage in addition to per-API metrics.

### d) Real-Time Dashboard (`index.html`)
- Built using **Chart.js**.
- Automatically refreshes every 10 seconds.
- Selectable metric types:
  - Duration, TTFB, Size, Count
  - REST/GraphQL CPU & Memory
  - System CPU & Memory
  - 📈 **Scalability (Duration vs Concurrent Users)**
  - 📈 **Load Graph (Response Time vs No. of Requests)**

### e) Export Options
- Download current graph data as:
  - **CSV**
  - **PDF**

### f) Simulated Load Testing
- `load_client.py` script to generate concurrent load:
  - Choose number of threads and requests
  - Target either REST, GraphQL, or both APIs

### g) Unified Benchmark Engine (`compare.py`)
- Executes both REST and GraphQL calls
- Collects all metrics and resource usage
- Estimates user load by parsing running client threads
- Appends results as JSON to `report.json`

---

## 🚀 How to Run

### 1. Clone the Repository
- git clone git@github.com:Manomay3447/api-comparison-rest-vs-graphql.git
- cd api-comparison-rest-vs-graphql

### 2. Start the APIs
- ./run_all.sh

### 3. Start Load Simulation
- python3 load_test/load_client.py --threads 30 --requests 100 --target rest/graphql/both

### 4. Open Dashboard
- Open dashboard/index.html in a browser (served locally or via live server)

---
