import collections, queue
import deepspeech
import pyaudio
import wave
import numpy as np
import multiprocessing
import threading
from webrtcvad import Vad
from datetime import datetime
from typing import List, Optional
from multiprocessing.connection import PipeConnection
from enum import Enum


from blue_st_sdk.utils.number_conversion import LittleEndian
from ..models import AudioSource, HotWord, TSpeech, TSpeechCommand, TSpeechObject, TSpeechCommandEnum, Voice

def millis():
    return datetime.now()


class TStreamStatus(Enum):
    STREAMING = 1
    STOPPED = 2

class TAudio:

    sample_rate: int = 16000
    frame_duration: int = 20
    tskin_frame_length: int = 80 // 2 # packet length is 80, but we have 2 bits per packet!
    frame_per_seconds: int = 50
    frame_buffer_length: int

    audio_source: AudioSource
    is_running: bool
    in_pipe: Optional[PipeConnection]
    buffer_queue: queue.Queue
    pa: pyaudio.PyAudio
    stream_status: TStreamStatus
    block_size: int

    thread: threading.Thread
    stream: pyaudio.Stream

    def __init__(self, in_pipe: Optional[PipeConnection], audio_source: AudioSource):
        self.audio_source = audio_source
        self.is_running = True
        self.in_pipe = in_pipe
        self.frame_buffer_length = self.sample_rate * self.frame_duration // 1000 // self.tskin_frame_length

        self.buffer_queue = queue.Queue()
        self.pa = pyaudio.PyAudio()
        self.stream_status = TStreamStatus.STOPPED

        if self.audio_source == AudioSource.TSKIN:
            self.thread = threading.Thread(target=self.tskin_audio)
            self.thread.start()
        else:
            def stream_callback(in_data, f_count, t_info, st):
                self.buffer_queue.put(in_data)
                return (None, pyaudio.paContinue)

            self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=int(self.sample_rate / self.frame_per_seconds),
                stream_callback=stream_callback,
                start=False
            )  

    def tskin_audio(self):

        if self.in_pipe is None: 
            raise TypeError("Audio source is TSKIN but no pipe is provided")

        n_buffer = 0
        data = b''
        while self.is_running:
            if not self.in_pipe.poll(2):
                if self.stream_status == TStreamStatus.STREAMING: 
                    raise TimeoutError("Audio source is TSKIN but no audio is streaming from TSkin")
                continue

            pipe_data = self.in_pipe.recv()
            if self.stream_status == TStreamStatus.STREAMING or n_buffer > 0:
                data += b''.join([LittleEndian.int16_to_bytes(d) for d in pipe_data])
                n_buffer += 1
                if not n_buffer < self.frame_buffer_length:
                    self.buffer_queue.put(data)
                    data = b''
                    n_buffer = 0

    def start_stream(self):
        if self.audio_source == AudioSource.TSKIN:
            self.stream_status = TStreamStatus.STREAMING
        else:
            self.stream.start_stream()

    def stop_stream(self):
        if self.audio_source == AudioSource.TSKIN:
            self.stream_status = TStreamStatus.STOPPED
        else:
            self.stream.stop_stream()

    def read(self):
        return self.buffer_queue.get()

    def play(self, audio_file):
        with wave.open(audio_file,"rb") as f:
            chunk = 1024

            if self.audio_source == AudioSource.MIC and self.stream.is_active():
                self.stream.stop_stream()

            audio_stream = self.pa.open(
                format=self.pa.get_format_from_width(f.getsampwidth()),
                channels=f.getnchannels(),
                rate=f.getframerate(),
                output=True
            )

            data = f.readframes(chunk)

            while data:
                audio_stream.write(data)
                data = f.readframes(chunk)

            audio_stream.stop_stream()
            audio_stream.close()

    def destroy(self):
        self.is_running = False
        if self.audio_source == AudioSource.TSKIN:
            self.thread.join(1.0)
        else:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
        self.pa.terminate()

