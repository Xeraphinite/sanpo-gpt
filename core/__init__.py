import sys
sys.path.append('.')

from core.exam import (
  Exam,
  MultipleChoice,
)

from core.load_files import load_files

__all__ = [
  'MultipleChoice',
  'Exam',
  'load_files',
]