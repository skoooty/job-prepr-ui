import streamlit as st
import io
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account


#Connecting Google Cloud account
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

#Voice to text
def transcribe(source):
    """Transcribe the given audio file from a local or bucket path
    transctipt = the full transctipt which should be used for emotion analysis
    web_transcript = sample transctipt with highest confidence to be shown on the web page"""
    with io.open(source, "rb") as audio_file:
        content = audio_file.read()

    #import ipdb; ipdb.set_trace()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.MP3,
                sample_rate_hertz=48000,
                language_code="en-US",
                audio_channel_count=1,
                enable_automatic_punctuation=True
                )
    client = speech.SpeechClient(credentials=credentials)
    response = client.recognize(config=config, audio=audio)
    best_alternative = speech.SpeechRecognitionAlternative()
    transcript = ''
    init_confidence=0

    web_transcript=""

    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript += best_alternative.transcript
        #import ipdb; ipdb.set_trace()
        confidence = best_alternative.confidence
        if confidence > init_confidence:
            init_confidence = confidence
            web_transcript = best_alternative.transcript
    return transcript, web_transcript
