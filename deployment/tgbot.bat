for /f "delims== tokens=1,2" %%G in (./deployment/.env.dev) do set %%G=%%H
python -m app.tgbot
