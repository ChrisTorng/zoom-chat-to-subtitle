from module.ZoomChat2Srt import ZoomChat2Txt
import argparse

parser = argparse.ArgumentParser(
  prog = "ZoomChat2Srt",
  description = "Convert Zoom chat text file into subtitle srt file",
  usage="python main.py \"uploads/meeting_saved_chat.txt\" [start_time]"
)

parser.add_argument(
  '-o',
  '--output-path',
  type= str,
  help= "Optional output file_path"
)

parser.add_argument(
  '-l',
  '--language',
  type= str,
  default= None,
  help= "Optional language code, e.g. zh-tw for Traditional Chinese translation"
)

parser.add_argument(
  metavar="file_path",
  type=str,
  dest="file_path",
  help="location (file path) of the zoom chat txt file"
)

parser.add_argument(
  "start_time",
  nargs="?",  # Make this parameter optional
  type=str,
  default=None,
  help="Optional start time in format h:m:s.f (e.g. 19:31:15)"
)

def split_filename_and_ext(file_path):
  *file_name, ext = file_path.split('.')
  file_name = '.'.join(file_name)
  
  return file_name, ext
  
if __name__ == "__main__":
  args = parser.parse_args()
  file_name, ext = split_filename_and_ext(args.file_path)
  if ext.lower() != 'txt':
    raise Exception("Sorry, this app supports txt file only. Please check your file extension")
  zchat2srt = ZoomChat2Txt(args.file_path, args.start_time, args.language)

  if args.output_path:
    file_name, ext = split_filename_and_ext(args.output_path)
    if ext.lower() != 'srt':
      raise Exception("Sorry, this app supports exporting srt file only. Please check your file extension")
  
  zchat2srt.save_srt(file_name + '.srt')





