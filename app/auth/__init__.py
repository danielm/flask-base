from flask import Blueprint, session, redirect, url_for, flash
from functools import wraps

auth = Blueprint('auth', __name__, url_prefix='/auth')

from . import views

# Simple decorator as only example
def protected_area(func):
  """Checks if user is logged in (keys exists in session)"""
  @wraps(func)
  def wrapper(*args, **kwargs):
    email = session.get('email')
    if not email:
      flash('You must login to access that area', 'warning')
      
      return redirect(url_for('auth.login'))
    
    return func(*args, **kwargs)

  return wrapper