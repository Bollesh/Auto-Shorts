import json
import getpass
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

# 1. Load and Clean Data


load_dotenv()

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

def get_transcript_chunks(transcript, chunk_seconds, buffer_time=60):
    chunks = []
    current_chunk = []
    buffer = []
    current_start_time = transcript[0]['s']

    for item in transcript:
        # adding buffer
        if chunk_seconds - item['s'] <= buffer_time:
            buffer.append(item) 
        # If the current item's start time exceeds the chunk window
        if item['s'] - current_start_time > chunk_seconds:
            chunks.append(current_chunk)
            current_chunk = []
            for b_item in buffer:
                current_chunk.append(b_item)
            buffer = []
            current_start_time = item['s']
        current_chunk.append(item)
    
    # Add the final chunk
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def analyze_transcript():
    with open('transcript/transcript.json', 'r') as file:
        data = json.load(file)

    cleaned_transcript = [{"t": item["text"], "s": item["start"]} for item in data]
    chunks = get_transcript_chunks(cleaned_transcript, chunk_seconds=300)

    # llm = ChatOllama(
    #     model="ministral-3:8b",
    #     # model="qwen3:8b",
    #     temperature=0,
    #     # num_ctx=8192, # Smaller context per chunk is more stable
    #     format="json"
    # )

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=None,
        max_retries=2,
    )

    all_viral_clips = []

    # 3. Process each chunk
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        
        # We use a f-string to inject the chunk specifically
        prompt = f"""
            ### Task
            Identify 3-5 distinct viral segments from the provided transcript. 

            ### Critical Rules
            1. **Duration Constraint**: Every clip MUST be between 30 and 60 seconds. Clips can be longer than 60 seconds ONLY if they can retain user attention
            2. **Context Grounding**: Use only the provided transcript. Do not hallucinate external references.
            3. **No Duplicates**: Ensure each clip start/end is unique within this response.
            4. **Calculated Math**: Ensure (clip_end - clip_start) matches the duration field.
            5. **Strict format**: Return ONLY the JSON. NO preamble, NO summary, NO intro text, NO closing remarks. Start your response with [ and end with ].

            ### Viral Selection Rubric
            - **The Hook**: High energy or a statement that creates immediate curiosity.
            - **The Pivot**: A sudden change in the story or a "Wait, what?" moment.
            - **The Peak**: A moment of high emotion, laughter, or intense action.

            ### Response Format
            Return ONLY a JSON list. Do not include conversational text.
            [
            {{
                "clip_start": 0.00,
                "clip_end": 0.00,
                "duration": 0.00,
                "viral_type": "Peak/Hook/Pivot",
                "reasoning": "Under 15 words explaining the appeal",
                "transcript_quote": "The first sentence of the clip"
            }}
            ]

            ### Transcript Data
            {chunk}
        """
        
        try:
            response = llm.invoke(prompt)
            # Parse the string content back into a list
            print(response.content)
            clips = json.loads(response.content)  # type: ignore
            all_viral_clips.extend(clips)
        except Exception as e:
            print(f"Error in chunk {i}: {e}")

    # 4. Final Result
    print(json.dumps(all_viral_clips, indent=2))