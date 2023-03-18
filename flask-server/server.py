from flask import Flask, request
import numpy as np
from transformers import pipeline


def create_app():
    app = Flask(__name__)

    app.classifier = pipeline(
        task="zero-shot-classification",
        model="facebook/bart-large-mnli",
        multi_label=True,
    )

    def respond(text):
        output = app.classifier(
            text,
            candidate_labels=[
                "greetings",
                "farewells",
                "prices",
                "h.m.",
                "location",
                "working hours",
                "cargos",
                "hoodies",
                "tote bags",
                "others",
            ],
        )
        labels = [output["labels"][0]]

        for i in range(1, len(output["labels"])):

            if output["scores"][i] > 0.8:
                labels.append(output["labels"][i])

        if "h.m." in labels:
            if "prices" in labels:
                labels.remove("h.m.")
            else:
                h_m_index = labels.index("h.m.")
                labels[h_m_index] = "prices"

        if "cargos" in labels:
            return (
                np.random.choice(
                    [
                        "Hello dear, Thank you for asking about the cargo pants.",
                        "Good day, I appreciate you asking about the cargo pants.",
                        "Hi, Thank you for asking about the cargo pants.",
                    ]
                )
                + "\nThe price of the cargo pants is 400$.\nThe available colors of the cargo pants are: White, Black, Army\nThe available sizes are: XS, small, Medium, Large, XL.\nPlease let us know if you want to ask about anything else."
            )

        elif "hoodies" in labels:
            return (
                np.random.choice(
                    [
                        "Hello dear, Thank you for asking about the hoodies.",
                        "Good day, I appreciate you asking about the hoodies.",
                        "Hi, Thank you for asking about the hoodies.",
                    ]
                )
                + "\nThe price of the hoodies is 400$.\nThe available colors of the hoodies are: White, Black, green\nThe available sizes are: small, Medium, Large, XL, 2XL.\nPlease let us know if you want to ask about anything else."
            )

        elif "tote bags" in labels:
            return (
                np.random.choice(
                    [
                        "Hello dear, Thank you for asking about the tote bags.",
                        "Good day, I appreciate you asking about the tote bags.",
                        "Hi, Thank you for asking about the tote bags.",
                    ]
                )
                + "\nThe price of the tote bags is 100$.\nThe available colors of the tote bags are: White, Black\nYou can pre-order your custom print for extra fees\nPlease let us know if you want to ask about anything else."
            )
        elif "prices" in labels:
            return np.random.choice(
                [
                    "Hello dear, Thank you for asking about the prices.\nCan you please tell us which item are you asking about?",
                    "Good day, I appreciate you asking about the prices.\nCould you please specify which item are you asking about?",
                    "Hi, Thank you for asking about the prices.\nCoud you please tell us which item are you asking about?",
                ]
            )

        elif "location" in labels:
            return (
                np.random.choice(
                    [
                        "Hi, Thank you for asking about out our location.",
                        "Hello, We appreciate you asking about our current location.",
                        "Good day, I appreciate you asking where we are located.",
                    ]
                )
                + "\nCurrently we are an online store so you can order online and your order will arrive in 3 days.\nPlease let us know if you want to ask about anything else."
            )
        elif "working hours" in labels:
            return (
                np.random.choice(
                    [
                        "Hello dear, Thank you for asking about our openning hours.",
                        "Good day, We appreciate you asking about our opening times.",
                        "Hi, Thank you for asking about out working fays.",
                    ]
                )
                + "\nCurrently we are an online store so you can order 24/7 and your order will arrive in 3 days.\nPlease let us know if you want to ask about anything else."
            )

        elif "greetings" in labels:
            return np.random.choice(
                [
                    "Hello dear, How can I help you today?",
                    "Hi there, How may I assist you?",
                    "Hello, What can I do for you?",
                    "Hola, Is there anything I can help you with?",
                ]
            )

        elif "farewells" in labels:
            return np.random.choice(
                ["Bye, Have a great day.", "Good bye.", "Take care.", "See you soon"]
            )
        else:
            return np.random.choice(
                [
                    "I apologize for the inconvenience, but I'm having difficulty understanding your inquiry.\nCould you please kindly formulate your questions related to the brand such as items, colors, sizes, location, and working hours? I would be more than happy to assist you with any information you may require., Have a great day.",
                    "I'm sorry, but I don't understand what you're asking.\nCould you please ask questions about the brand's items, colors, sizes, location, or working hours? I'll be happy to help you with any information you need.",
                    "I'm sorry, I didn't understand your question.\nCould you please ask it again in a different way? If you have any questions about the brand's products, colors, sizes, location, or working hours, just let me know and I'll try my best to help you.",
                ]
            )

    @app.route("/", methods=["POST"])
    def home():

        entry_content = request.json.get("data")

        response = respond(entry_content)

        return {"sender": "Wahdan", "content": response}

    return app
