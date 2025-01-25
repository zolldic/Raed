# Raed  
**Empowering Change, Guiding Activism**  

Raed is a Telegram bot designed to empower activists, organizations, and civil society leaders. With a focus on guiding users through key tasks, the bot aims to support change-making efforts, foster collaboration, and provide tools to address social challenges.  

## Key Features  
- **Activist and Organization Support**: Tailored interactions for individuals and organizations.
- **Profile Uploads**: Easily upload organizational profiles in supported formats (PDF, DOCX, DOC).
- **Task Guidance**: Step-by-step guidance for analyzing problems, creating concept notes, or drafting full proposals.  
- **Custom Replies**: User-friendly messaging with clear instructions for each step.  

## Vision  
Raed aims to strengthen civil society in Sudan by leveraging technology to provide accessible tools for activist and societal improvement. It empowers users to address challenges in a structured and impactful way.

---

## Project Structure  

```
Raed/
├── bot/
│   ├── app.py                # Main entry point for running the bot
│   ├── config.py             # Configuration file for bot settings and API key
│   ├── handlers/             # Folder containing bot handler logic
│   │   ├── start_conversation.py  # Logic for handling the /start command
│   │   ├── user_type.py           # Handles user type selection
│   │   ├── choose_task.py         # Guides users to select tasks
│   │   ├── profile_upload.py      # Handles organizational profile uploads
│   │   └── fallbacks.py           # Handles fallback logic and cancellations
│   └── __init__.py           # Package initializer for the bot
├── tests/                    # Tests for ensuring bot functionality
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

---

## Installation  

### Prerequisites  
- Python 3.9 or later  
- Telegram bot token (obtainable via [BotFather](https://core.telegram.org/bots))  

### Steps  
1. Clone this repository:  
   ```bash
   git clone https://github.com/your-username/raed.git  
   cd raed  
   ```  

2. Install dependencies:  
   ```bash
   pip3 install -r requirements.txt  
   ```  

3. Set up your bot token:  
   - Add your bot token to the `.env` file under the variable `BOT_KEY`.

4. Run the bot:  
   ```bash
   python3 -m bot.app  
   ```  

---

## Usage  

### Start the Bot  
1. Launch the bot in Telegram using the `/start` command.  
2. Choose your user type:  
   - **Activist**: Access tools to analyze problems, create concept notes, or draft proposals.  
   - **Org**: Upload your organization’s profile and get customized guidance.  

### Handle Tasks  
- Choose a task like "Analyze a problem" to proceed with further actions guided by the bot.  
- Upload valid documents for organizational profiles in supported formats.  

---

## Logging  
Raed includes a robust logging system to monitor user interactions and track errors:  
- Logs critical events like invalid choices or unsupported file uploads.  
- Maintains a log history for debugging and analytics.  

Logs are stored in the `logs/` directory (configurable).  


---

## Contact  
For support, suggestions, or feedback, please contact:  
- **Email**: hi@mynameisali.tech
- **Telegram**: [Raed](https://t.me/YourBotUsername)  

  