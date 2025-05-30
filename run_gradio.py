import gradio as gr
import nemo.collections.asr as nemo_asr

print('Loading Parakeet model...')
model = nemo_asr.models.ASRModel.from_pretrained('nvidia/parakeet-tdt-0.6b-v2')
print('Model loaded successfully!')

def transcribe_audio(audio):
    if audio is None:
        return 'Please upload an audio file.'
    try:
        result = model.transcribe([audio])
        return result[0].text
    except Exception as e:
        return f'Error: {str(e)}'

with gr.Blocks(title='Parakeet ASR') as demo:
    gr.Markdown('# 🎙️ Parakeet-TDT-0.6B Speech to Text')
    gr.Markdown('Upload an audio file to get high-quality transcription.')
    
    audio_input = gr.Audio(type='filepath', label='Upload Audio')
    transcribe_btn = gr.Button('Transcribe', variant='primary')
    output_text = gr.Textbox(label='Transcription', lines=10)
    
    transcribe_btn.click(transcribe_audio, inputs=audio_input, outputs=output_text)

print('Starting web interface on http://localhost:7860')
demo.launch(server_name='0.0.0.0', server_port=7860) 