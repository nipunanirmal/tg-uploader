#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for type-safe operations and data handling
"""

import logging

logger = logging.getLogger(__name__)

def safe_int(value, default=0):
    """
    Safely convert a value to integer
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        int: Converted integer or default value
    """
    if value is None:
        return default
    
    try:
        if isinstance(value, (int, float)):
            return int(value)
        elif isinstance(value, str):
            # Handle string representations of numbers
            if value.strip() == "":
                return default
            return int(float(value))  # Handle strings like "123.0"
        else:
            return default
    except (ValueError, TypeError, OverflowError):
        return default

def safe_float(value, default=0.0):
    """
    Safely convert a value to float
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        float: Converted float or default value
    """
    if value is None:
        return default
    
    try:
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, str):
            # Handle string representations of numbers
            if value.strip() == "":
                return default
            return float(value)
        else:
            return default
    except (ValueError, TypeError, OverflowError):
        return default

def safe_compare_greater(value1, value2, convert_to='float'):
    """
    Safely compare if value1 > value2 with type conversion
    
    Args:
        value1: First value to compare
        value2: Second value to compare
        convert_to: Type to convert to ('int' or 'float')
        
    Returns:
        bool: True if value1 > value2, False otherwise
    """
    try:
        if convert_to == 'int':
            v1 = safe_int(value1)
            v2 = safe_int(value2)
        else:
            v1 = safe_float(value1)
            v2 = safe_float(value2)
        
        return v1 > v2
    except Exception as e:
        logger.warning(f"Safe comparison failed: {e}")
        return False

def safe_compare_greater_equal(value1, value2, convert_to='float'):
    """
    Safely compare if value1 >= value2 with type conversion
    
    Args:
        value1: First value to compare
        value2: Second value to compare
        convert_to: Type to convert to ('int' or 'float')
        
    Returns:
        bool: True if value1 >= value2, False otherwise
    """
    try:
        if convert_to == 'int':
            v1 = safe_int(value1)
            v2 = safe_int(value2)
        else:
            v1 = safe_float(value1)
            v2 = safe_float(value2)
        
        return v1 >= v2
    except Exception as e:
        logger.warning(f"Safe comparison failed: {e}")
        return False

def sanitize_format_data(format_dict):
    """
    Sanitize format data to ensure all numeric fields are properly typed
    
    Args:
        format_dict: Dictionary containing format information
        
    Returns:
        dict: Sanitized format dictionary
    """
    if not isinstance(format_dict, dict):
        return format_dict
    
    # Create a copy to avoid modifying the original
    sanitized = format_dict.copy()
    
    # Fields that should be numeric
    numeric_fields = [
        'filesize', 'filesize_approx', 'tbr', 'abr', 'vbr', 
        'width', 'height', 'fps', 'duration', 'view_count',
        'like_count', 'dislike_count', 'average_rating'
    ]
    
    for field in numeric_fields:
        if field in sanitized:
            if field in ['width', 'height', 'fps', 'view_count', 'like_count', 'dislike_count']:
                # These should be integers
                sanitized[field] = safe_int(sanitized[field])
            else:
                # These can be floats
                sanitized[field] = safe_float(sanitized[field])
    
    return sanitized

def sanitize_formats_list(formats_list):
    """
    Sanitize a list of format dictionaries
    
    Args:
        formats_list: List of format dictionaries
        
    Returns:
        list: List of sanitized format dictionaries
    """
    if not isinstance(formats_list, list):
        return formats_list
    
    return [sanitize_format_data(fmt) for fmt in formats_list]

def format_file_size(size_bytes, default="Unknown size"):
    """
    Format file size in bytes to human readable format
    
    Args:
        size_bytes: Size in bytes
        default: Default string if size is invalid
        
    Returns:
        str: Formatted size string
    """
    size = safe_float(size_bytes)
    
    if size <= 0:
        return default
    
    # Convert to MB
    size_mb = size / (1024 * 1024)
    
    if size_mb < 1:
        return f"{size / 1024:.1f} KB"
    elif size_mb < 1024:
        return f"{size_mb:.1f} MB"
    else:
        return f"{size_mb / 1024:.1f} GB"
