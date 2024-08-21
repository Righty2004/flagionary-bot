# Flagionary Discord Bot

Flagionary is a Discord bot designed to provide a fun and educational experience by helping users learn country flags through a series of interactive rounds.

## Features
- **Fun and Educational**: Engage in a game where you guess country flags, promoting both fun and learning.
- **Interactive Rounds**: Start a new round and guess the flag within the time limit.
- **Hints and Skips**: Get hints or skip levels if you find the question too difficult.
- **Leaderboard**: Keep track of your progress and see how you rank among others.

## Commands
- `f.set`: Set the current channel for the bot to operate in.
- `f.remove`: Remove the current channel from the bot's list.
- `f.start`: Start a new round of flag guessing.
- `f.hint`: Get a hint for the current flag.
- `f.skip`: Skip the current level.
- `f.end`: End the current round.
- `f.help`: Display help information for all commands.
- `f.invite`: Get an invite link for the bot.

## Setup and Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Righty2004/flagionary-bot.git
    cd flagionary-bot
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your `flag_data.py`:
    - Ensure your `flag_data.py` file includes the `bot_token` variable:
    ```python
    flags = [['Afghanistan', 'AF'], ['Albania', 'AL'], ... ]  # Add all the flags and their country codes here

    bot_token = 'YOUR_BOT_TOKEN_HERE'
    ```

5. Run the bot:
    ```bash
    python flag_main.py
    ```

## Usage
- Add the bot to your Discord server using the invite link generated by the `f.invite` command.
- Set a channel for the bot using `f.set`.
- Start a round using `f.start` and begin guessing the flags.
- Use `f.hint` and `f.skip` to assist you in difficult levels.
- End the round anytime using `f.end`.

## Contributing
Feel free to fork this repository and make any improvements or additions. Pull requests are welcome.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any questions or suggestions, feel free to open an issue or contact me directly.

Enjoy learning flags with Flagionary!
