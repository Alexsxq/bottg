name: Run Telegram Bot
on: [workflow_dispatch]

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Проверить файлы
        run: ls -la  # Покажет все файлы в папке
      - name: Install Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install python-telegram-bot
      - name: Run bot
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
        run: python bot.py
