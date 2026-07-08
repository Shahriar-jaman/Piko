
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Email configuration
EMAIL_ADDRESS = 'shahriarnayem001@gmail.com'
EMAIL_PASSWORD = 'Shahriar@001'
RECIPIENT_EMAIL = 'shahriarnayem001@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# URL for ESP32-CAM (single image for detection)
url = 'http://192.168.55.77/