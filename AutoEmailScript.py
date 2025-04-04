import smtplib
import pandas as pd
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ✅ File paths
# excel_path = "/home/kajal/Job-App-Bot/Job_List_Data/Job_Lists_Test.xlsx"
excel_path = "Job_List_Data/job_listings.xlsx" # Update with your Excel file path
resume_path = "/path/to/your_resume.docx"  # Update with your resume path

# ✅ Email credentials
SENDER_EMAIL = "your_email@gmail.com" # Update with your email
SENDER_PASSWORD = "your_gmail_app_password"  # Use your 16 characters(abcd efgh ijkl mnop) app password for security

def send_emails():
    """Send emails only for job listings that haven't been sent yet."""
    
    # ✅ Check if the file exists
    if not os.path.exists(excel_path):
        print(f"❌ No job listings file found at '{excel_path}'. Emails cannot be sent.")
        return

    # ✅ Load Excel file
    df = pd.read_excel(excel_path)

    # ✅ Filter for jobs where email is not yet sent
    df_unsent = df[df["Email Sent"] != "Yes"]

    if df_unsent.empty:
        print("✅ All emails have already been sent. No new emails to send.")
        return

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)

    for index, row in df_unsent.iterrows():
        to_email = row["To"]
        cc_email = row["CC"] if pd.notna(row["CC"]) else ""
        job_title = row["Job Title"] if pd.notna(row["Job Title"]) else "Software Engineer" 

        if pd.notna(to_email):  
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = to_email
            msg["Cc"] = cc_email
            msg["Subject"] = f"Looking for {job_title} Position"
            # Change the body of the email as per your requirement
            body = f"""\
Hi,

I hope you're doing well! I recently came across the {job_title} position and have submitted my application. I have also attached my resume for your reference.

Please let me know if you need any additional information to support my application.

Best regards,  
Your Name  
Your email 
Your phone number
"""
            msg.attach(MIMEText(body, "plain"))

            # ✅ Attach resume
            if os.path.exists(resume_path):
                with open(resume_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(resume_path)}")
                    msg.attach(part)
            else:
                print(f"⚠️ Resume file not found at {resume_path}. Email sent without attachment.")

            recipients = [to_email] + ([cc_email] if cc_email else [])

            try:
                server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
                print(f"📧 Email sent to: {to_email} (CC: {cc_email}) for Job Title: {job_title}")

                # ✅ Mark email as sent
                df.loc[df.index == index, "Email Sent"] = "Yes"
            except Exception as e:
                print(f"❌ Failed to send email to {to_email}: {e}")

    server.quit()

    # ✅ Save updated Excel file (marking sent emails)
    df.to_excel(excel_path, index=False, engine="openpyxl")
    print("✅ Email statuses updated in the job listings file.")

if __name__ == "__main__":
    send_emails()  # Run when executed directly
