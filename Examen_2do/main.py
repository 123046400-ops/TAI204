from fastapi import FastAPI,status,HTTPException,Depends 
import asyncio
from typing import Optional
from pydantic import BaseModel ,Field
from typing import Optional

from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#instaccias de servidor 