class TDeepSpeech(TAudio):

    config: Voice

    # vad_aggressiveness: int = 3
    # vad_padding_ms: int = 800
    # vad_ratio: float = 0.6
    # beam_width: int = 1024

    # model_file: str
    model: deepspeech.Model

    # scorer_file: Optional[str]
    
    # voice_timeout: int = 10
    # silence_timeout: int = 5

    has_been_stopped: bool = False

    def __init__(self, pipe: PipeConnection, adpcm_pipe: Optional[PipeConnection], audio_source: AudioSource, config: Voice):
        self.config = config
        super().__init__(adpcm_pipe, audio_source)
        self.vad = Vad(self.config.vad_aggressiveness)
        self.config = config
        # model_file = config.get("model")
        # scorer_file = config.get("scorer")
        # self.silence_timeout = config.get("silence_timeout")
        # self.voice_timeout = config.get("voice_timeout")

        # self.model_file = path.join(CONFIG_FILES_DIR, model_file)
        self.model = deepspeech.Model(self.config.model_full_path)

        if self.config.scorer_full_path:
            self.model.enableExternalScorer(self.config.scorer_full_path)
            self.model.setBeamWidth(self.config.beam_width)

        self.pipe = pipe
        self.run()
        self.destroy()
    
    def is_timeout(self, tick: datetime, timeout: int):
        return (millis() - tick).total_seconds() > timeout

    def vad_collector(self):
        ticks = millis()
        num_padding_frames: int = int(self.frame_per_seconds * (self.config.vad_padding_ms / 1000))
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False

        while True:

            if self.pipe.poll():
                cmd: TSpeechCommand = self.pipe.recv()
                if type(cmd) == TSpeechCommand and cmd.command_type == TSpeechCommandEnum.STOP:
                    self.has_been_stopped = True
                    break

            frame = self.read()
            is_speech = self.vad.is_speech(frame, self.sample_rate)

            if not triggered:
                if self.is_timeout(ticks, self.config.silence_timeout): raise TimeoutError()

                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced >= (self.config.vad_ratio * num_padding_frames):
                    triggered = True
                    ticks = millis()
                    for f, s in ring_buffer:
                        yield f
                    ring_buffer.clear()

            else:
                if self.is_timeout(ticks, self.config.voice_timeout):
                    ring_buffer.clear()
                    break

                yield frame
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                if num_unvoiced >= (self.config.vad_ratio * num_padding_frames):
                    ring_buffer.clear()
                    break
        yield None

    def run(self):
        while True:
            if self.pipe.poll(0.1):
                cmd: TSpeechCommand = self.pipe.recv()
                if not type(cmd) == TSpeechCommand:
                    continue

                if cmd.command_type == TSpeechCommandEnum.LISTEN and cmd.speech_tree != None:
                    result = None
                    try:
                        result = self.stt(cmd.speech_tree)
                    except TimeoutError as e:
                        result = e
                    finally:
                        self.stop_stream()
                        if not self.has_been_stopped:
                            self.pipe.send(result)
                        else:
                            self.has_been_stopped = False
                elif cmd.command_type == TSpeechCommandEnum.PLAY:
                    try:
                        self.play(cmd.audio_file)
                        cmd.set_ack()
                    except:
                        print("File not found")
                    finally:
                        self.pipe.send(cmd)
                elif cmd.command_type == TSpeechCommandEnum.END:
                    break
                else:
                    print("error")

    def stt(self, speech_tree: TSpeechObject):
        frames = self.vad_collector()

        text_so_far = ""
        self.tree_path: List[HotWord] = []
        self.current_branch: List[TSpeech] = speech_tree.t_speech
        self.word_list: List[str] = []
        time_inference = 0

        self.model.clearHotWords()
        stt_stream = self.model.createStream()
        self.start_stream()

        print("listening")
        
        for frame in frames:
            if frame is None:
                break

            delta = millis()
            data16 = np.frombuffer(frame, dtype='int16')
            self.model.clearHotWords()

            for hw_obj in self.current_branch:
                for hotword in hw_obj.hotwords:
                    # print(hotword)
                    self.model.addHotWord(hotword.word, hotword.boost)
            if self.config.stop_hotword:
                self.model.addHotWord(self.config.stop_hotword.word, self.config.stop_hotword.boost)

            stt_stream.feedAudioContent(data16)
            text = stt_stream.intermediateDecode()

            if text != text_so_far:
                print(text)
                text_so_far = text

                self.word_list = list(filter(lambda t: len(t) > 1 , text.split(" ")))
                self.check_branch()

            delta = millis() - delta
            time_inference = time_inference + delta.total_seconds()

        text_so_far = stt_stream.finishStream()

        return " ".join(w for w in self.word_list), self.tree_path, time_inference

    def check_branch(self):
        if self.config.stop_hotword and self.config.stop_hotword.word in self.word_list[-2::]:
            self.tree_path.append(self.config.stop_hotword)
            return

        for tspeech in self.current_branch:
            for hotword in tspeech.hotwords:
                if hotword.word in self.word_list[-2::]:
                    self.tree_path.append(hotword)
                    self.current_branch = tspeech.children.t_speech if tspeech.children else []
                    return
        return

