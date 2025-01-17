# Using Split.io with FastAPI

This tutorial demonstrates how to integrate Split.io with a FastAPI application. Split.io is a feature flagging and experimentation platform that allows you to control the rollout of features to your users.

## Prerequisites

- Python 3.7+
- FastAPI
- Split.io SDK
- dotenv for environment variable management

## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Create a virtual environment** and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:

   ```bash
   pip install fastapi uvicorn splitio-python-sdk python-dotenv
   ```

4. **Set up environment variables**:

   Create a `.env` file in the root of your project and add your Split.io API key:

   ```
   SPLIT_API_KEY=your_split_api_key_here
   ```

   Make sure your `.env` file is included in your `.gitignore` to keep your API key secure.

## Code Overview

### Split Client Singleton

The `SplitClientSingleton` class is responsible for initializing and managing the Split.io client.
