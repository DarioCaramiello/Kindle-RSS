import logging
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv


logger = logging.getLogger(__name__)


def load_email_configuration() -> dict:
    """
    Load SMTP and Kindle email configuration
    from environment variables.

    Returns:
        Dictionary containing SMTP configuration.

    Raises:
        ValueError: If one or more required variables are missing.
    """

    load_dotenv()

    required_variables = [
        "SMTP_HOST",
        "SMTP_PORT",
        "SMTP_USERNAME",
        "SMTP_PASSWORD",
        "KINDLE_EMAIL",
    ]

    missing_variables = []

    for variable in required_variables:
        if not os.getenv(variable):
            missing_variables.append(variable)

    if missing_variables:
        raise ValueError(
            "Missing environment variables: "
            + ", ".join(missing_variables)
        )

    return {
        "smtp_host": os.environ["SMTP_HOST"],
        "smtp_port": int(os.environ["SMTP_PORT"]),
        "smtp_username": os.environ["SMTP_USERNAME"],
        "smtp_password": os.environ["SMTP_PASSWORD"],
        "kindle_email": os.environ["KINDLE_EMAIL"],
    }
def send_to_kindle(epub_path: str) -> None:
    """
    Send an EPUB file to the configured Kindle
    Send-to-Kindle email address.

    Args:
        epub_path: Path to the EPUB file.

    Raises:
        FileNotFoundError: If the EPUB file does not exist.
        ValueError: If the email configuration is incomplete.
        smtplib.SMTPException: If sending fails.
    """

    file_path = Path(epub_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"EPUB file not found: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"EPUB path is not a file: {file_path}"
        )

    config = load_email_configuration()

    logger.info(
        "Preparing Kindle delivery for: %s",
        file_path.name,
    )

    message = EmailMessage()

    message["From"] = config["smtp_username"]
    message["To"] = config["kindle_email"]
    message["Subject"] = file_path.stem

    message.set_content(
        "Automatically generated personal newspaper."
    )

    with file_path.open("rb") as epub_file:
        epub_data = epub_file.read()

    message.add_attachment(
        epub_data,
        maintype="application",
        subtype="epub+zip",
        filename=file_path.name,
    )

    logger.info(
        "Connecting to SMTP server %s:%d",
        config["smtp_host"],
        config["smtp_port"],
    )

    with smtplib.SMTP(
        config["smtp_host"],
        config["smtp_port"],
        timeout=30,
    ) as smtp:

        smtp.ehlo()

        smtp.starttls()

        smtp.ehlo()

        smtp.login(
            config["smtp_username"],
            config["smtp_password"],
        )

        smtp.send_message(
            message
        )

    logger.info(
        "EPUB successfully sent to Kindle: %s",
        config["kindle_email"],
    )