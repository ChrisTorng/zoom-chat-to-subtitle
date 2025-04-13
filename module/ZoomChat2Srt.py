import re
import os
import sys
from datetime import datetime, date, time, timedelta

class ZoomChat2Txt:
    def __init__(self, file_path, start_time_str=None, language=None):
        self.text = ''
        self.start_hour = None
        self.start_minute = None
        self.start_second = None
        self.start_time_str = start_time_str
        self.meeting_start_time = None
        self.file_path = file_path
        self.language = language
        self.ts0 = [] # timestamp start
        self.ts1 = [] # timestamp end
        self.delays = [] # t1 - t2 in ms
        self.users = []
        self.messages = []
        self.load_file(file_path)
        
    def parse_start_time_str(self):
        """Parse start time string in format h:m:s.f"""
        try:
            # Split by colon for hours, minutes, seconds
            parts = self.start_time_str.split(':')
            if len(parts) != 3:
                print(f"Invalid time format: {self.start_time_str}, should be h:m:s.f")
                return False
                
            hours = int(parts[0])
            minutes = int(parts[1])
            
            # Handle seconds with optional milliseconds
            if '.' in parts[2]:
                seconds_parts = parts[2].split('.')
                seconds = int(seconds_parts[0])
                # We don't use milliseconds in this implementation
            else:
                seconds = int(parts[2])
                
            self.start_hour = hours
            self.start_minute = minutes
            self.start_second = seconds
            self.meeting_start_time = time(hours, minutes, seconds)
            print(f"Using provided start time: {hours:02d}:{minutes:02d}:{seconds:02d}")
            return True
        except Exception as e:
            print(f"Error parsing start time: {e}")
            return False
            
    def set_start_hour(self):
        # First try to use the provided start_time_str if available
        if self.start_time_str and self.parse_start_time_str():
            return
            
        # Next try to get meeting start time from folder name
        if self.extract_meeting_start_time():
            return
            
        # If both methods failed, show error and exit
        print("Error: Unable to determine start time. Please provide a start time parameter or ensure the folder name contains time information.")
        sys.exit(1)
    
    def extract_meeting_start_time(self):
        """Extract meeting start time from the folder name in the file path"""
        try:
            # Get directory name of the input file
            dir_name = os.path.basename(os.path.dirname(self.file_path))
            
            # Use regex to extract time from folder name (format: HH.MM.SS)
            time_pattern = re.search(r'(\d{1,2})[.](\d{1,2})(?:[.](\d{1,2}))?', dir_name)
            if time_pattern:
                self.start_hour = int(time_pattern.group(1))
                self.start_minute = int(time_pattern.group(2))
                self.start_second = int(time_pattern.group(3) or 0)  # If no seconds available, default to 0
                self.meeting_start_time = time(self.start_hour, self.start_minute, self.start_second)
                print(f"Got meeting start time from folder name: {self.start_hour}:{self.start_minute}:{self.start_second}")
                return True
            return False
        except Exception as e:
            print(f"Error extracting meeting start time: {e}")
            return False
    
    def extract_ts0(self):
        temp = re.findall("(\d{2}:\d{2}:\d{2})\s.+?:", self.text)
        for t in temp:
            self.ts0.append(self.txt_to_time(t))
         
    def translate_message(self, message):
        """
        翻譯訊息中的特定英文模式為中文
        - "Replying to " 轉為 "回覆 "
        - "Reacted to \"*\" with ?" 轉為 "對 \"*\" 比 ?"
        """
        if self.language != 'zh-tw':
            return message
            
        # 替換 "Replying to " 為 "回覆 "
        message = re.sub(r'Replying to ', r'回覆 ', message)
        
        # 替換 "Reacted to "*" with ?" 為 "對 "*" 比 ?"
        message = re.sub(r'Reacted to "(.*?)" with (.*)', r'對 "\1" 比 \2', message)
        
        return message
        
    def extract_messages(self):
        messages = re.split("\d{2}:\d{2}:\d{2}\s.+?:", self.text)
        messages.pop(0) # remove the first empty element
        # 對每個訊息套用語言翻譯
        self.messages = [self.translate_message(m.strip()) for m in messages]
        
    def extract_users(self):
        users = re.findall("\d{2}:\d{2}:\d{2}\s(.+?):", self.text)
        self.users = [user.strip() for user in users]
    
    def load_file(self, file_path):
        f = open(file_path, 'r', encoding='utf-8')
        text = f.readlines()
        self.text = ''.join(text)
        self.extract_messages()
        self.extract_ts0()
        self.extract_users()
        self.set_start_hour()
        self.reset_hour()
        self.generate_delays()
        self.generate_ts1()
    
    # Reset message timestamps by subtracting meeting start time
    def reset_hour(self):
        if not self.meeting_start_time:
            # If no meeting start time available, use the old method
            for i in range(len(self.ts0)):
                self.ts0[i] -= timedelta(hours=self.start_hour)
            return
            
        # Reset using meeting start time
        meeting_start_datetime = datetime.combine(date.today(), self.meeting_start_time)
        for i in range(len(self.ts0)):
            # Calculate difference between each message and meeting start time
            self.ts0[i] = self.ts0[i] - meeting_start_datetime
    
    # input: text
    # return: datetime object
    def txt_to_time(self, text):
        h, m, s = (int(part) for part in text.split(":"))
        t = time(h,m,s)
        return datetime.combine(date.today(), t)
    
    # input: datetime: ts0
    # return: datetime object: ts0 + ms
    def generate_ts1(self):
        for i, t in enumerate(self.ts0):
            self.ts1.append(t + timedelta(milliseconds=self.delays[i]))
        
    # input single message
    # return delay time in ms
    def generate_delays(self):
        for i in range(len(self.messages)):
            text_list = re.split("\s", self.messages[i])
            result = len(text_list) * 1000
            if result > 5000:
                result = 5000
            self.delays.append(result)
            
    def display_result(self, elements=5):
        for i in range(min(elements, len(self.users))):
            # Process timedelta object, calculate hours, minutes, seconds from total seconds
            ts0_seconds = int(self.ts0[i].total_seconds())
            ts0_hours = ts0_seconds // 3600
            ts0_minutes = (ts0_seconds % 3600) // 60
            ts0_seconds = ts0_seconds % 60
            
            ts1_seconds = int(self.ts1[i].total_seconds())
            ts1_hours = ts1_seconds // 3600
            ts1_minutes = (ts1_seconds % 3600) // 60
            ts1_seconds = ts1_seconds % 60
            
            # Get milliseconds
            ts1ms = f"{int(self.ts1[i].microseconds / 1000):03d}"
            
            print(i+1)
            print(f"{ts0_hours:02d}:{ts0_minutes:02d}:{ts0_seconds:02d},000  -->  {ts1_hours:02d}:{ts1_minutes:02d}:{ts1_seconds:02d},{ts1ms}")
            message = self.messages[i]

            print(f"{self.users[i]}: {message}", end="\n\n")
            
    def save_srt(self, file_path):
        with open(file_path, 'w+', encoding='utf-8') as f:
            for i in range(len(self.users)):
                # Process timedelta object, calculate hours, minutes, seconds from total seconds
                ts0_seconds = int(self.ts0[i].total_seconds())
                ts0_hours = ts0_seconds // 3600
                ts0_minutes = (ts0_seconds % 3600) // 60
                ts0_seconds = ts0_seconds % 60
                
                ts1_seconds = int(self.ts1[i].total_seconds())
                ts1_hours = ts1_seconds // 3600
                ts1_minutes = (ts1_seconds % 3600) // 60
                ts1_seconds = ts1_seconds % 60
                
                # Get milliseconds
                ts1ms = f"{int(self.ts1[i].microseconds / 1000):03d}"
                
                f.write(str(i+1))
                f.write("\n")
                f.write(f"{ts0_hours:02d}:{ts0_minutes:02d}:{ts0_seconds:02d},000  -->  {ts1_hours:02d}:{ts1_minutes:02d}:{ts1_seconds:02d},{ts1ms}")
                f.write("\n")
                f.write(f"{self.users[i]}: {self.messages[i]}")
                f.write("\n")
                f.write("\n")
            f.close()
        print(f"Success exporting srt files: {file_path}")