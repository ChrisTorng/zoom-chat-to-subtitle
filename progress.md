1. Ask: 原始的 chat 輸入只有訊息發送時間，為了轉 srt 必須要有訊息開始及結束時間，請問 srt 的時間如何計算?
2. Agent: 小時重置的方法我要改掉。請抓輸入檔的資料夾名稱，裡面會包含會議開始時間。因此請將輸入檔內的實際時間，減掉會議開始時間，才當然 srt 檔中需要用的時間開始值。
3. Agent: 從資料夾名稱取得會議開始時間: 19:30:36
   ```
   Traceback (most recent call last):
   File "D:\Projects\GitHub\Cloned\zoom-chat-to-subtitle\main.py", line 43, in <module>
       zchat2srt.save_srt(file_name + '.srt')
   File "D:\Projects\GitHub\Cloned\zoom-chat-to-subtitle\module\ZoomChat2Srt.py", line 125, in save_srt
       f.write(f"{self.ts0[i].hours:02d}:{self.ts0[i].minutes:02d}:{self.ts0[i].seconds:02d},000  -->  {self.ts1[i].hours:02d}:{self.ts1[i].minutes:02d}:{self.ts1[i].seconds:02d},{ts1ms}")
               ^^^^^^^^^^^^^^^^^
   AttributeError: 'datetime.timedelta' object has no attribute 'hours'
   ```
4. Agent: 請將中文訊息包括註解均改為英文。
5. Agent: 增加可選擇的第二個參數，輸入開始時間字串，格式 h:m:s.f，若未輸入，才依資料夾名稱時間。若也沒有資料夾名稱時間，那就輸出錯誤訊息停止執行。
6. Agent:
   ```
   PS zoom-chat-to-subtitle> python main.py "...\2025-04-07 19.30.36 GitHub Copilot 進階實戰及策略 ( ChrisTorng )\chat.txt"  19:31:15
    usage: python main.py "uploads/meeting_saved_chat.txt"
    ZoomChat2Srt: error: unrecognized arguments: 19:31:15
   ```
7. Agent: 將所有中文都改為英文，包括註解。
8. Agent: 我要加入一個選擇性參數 -l，若未指定則為英文 (亦即不轉換)，若有指定 zh-tw，則額外執行轉換: "Replying to " 轉為 "回覆 "；"Reacted to \"*\" with ?" 轉為 "對 \"*\" 比 ?"

Claude Sonnet 4/Ask:
Claude Sonnet 3.7:
GPT-4.1:
9. 請更新 README.md，依目前的 main.py 功能補充參數，包括 -l 及讀取資料夾起始時間或輸入參數起始時間的機制。

Claude Sonnet 4/Agent:
10. 請更新 README.md，全部撰寫英文。依目前的 main.py 功能補充參數，包括 -l 及讀取資料夾起始時間或輸入參數起始時間的機制。