from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3
import re

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speed

# Function to convert numbers to Hindi
def number_to_hindi(num):
    hindi_digits = ['शून्य', 'एक', 'दो', 'तीन', 'चार', 'पाँच', 'छः', 'सात', 'आठ', 'नौ', 'दस']
    hindi_teens = ['ग्यारह', 'बारह', 'तेरह', 'चौदह', 'पंद्रह', 'सोलह', 'सत्रह', 'अठारह', 'उन्नीस']
    hindi_tens = ['', 'दस', 'बीस', 'तीस', 'चालीस', 'पचास', 'साठ', 'सत्तर', 'अस्सी', 'नब्बे']
    
    if num == 0:
        return hindi_digits[0]
    if num < 0:
        return "ऋण " + number_to_hindi(abs(num))
    
    if num <= 10:
        return hindi_digits[num]
    elif num <= 19:
        return hindi_teens[num - 11]
    elif num <= 99:
        return hindi_tens[num // 10] + " " + hindi_digits[num % 10] if num % 10 else hindi_tens[num // 10]
    
    return str(num)  # For simplicity, handle only 0-99

# Convert text to speech
def speak_hindi(text):
    engine.say(text)
    engine.runAndWait()

# Speech-to-text function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio, language="hi-IN")
        except:
            return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    data = request.json
    number = re.findall(r'\d+', data.get("text", ""))
    if number:
        num = int(number[0])
        hindi_output = number_to_hindi(num)
        return jsonify({"hindi": hindi_output})
    return jsonify({"error": "No number detected"})

@app.route("/listen", methods=["GET"])
def listen():
    text = recognize_speech()
    if text:
        return jsonify({"text": text})
    return jsonify({"error": "Speech not recognized"})

if __name__ == "__main__":
    app.run(debug=True)
