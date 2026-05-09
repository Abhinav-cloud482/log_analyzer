# log_analyzer
AI-powered log analysis tool with real-time monitoring, anomaly detection, brute-force attack detection, automated PDF reporting, email alerts, and interactive visualizations.


## Advanced AI Log Analyzer

An intelligent Python-based log analysis system that performs **real-time monitoring**, **machine learning anomaly detection**, **security threat detection**, **PDF report generation**, and **data visualization** from server logs.

Designed for cybersecurity enthusiasts, SOC analysts, system administrators, and Python developers.


## Features

- Machine Learning Anomaly Detection  
- Real-Time Log Monitoring  
- Brute Force Attack Detection  
- High Traffic Detection  
- HTTP Error Detection  
- PDF Report Generation  
- CSV Database Export  
- Email Alerts  
- Charts & Visualizations  
- Fully Automated & Executable


## Technologies Used

- Python 3
- Pandas
- Matplotlib
- Scikit-Learn
- NumPy


## Project Structure

```bash
advanced-ai-log-analyzer/
│
├── log_analyzer.py          # Main Python Script
├── server.log               # Sample Server Log File
├── requirements.txt         # Required Python Libraries
│
├── database/
│   └── log_database.csv     # Exported Log Database
│
├── error_logs.csv           # Extracted Error Logs
├── summary_report.csv       # Summary Report
├── ml_anomalies.csv         # ML Detected Anomalies
│
├── status_codes.png         # Status Code Chart
├── top_ips.png              # Top IPs Chart
├── top_endpoints.png        # Top Endpoints Chart
│
└── log_analysis_report.pdf  # Final PDF Report
```


## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/advanced-ai-log-analyzer.git
cd advanced-ai-log-analyzer
```


### Install Dependencies

```bash
pip install -r requirements.txt
```


## Running the Project

Run the analyzer using :-

```bash
python log_analyzer.py
```

The program will :- 

- Parse logs
- Detect suspicious activities
- Generate charts
- Create CSV reports
- Export PDF analysis
- Start real-time monitoring


## Sample Log Format

The analyzer supports logs in this format :-

```log
192.168.1.10 - - [08/May/2026:10:15:32] "GET /index.html HTTP/1.1" 200
192.168.1.15 - - [08/May/2026:10:16:11] "POST /login HTTP/1.1" 401
```


## Detection Capabilities

### Brute Force Detection

Detects repeated failed login attempts from the same IP address.

Example :-
- Multiple `401 Unauthorized`
- Repeated `/login` requests


### High Traffic Detection

Identifies suspicious IPs generating unusually high request volumes.


### Machine Learning Anomaly Detection

Uses **Isolation Forest Algorithm** from Scikit-Learn to detect anomalous IP behavior.


### Error Detection

Automatically extracts :-
- 4xx Errors
- 5xx Errors

Exports them into :-

```bash
error_logs.csv
```


## Generated Reports

The system automatically creates :-

| Report/File | Description |
|---|---|
| `summary_report.csv` | Overall statistics |
| `error_logs.csv` | Error requests |
| `ml_anomalies.csv` | Detected anomalies |
| `log_analysis_report.pdf` | Full PDF report |
| `database/log_database.csv` | Parsed log database |


## Generated Charts

The analyzer generates :- 

- HTTP Status Code Distribution  
- Top IP Addresses  
- Most Accessed Endpoints

Saved as :- 

```bash
status_codes.png
top_ips.png
top_endpoints.png
```


## Email Alerts Configuration

Enable email alerts inside :-

```python
EMAIL_ALERTS = True
```

Update credentials :-

```python
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver@gmail.com"
```


## Real-Time Monitoring

The analyzer continuously watches the log file for changes.

Configuration :-

```python
ENABLE_REALTIME_MONITORING = True
REALTIME_REFRESH_SECONDS = 5
```


## Example Output

```bash
=================================================
        ADVANCED AI LOG ANALYZER
=================================================

Total Requests: 10
Unique IPs: 6

STATUS CODES
200    3
401    5
500    1
403    1

Possible Brute Force Attack:
192.168.1.15    5

PDF REPORT GENERATED
ANALYSIS COMPLETE
```

## Screenshots

<img width="1366" height="705" alt="1" src="https://github.com/user-attachments/assets/3cb46cba-82ab-4bfc-9f8a-dc68359fcdda" />

<img width="1366" height="587" alt="2" src="https://github.com/user-attachments/assets/517c32ac-752f-4e9c-8cbe-169c33e026df" />

<img width="1366" height="701" alt="3" src="https://github.com/user-attachments/assets/aebd2c08-f5ff-4543-b6e1-64215a435c36" />

<img width="1362" height="684" alt="4" src="https://github.com/user-attachments/assets/38ff7eb0-1d28-46a0-bad0-463ad3d17f86" />

## Use Cases

- Security Monitoring
- SIEM Projects
- Cybersecurity Labs
- Server Log Auditing
- Threat Detection
- Intrusion Detection
- DevOps Monitoring
- Academic Projects


## Requirements

```txt
pandas
matplotlib
scikit-learn
numpy
```


## Future Improvements

- Web Dashboard
- Streamlit Integration
- Live Alert Notifications
- Database Integration (MySQL/PostgreSQL)
- GeoIP Tracking
- Docker Support
- REST API
- Threat Intelligence Integration


## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit changes
4. Open a Pull Request


## License

This project is licensed under the MIT License.


## Author

Abhinav Dixit

Python Developer | Data & ML Enthusiast
