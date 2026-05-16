# Algo Buddy
An AI assistant that helps you prepare for technical interviews by helping you learn common algorithms.

## How to run

1. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key**
   ```
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-key-here"

   # Windows (cmd)
   set OPENAI_API_KEY=your-key-here

   # macOS/Linux
   export OPENAI_API_KEY=your-key-here
   ```

3. **Start the server**
   ```
   python app.py
   ```

4. Open your browser to `http://localhost:5000`

## To run the tests

1. Activate virtual environment
2. Run `pytest eval/`
