import threading
import time

from audio.recorder import record_continuously


stop_event = threading.Event()


recording_thread = threading.Thread(
    target=record_continuously,
    kwargs={
        "output_directory": "audio/recordings",
        "chunk_duration": 60,
        "stop_event": stop_event
    }
)

recording_thread.start()

print()
print("⏱️ Test will run for 15 seconds...")
print()

time.sleep(15)

print()
print("🛑 Sending stop signal...")
stop_event.set()

recording_thread.join()

print()
print("✅ Recorder test finished.")