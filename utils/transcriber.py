import whisper
import srt
import datetime

def transcribe_and_generate_srt(input_path,output_path):
    model=whisper.load_model("base")
    results=model.transcribe(input_path)
    segments=results["segments"]
    subtitles=[]
    for i, seg in enumerate(segments):
        subtitles.append(srt.Subtitle(
            index=i+1,
            start=datetime.timedelta(seconds=seg["start"]),
            end=datetime.timedelta(seconds=seg["end"]),
            content=seg["text"].strip()
        ))
    with open(output_path, 'w') as f:
        f.write(srt.compose(subtitles))