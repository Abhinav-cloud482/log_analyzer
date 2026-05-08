# =========================================================
# ADVANCED AI LOG ANALYZER
# =========================================================
# FEATURES
# ---------------------------------------------------------
# ✔ Machine Learning Anomaly Detection
# ✔ Real-Time Monitoring
# ✔ PDF Report Generation
# ✔ CSV Database Storage
# ✔ Email Alerts
# ✔ Charts & Visualizations
# ✔ Brute Force Detection
# ✔ High Traffic Detection
# ✔ Error Detection
# ✔ Fully Executable
# =========================================================

import re
import os
import time
import smtplib
import threading
import pandas as pd
import matplotlib.pyplot as plt

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from sklearn.ensemble import IsolationForest

# =========================================================
# CONFIGURATION
# =========================================================

LOG_FILE = "server.log"

FAILED_LOGIN_THRESHOLD = 5
REQUEST_THRESHOLD = 20

ENABLE_REALTIME_MONITORING = True
REALTIME_REFRESH_SECONDS = 5

# =========================================================
# EMAIL CONFIGURATION
# =========================================================
# Use Gmail App Password
# Example:
# EMAIL_SENDER = "yourmail@gmail.com"
# EMAIL_PASSWORD = "your_app_password"
# EMAIL_RECEIVER = "receiver@gmail.com"

EMAIL_ALERTS = False

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver@gmail.com"

# =========================================================
# LOG PATTERN
# =========================================================

log_pattern = re.compile(
    r'(\d+\.\d+\.\d+\.\d+).*?\[(.*?)\]\s"(\w+)\s(.*?)\s.*?"\s(\d{3})'
)

# =========================================================
# SEND EMAIL ALERT
# =========================================================

def send_email_alert(subject, body):

    if not EMAIL_ALERTS:
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        server.send_message(msg)
        server.quit()

        print("EMAIL ALERT SENT")

    except Exception as e:
        print("Email Error:", e)

# =========================================================
# PARSE TIMESTAMP
# =========================================================

def parse_timestamp(ts):

    try:
        return datetime.strptime(
            ts.split()[0],
            "%d/%b/%Y:%H:%M:%S"
        )

    except:
        return None

# =========================================================
# READ LOG FILE
# =========================================================

def load_logs():

    logs = []

    try:
        with open(LOG_FILE, "r") as file:

            for line in file:

                match = log_pattern.search(line)

                if match:

                    ip = match.group(1)
                    timestamp = match.group(2)
                    method = match.group(3)
                    endpoint = match.group(4)
                    status = int(match.group(5))

                    logs.append({
                        "ip": ip,
                        "timestamp": timestamp,
                        "method": method,
                        "endpoint": endpoint,
                        "status": status
                    })

    except FileNotFoundError:
        print(f"ERROR: '{LOG_FILE}' not found.")
        return pd.DataFrame()

    df = pd.DataFrame(logs)

    if df.empty:
        return df

    df["parsed_time"] = df["timestamp"].apply(parse_timestamp)

    return df

# =========================================================
# MACHINE LEARNING ANOMALY DETECTION
# =========================================================

def detect_anomalies(df):

    print("\n================ ML ANOMALY DETECTION ================\n")

    ip_counts = df["ip"].value_counts().reset_index()

    ip_counts.columns = ["ip", "request_count"]

    model = IsolationForest(
        contamination=0.15,
        random_state=42
    )

    ip_counts["anomaly"] = model.fit_predict(
        ip_counts[["request_count"]]
    )

    anomalies = ip_counts[ip_counts["anomaly"] == -1]

    if anomalies.empty:
        print("No ML anomalies detected.")

    else:
        print("Anomalous IPs Detected:")
        print(anomalies)

        send_email_alert(
            "AI Log Analyzer Alert",
            f"Anomalous IPs detected:\n\n{anomalies}"
        )

    anomalies.to_csv("ml_anomalies.csv", index=False)

    return anomalies

# =========================================================
# GENERATE CHARTS
# =========================================================

def generate_charts(df):

    status_counts = df["status"].value_counts()
    top_ips = df["ip"].value_counts().head(10)
    top_endpoints = df["endpoint"].value_counts().head(10)

    # Status Codes
    plt.figure(figsize=(10, 5))

    status_counts.sort_index().plot(
        kind="bar",
        color="skyblue"
    )

    plt.title("HTTP Status Codes")
    plt.xlabel("Status")
    plt.ylabel("Count")

    plt.tight_layout()
    plt.savefig("status_codes.png")

    # Top IPs
    plt.figure(figsize=(10, 5))

    top_ips.plot(
        kind="bar",
        color="orange"
    )

    plt.title("Top IP Addresses")
    plt.xlabel("IP")
    plt.ylabel("Requests")

    plt.tight_layout()
    plt.savefig("top_ips.png")

    # Endpoints
    plt.figure(figsize=(10, 5))

    top_endpoints.plot(
        kind="bar",
        color="green"
    )

    plt.title("Top Endpoints")
    plt.xlabel("Endpoint")
    plt.ylabel("Hits")

    plt.tight_layout()
    plt.savefig("top_endpoints.png")

# =========================================================
# PDF REPORT
# =========================================================

