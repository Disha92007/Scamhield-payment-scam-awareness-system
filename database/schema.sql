CREATE DATABASE IF NOT EXISTS scamshield CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE scamshield;

CREATE TABLE IF NOT EXISTS scam_rules (
  id INT AUTO_INCREMENT PRIMARY KEY,
  rule_key VARCHAR(60) NOT NULL UNIQUE,
  label VARCHAR(150) NOT NULL,
  pattern VARCHAR(500) NOT NULL,
  weight TINYINT UNSIGNED NOT NULL DEFAULT 1,
  explanation VARCHAR(500) NOT NULL,
  advice VARCHAR(500) NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS sample_messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(150) NOT NULL,
  message TEXT NOT NULL,
  expected_risk ENUM('HIGH','MEDIUM','LOW') NOT NULL,
  description VARCHAR(500) NOT NULL
);

CREATE TABLE IF NOT EXISTS quiz_questions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  question VARCHAR(500) NOT NULL,
  options_json JSON NOT NULL,
  correct_answer TINYINT UNSIGNED NOT NULL,
  explanation VARCHAR(500) NOT NULL
);

INSERT IGNORE INTO scam_rules (rule_key,label,pattern,weight,explanation,advice) VALUES
('pin_request','UPI PIN or payment PIN request','\\b(enter|share|send|tell|provide)\\b.{0,45}\\b(upi\\s*)?pin\\b|\\bpin\\b.{0,35}\\b(receive|claim|refund|cashback)\\b',5,'A UPI PIN authorizes money leaving your account; it is not needed to receive money.','Never enter your UPI PIN to receive a payment or refund.'),
('otp_request','OTP or verification code request','\\b(share|send|tell|provide|verify with)\\b.{0,35}\\b(otp|one[- ]time password|verification code)\\b',4,'A request to share an OTP can let someone authorize access or a transaction.','Never share an OTP with callers or message senders.'),
('urgent_threat','Urgency or threat','\\b(urgent|immediately|within \\d+ hours|today only|account.{0,15}blocked|disconnect(ed|ion)?|will be blocked|suspended)\\b',2,'Scammers often create panic so people act without verifying.','Pause and independently contact the organization using its official channel.'),
('suspicious_link','Link or shortened URL','(https?://|www\\.|bit\\.ly|tinyurl|t\\.co/|cutt\\.ly)',2,'Unexpected links can lead to fake login pages or malicious sites.','Do not open unexpected links. Visit the official website or app yourself.'),
('reward_bait','Prize, cashback or reward bait','\\b(cashback|prize|lottery|won|reward|claim.{0,20}(money|cash|gift)|free gift)\\b',2,'Unexpected rewards may persuade people to click a link or disclose details.','Verify offers in the official app; never reveal a PIN to claim money.'),
('kyc_threat','KYC or account-block threat','\\b(kyc|account).{0,45}\\b(expire|update|block(ed)?|suspend(ed)?)\\b|\\b(update|complete)\\b.{0,20}\\bkyc\\b',2,'Fake KYC notices pressure people to click links or provide personal information.','Check KYC status only through your bank official app, branch, or website.'),
('remote_access','Remote-access app request','\\b(anydesk|teamviewer|remote access|screen sharing app)\\b',4,'Remote access can expose your screen, messages, and financial activity.','Do not install remote-access apps at a stranger’s request.'),
('qr_receive','QR code to receive money','\\b(scan|scanning)\\b.{0,40}\\b(qr|code)\\b.{0,55}\\b(receive|get|claim)\\b|\\b(qr code)\\b.{0,55}\\b(pin|payment)\\b',4,'Scanning a QR code and entering a UPI PIN generally authorizes a payment, not receipt of money.','Do not enter a PIN to receive money.');

INSERT INTO sample_messages (id,title,message,expected_risk,description) VALUES
(1,'UPI PIN Cashback Trap','Congratulations! You received Rs 4,999 cashback. Enter your UPI PIN at http://example.invalid/cashback to claim your reward.','HIGH','PIN request and suspicious link are warning signs.'),
(2,'Electricity Disconnection Panic','URGENT: Your electricity will be disconnected today. Call this number immediately and share OTP to stop disconnection.','HIGH','Urgency and OTP requests are warning signs.'),
(3,'Bank KYC & Account Block Threat','Your bank KYC will expire. Click this link immediately to update your account or it will be blocked.','MEDIUM','A threatening account notice with a link needs verification.'),
(4,'Telegram Work-From-Home Task Scam','Earn a guaranteed reward today. Pay a registration fee and share your bank OTP to unlock your task earnings.','HIGH','Upfront fees and OTP requests are warning signs.'),
(5,'Fake Screenshot Transfer Claim','Payment sent. Here is my screenshot. Give me the item now; bank confirmation may take time.','MEDIUM','Verify payment inside your own banking app.'),
(6,'Genuine Bank Debit Alert','Your account has been debited by Rs 500. If you did not make this transaction, contact your bank using the official app or number.','LOW','Neutral alert with official-channel advice.'),
(7,'Genuine Bank Login OTP Notice','Your login OTP is 123456. Do not share this OTP with anyone. If you did not request it, secure your account using the official app.','LOW','Protective wording, but never share real OTPs. Do not use real OTPs in testing.')
ON DUPLICATE KEY UPDATE title=VALUES(title),message=VALUES(message),expected_risk=VALUES(expected_risk),description=VALUES(description);

INSERT INTO quiz_questions (id,question,options_json,correct_answer,explanation) VALUES
(1,'A buyer sends a QR code and asks you to enter your UPI PIN to receive money. What should you do?','["Scan it and enter PIN","Do not enter PIN; receiving money does not require it","Share OTP instead"]',1,'A UPI PIN authorizes payments from your account; it is not needed to receive money.'),
(2,'A caller says your bank account will be blocked unless you share an OTP. What is safest?','["Share it quickly","Ask for their employee ID, then share it","Do not share it; contact the bank through an official channel"]',2,'Never share OTPs. Contact your bank using its official app, card, or website.'),
(3,'A buyer shows a payment screenshot. What should you do before handing over goods?','["Trust the screenshot","Verify the credit in your own bank app","Ask them to send another screenshot"]',1,'Screenshots can be edited. Confirm the transaction in your own bank account.')
ON DUPLICATE KEY UPDATE question=VALUES(question),options_json=VALUES(options_json),correct_answer=VALUES(correct_answer),explanation=VALUES(explanation);
