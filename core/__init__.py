"""Core package initialization."""

from .config import config
from .email_parser import EmailParser
from .email_sender import EmailSender, EmailSendResult

__all__ = ['config', 'EmailParser', 'EmailSender', 'EmailSendResult']
