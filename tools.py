from flask_sqlalchemy import SQLAlchemy
import datetime

# Add this at the top with other imports
from typing import Dict, Any, Optional, List
import requests
import json

db = SQLAlchemy()


# Define the data model
class APIData(db.Model):
    """Model for storing API response data"""
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    response_data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    method = db.Column(db.String(10), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)

def fetch_and_save_data(
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
    """
    Fetch data from API and save to SQLite database.
    
    Args:
        url (str): The API endpoint URL
        method (str): HTTP method (GET, POST, PUT, DELETE)
        headers (Dict[str, str], optional): Request headers
        params (Dict[str, Any], optional): Query parameters
        body (Dict[str, Any], optional): Request body for POST/PUT
        timeout (int): Request timeout in seconds
        
    Returns:
        Dict[str, Any]: Response data and database record ID
    """
    try:
        # First fetch the data using existing fetch_data function
        response_data = fetch_data(
            url=url,
            method=method,
            headers=headers,
            params=params,
            body=body,
            timeout=timeout
        )
        
        # Create new database record
        api_data = APIData(
            url=url,
            response_data=response_data,
            method=method.upper(),
            status_code=200  # We know it's successful if we got here
        )
        
        # Save to database
        db.session.add(api_data)
        db.session.commit()
        
        return {
            "success": True,
            "data": response_data,
            "db_record_id": api_data.id,
            "saved_at": api_data.created_at.isoformat()
        }
        
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error saving API data: {str(e)}")