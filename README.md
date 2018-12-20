## Отображатор графика с амплитудным спектром текущего звука.

**Необходимо**
- python3
- pip
- virualenv

**Run on Ubuntu**
```
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python3 main.py
```


**После запуска**
- в PulseAudio перейти на вкладку 'Recording' 
- выставить для приложения Monitor of Built-in Audio Analog Stereo (или что-нибудь такое)
