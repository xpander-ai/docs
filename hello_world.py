#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple Hello World Python script.
Created for the xpander-ai/docs repository.
"""

def hello_world():
    """
    Print a greeting to the world.
    
    Returns:
        str: A greeting message
    """
    return "Hello, World!"

def main():
    """
    Main function to execute when the script is run.
    """
    message = hello_world()
    print(message)

if __name__ == "__main__":
    main()