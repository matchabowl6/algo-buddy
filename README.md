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

   You can also set OPENAI_API_KEY in `.env`

3. **Start the server**
   ```
   python app.py
   ```

   - If you are on macOS, you'll need to start the server over port 5001 to avoid conflicts with AirPlay. This can be achieved by running
   ```
   flask --app app.py run --port 5001
   ```

4. Open your browser to `http://localhost:5000`
   - If on macOS and running `app.py` on port 5001, open `http://localhost:5001` instead

## To run the tests

1. Activate virtual environment
2. Run `pytest eval/`
