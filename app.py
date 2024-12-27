from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from subprocess import run, CalledProcessError
import os
from DCE.src.document_content_extraction.document_content_extraction import DocumentContentExtraction
from fastapi.responses import ORJSONResponse
import logging