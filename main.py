import os
import telebot
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

API_KEYY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEYY)

def suggest_categories():
    categories = ["Citizen", "Farmer", "Education Loan", "First-Time Homebuyer", "Entrepreneur Support", "Skill Development", "Tax Relief", "Travel or Work Abroad", "Student Loan Repayment", "Employment Support"]
    return categories

@bot.message_handler(commands=['start'])
def start(message):
    greet(message)

@bot.message_handler(commands=['categories'])
def categories(message):
    categories_list = suggest_categories()
    response = "Here are the available categories:\n" + "\n".join(categories_list)
    response += "\n\nTo check schemes, use the format: /check_schemes age category"
    bot.reply_to(message, response)

def suggest_schemes(age, keywords):
    schemes = []
    matched_category = None

    for keyword in keywords:
        if age < 18:
            schemes.append("You are too young to be eligible for most financial schemes.")
        elif age >= 18:
            if keyword.lower() == "citizen":
                schemes.extend(["1. Retirement Savings Schemes",
                                "2. Health Insurance Schemes",
                                "3. Education Loan Schemes",
                                "4. First-Time Homebuyer Schemes",
                                "5. Entrepreneurship Support Schemes",
                                "6. Skill Development Schemes",
                                "7. Tax Relief Schemes",
                                "8. Travel or Work Abroad Programs",
                                "9. Student Loan Repayment Schemes",
                                "10. Employment Support Schemes"])
                matched_category = "Citizen"
                break  
            elif keyword.lower() == "farmer":
                schemes.extend(["1. Farmer's Insurance Scheme",
                                "2. Subsidized Loans for Farm Equipment",
                                "3. Crop Insurance Scheme",
                                "4. Government Subsidies for Seeds and Fertilizers",
                                "5. Irrigation Scheme",
                                "6. Farmer's Pension Scheme",
                                "7. Agricultural Training Programs",
                                "8. Organic Farming Subsidy",
                                "9. Market Access Support Scheme",
                                "10. Agricultural Research and Development Grants"])
                matched_category = "Farmer"
                break
            elif keyword.lower() == "education":
                schemes.extend(["1. Central Sector Interest Subsidy Scheme",
                                "2. Dr. Ambedkar Central Sector Scheme of Interest Subsidy on Educational Loan for OBCs/EBCs",
                                "3. Vidyalakshmi Education Loan Scheme",
                                "4. State Government Education Loan Schemes",
                                "5. Interest Waiver Schemes for Specific Categories",
                                "6. Collateral-Free Loans for Lower Loan Amounts",
                                "7. Skill Development Loan Schemes",
                                "8. Customized Repayment Options"])
                matched_category = "Education Loan"
                break
            elif keyword.lower() == "homebuyer":
                if age >= 18:
                    schemes.extend(["1. First-Time Homebuyer Grant",
                                    "2. Mortgage Loan with Low Interest Rates",
                                    "3. Government Assistance for Down Payments",
                                    "4. Tax Credits for First-Time Homebuyers",
                                    "5. Homeownership Counseling Programs"])
                    matched_category = "First-Time Homebuyer"
                    break
                else:
                    schemes.append("You must be 18 or older to be eligible for homebuyer schemes.")
                    break
            elif keyword.lower() == "entrepreneur":
                schemes.extend(["1. Startup Loans with Low Interest Rates",
                                "2. Government Grants for Small Businesses",
                                "3. Business Incubation Programs",
                                "4. Mentorship and Training Programs",
                                "5. Tax Incentives for Entrepreneurs"])
                matched_category = "Entrepreneur Support"
                break    

    if matched_category:
        schemes.insert(0, f"Schemes for the category: {matched_category}")

    return schemes

def extract_keywords(scenario):

    tokens = word_tokenize(scenario)

    tagged_tokens = pos_tag(tokens)

    keywords = [word for word, pos in tagged_tokens if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']]
    return keywords

@bot.message_handler(commands=['check_schemes'])
def check_schemes(message):
    try:
        parts = message.text.split()
        age = int(parts[1])
        category = " ".join(parts[2:])

        schemes = suggest_schemes(age, [category])  
        if schemes:
            bot.reply_to(message, f"The schemes you may be eligible for are:\n\n" + "\n".join(schemes))
        else:
            bot.reply_to(message, "Sorry, there are no schemes available for your age or category.")
    except (ValueError, IndexError):
        bot.reply_to(message, "Please provide a valid age and category with the /check_schemes command.")

@bot.message_handler(commands=['help'])
def help(message):
    response = "Available commands:\n"
    response += "/start_the_bot - Start the bot\n"
    response += "/categories - View available categories\n"
    response += "/check_schemes age category - Check schemes based on age and category\n"
    response += "/help - Display this help message"
    bot.reply_to(message, response)

@bot.message_handler(commands=['greet'])
def greet(message):
    response = "Hello! How can I assist you today?\n"
    response += "You can utilize /help to discover the available commands.\n"
    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: message.text.lower() == '/start_the_bot')
def welcome(message):
    response = "Welcome! Please choose a category to explore schemes. Use /categories to see available categories. Or you can provide a scenario for personalized suggestions."
    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    scenario_keywords = extract_keywords(message.text)
    print("Scenario keywords:", scenario_keywords) 
    if scenario_keywords:
        schemes = suggest_schemes(25, scenario_keywords)
        if schemes:
            bot.reply_to(message, f"Based on your scenario, you may be eligible for the following schemes:\n\n" + "\n".join(schemes))
        else:
            bot.reply_to(message, "Sorry, no relevant schemes found for your scenario.")

bot.polling()