def generate_pdf_report(df):

    from matplotlib.backends.backend_pdf import PdfPages

    pdf = PdfPages("log_analysis_report.pdf")

    # -----------------------------------------------------
    # SUMMARY PAGE
    # -----------------------------------------------------

    fig = plt.figure(figsize=(10, 6))

    plt.axis("off")

    total_requests = len(df)
    unique_ips = df["ip"].nunique()
    errors = len(df[df["status"] >= 400])

    report_text = f"""
    ADVANCED AI LOG ANALYSIS REPORT

    Total Requests: {total_requests}

    Unique IPs: {unique_ips}

    Total Errors: {errors}

    Report Generated:
    {datetime.now()}
    """

    plt.text(
        0.1,
        0.5,
        report_text,
        fontsize=14
    )

    pdf.savefig(fig)
    plt.close()

    # -----------------------------------------------------
    # ADD CHARTS
    # -----------------------------------------------------

    for image in [
        "status_codes.png",
        "top_ips.png",
        "top_endpoints.png"
    ]:

        fig = plt.figure(figsize=(10, 6))

        img = plt.imread(image)

        plt.imshow(img)
        plt.axis("off")

        pdf.savefig(fig)
        plt.close()

    pdf.close()

    print("PDF REPORT GENERATED")

# =========================================================
# EXPORT CSV DATABASE
# =========================================================

def export_database(df):

    os.makedirs("database", exist_ok=True)

    df.to_csv(
        "database/log_database.csv",
        index=False
    )

    print("CSV DATABASE STORED")

# =========================================================
# MAIN ANALYSIS
# =========================================================

def analyze_logs():

    print("\n=================================================")
    print("        ADVANCED AI LOG ANALYZER")
    print("=================================================\n")

    df = load_logs()

    if df.empty:
        print("No valid logs found.")
        return

    # =====================================================
    # SUMMARY
    # =====================================================

    total_requests = len(df)

    status_counts = df["status"].value_counts()

    error_logs = df[df["status"] >= 400]

    unique_ips = df["ip"].nunique()

    top_ips = df["ip"].value_counts().head(10)

    top_endpoints = df["endpoint"].value_counts().head(10)

    print("Total Requests:", total_requests)
    print("Unique IPs:", unique_ips)

    print("\nSTATUS CODES")
    print(status_counts)

    print("\nTOP IPs")
    print(top_ips)

    print("\nTOP ENDPOINTS")
    print(top_endpoints)

    # =====================================================
    # FAILED LOGIN DETECTION
    # =====================================================

    failed_logins = df[
        (df["status"] == 401) |
        (df["endpoint"].str.contains(
            "login",
            case=False,
            na=False
        ))
    ]

    failed_ip_counts = failed_logins["ip"].value_counts()

    suspicious_ips = failed_ip_counts[
        failed_ip_counts >= FAILED_LOGIN_THRESHOLD
    ]

    print("\n================ SECURITY ALERTS ================\n")

    if not suspicious_ips.empty:

        print("Possible Brute Force Attack:")
        print(suspicious_ips)

        send_email_alert(
            "Brute Force Alert",
            f"Suspicious IPs:\n\n{suspicious_ips}"
        )

    else:
        print("No brute force attacks detected.")

    # =====================================================
    # HIGH TRAFFIC DETECTION
    # =====================================================

    request_counts = df["ip"].value_counts()

    high_traffic_ips = request_counts[
        request_counts >= REQUEST_THRESHOLD
    ]

    if not high_traffic_ips.empty:

        print("\nHigh Traffic IPs:")
        print(high_traffic_ips)

    else:
        print("\nNo abnormal traffic spikes.")

    # =====================================================
    # MACHINE LEARNING
    # =====================================================

    detect_anomalies(df)

    # =====================================================
    # EXPORT REPORTS
    # =====================================================

    error_logs.to_csv(
        "error_logs.csv",
        index=False
    )

    summary_data = {
        "Metric": [
            "Total Requests",
            "Unique IPs",
            "Total Errors"
        ],
        "Value": [
            total_requests,
            unique_ips,
            len(error_logs)
        ]
    }

    summary_df = pd.DataFrame(summary_data)

    summary_df.to_csv(
        "summary_report.csv",
        index=False
    )

    export_database(df)

    # =====================================================
    # CHARTS
    # =====================================================

    generate_charts(df)

    # =====================================================
    # PDF REPORT
    # =====================================================

    generate_pdf_report(df)

    print("\n=================================================")
    print("ANALYSIS COMPLETE")
    print("=================================================\n")

# =========================================================
# REAL-TIME MONITORING
# =========================================================

def realtime_monitor():

    print("\nREAL-TIME MONITORING STARTED...\n")

    last_size = 0

    while True:

        try:

            current_size = os.path.getsize(LOG_FILE)

            if current_size != last_size:

                print(
                    f"\n[{datetime.now()}] "
                    f"NEW LOG ACTIVITY DETECTED\n"
                )

                analyze_logs()

                last_size = current_size

            time.sleep(REALTIME_REFRESH_SECONDS)

        except KeyboardInterrupt:

            print("\nReal-time monitoring stopped.")
            break

        except Exception as e:

            print("Monitoring Error:", e)

# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    analyze_logs()

    if ENABLE_REALTIME_MONITORING:

        realtime_monitor()