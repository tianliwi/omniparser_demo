from openai import OpenAI
import os
from PIL import Image
import base64
from mimetypes import guess_type

def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

baseurl = "https://api.openai.com/v1"

os.environ["OPENAI_API_BASE"] = baseurl
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

os_name = "Windows"
annotation_path = "demo_sample/word2_annotation.json"
annotation_content = ""
with open(annotation_path, "r") as file:
    annotation_content = file.read()

template_4ovision = f"""
You are using an {os_name} device.
You are able to use a mouse and keyboard to interact with the computer based on the given task and screenshot, as well as each screen element in text format.
You can only interact with the desktop GUI (no terminal or application menu access).
"""

template_omniparser = f"""
You are using an {os_name} device.
You are able to use a mouse and keyboard to interact with the computer based on the given task and screenshot, as well as each screen element in text format.
You can only interact with the desktop GUI (no terminal or application menu access).

You may be given some history plan and actions, this is the response from the previous loop.
You should carefully consider your plan base on the task, screenshot, and history actions.

Here is the list of all detected bounding boxes by IDs on the screen and their description:{annotation_content}

Your available "Next Action" only include:
- type: type a string of text.
- left_click: Describe the ui element to be clicked.
- enter: Press an enter key.
- escape: Press an ESCAPE key.
- hover: Describe the ui element to be hovered.
- scroll: Scroll the screen, you must specify up or down.
- press: Describe the ui element to be pressed.

Based on the visual information from the screenshot image and the detected bounding boxes, please determine the next action, the Box ID you should operate on, and the value (if the action is 'type') in order to complete the task. Note you should only choose the bounding Box that contains relavant text or icon ID to the user task. 

Output format:
```json
{{
    "Reasoning": str, # describe what is in the current screen, taking into account the history, then describe your step-by-step thoughts on how to achieve the task, choose one action from available actions at a time.
    "Next Action": "action_type, action description" | "None" # one action at a time, describe it in short and precisely. 
    'Box ID': n,
    'value': "xxx" # if the action is type, you should provide the text to type.
}}
```

One Example:
```json
{{  
    "Reasoning": "The current screen shows google result of amazon, in previous action I have searched amazon on google. Then I need to click on the first search results to go to amazon.com.",
    "Next Action": "left_click",
    'Box ID': m,
}}
```

Another Example:
```json
{{
    "Reasoning": "The current screen shows the front page of amazon. There is no previous action. Therefore I need to type "Apple watch" in the search bar.",
    "Next Action": "type",
    'Box ID': n,
    'value': "Apple watch"
}}
```

IMPORTANT NOTES:
1. You should only give a single action at a time.
2. You should give an analysis to the current screen, and reflect on what has been done by looking at the history, then describe your step-by-step thoughts on how to achieve the task.
3. Attach the next action prediction in the "Next Action".
4. You should not include other actions, such as keyboard shortcuts.
5. When the task is completed, you should say "Next Action": "None" in the json field.
"""

image_path = "./demo_sample/word2_origin.png"
image = Image.open(image_path)
image_data = local_image_to_data_url(image_path)

chat_completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": template_omniparser,
        },
        {
            "role": "user",
            "content":  [
	            {
	                "type": "text",
	                "text": "How do I insert a watermark?"
	            },
	            {
	                "type": "image_url",
	                "image_url": {
                        "url": image_data,
                        "detail": "high"
                    }
                } 
            ]
        }
    ]
)

print(chat_completion.choices[0].message.content)