class Tactigon_Speech:
    def __init__(self, 
                 config: Voice,
                 pipe: PipeConnection, 
                 adpcm_pipe: Optional[PipeConnection] = None, 
                 audio_source: Optional[AudioSource] = AudioSource.TSKIN):
        self.process = multiprocessing.Process(target=TDeepSpeech, args=(pipe, adpcm_pipe, audio_source, config))
    
    def start(self):
        self.process.start()

    def terminate(self):
        self.process.terminate()

def test_tree(tree: TSpeechObject, voice_pipe: PipeConnection):

    voice_pipe.send(
        TSpeechCommand.listen(tree)
    )

    if not voice_pipe.poll(20):
        voice_pipe.send(
            TSpeechCommand.stop()
        )
        return [None]

    result = voice_pipe.recv()
    
    if type(result) == TimeoutError:
        # print("voice timeout")
        return []

    transcript, tree_path, inference = result

    if tree_path and tree_path[-1] == HotWord("exit"):
        # print("stop word, esco")
        return [None]

    filtered_tree = filter_tree(tree, tree_path)

    if filtered_tree:
        print("Ho capito", tree_path)
        print("Mi mancano le seguenti possibilità")

        for b in filtered_tree.t_speech:
            for hw in b.hotwords:
                print("----" + hw.word)

        print("\nfeedback", filtered_tree.feedback)

        return tree_path + test_tree(filtered_tree, voice_pipe)

    return tree_path

def filter_tree(tree: TSpeechObject, tree_path: List[HotWord]) -> TSpeechObject:
    if not tree_path:
        return tree

    print(tree_path)
    node, *rest = tree_path

    branches = [branch.children for branch in tree.t_speech if node in branch.hotwords]

    if not branches:
        return tree

    filtered_tree, *_ = branches

    if not filtered_tree:
        return tree

    return filter_tree(filtered_tree, rest)

# def get_wav(filename: str, framerate: int = 16000):
#     wf = wave.open(filename, "w")
#     wf.setnchannels(1)
#     wf.setsampwidth(2)
#     wf.setframerate(framerate)
#     return wf

# if __name__ == "__main__":
#     import json
#     from os import path
#     from ..hal.Tactigon_BLE import BLE

#     with open(path.join(path.dirname(__file__), "config_files", "voice.json")) as voice_file:
#         voice: Voice = Voice.FromJSON(json.load(voice_file))

#     adpcm_rx, adpcm_tx = multiprocessing.Pipe(duplex=False)
#     button_rx, button_tx = multiprocessing.Pipe(duplex=False)
#     ble = BLE("RIGHT", "C0:83:38:32:55:36", adpcm_pipe=adpcm_tx, button_pipe=button_tx)
#     ble.select_sensors()
#     ble.start()

#     while not ble.get_connection_status():
#         pass

#     p1, p2 = multiprocessing.Pipe()
#     t_s = Tactigon_Speech(voice, p2, adpcm_pipe=adpcm_rx, audio_source=AudioSource.MIC)
#     t_s.start()

#     button: Optional[int] = None


#     while True:
#         if button_rx.poll(0.5):
#             button = button_rx.recv()[0]

#             if button == 4:
#                 print("start voce")
#                 # ble.select_voice()
#                 p1.send(
#                     TSpeechCommand.play("D:\\projects\\TSkin\\TGear_SDK\\src\\applications\\application_rhino\\voices\\command_ok.wav")
#                 )
                
#                 if p1.poll(10):
#                     _ = p1.recv()

#                 d = test_tree(
#                     TSpeechObject(
#                         [TSpeech(
#                             [HotWord("draw")],
#                             children=TSpeechObject(
#                                 [
#                                     TSpeech(
#                                         [HotWord("circle")]
#                                     ),
#                                     TSpeech(
#                                         [HotWord("cone")]
#                                     ),
#                                 ]
#                             )
#                         )],
#                         "draw"
#                     )
#                     , p1
#                 )

#                 print(d)

#                 print("stop voce")
#                 # ble.select_sensors()

#                 while button_rx.poll():
#                     _ = button_rx.recv()

#             if button == 1:
#                 print("Exit")
#                 break

#     t_s.terminate()
#     ble.terminate()
    