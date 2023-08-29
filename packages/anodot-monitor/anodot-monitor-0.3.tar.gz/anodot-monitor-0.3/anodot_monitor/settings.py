import os

settings = {
    "stack": os.getenv("STACK"),
    "anodotd.monitoring.url": os.getenv("ANODOTD_MONITORING_URL"),
    "anodotd.monitoring.token": os.getenv("ANODOTD_MONITORING_TOKEN"),
    "aws.ses.region": os.getenv("AWS_SES_REGION"),
}
