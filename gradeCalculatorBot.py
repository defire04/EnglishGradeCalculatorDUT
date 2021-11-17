import telebot
import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "Напишите оценки одним сообщением")
    bot.register_next_step_handler(msg, countingFormula)


def countingFormula(message):
    grade = message.text.replace(" ", "+")
    counter = 1
    for element in grade:
        if (element == "+"):
            counter +=1

    averageGrade = eval(grade) / counter

    passingScore = 40 # необходимое количество балов, для допуска к экзамена

    global resultFormula
    resultFormula = (averageGrade * 0.05 + 0.4) * passingScore 
    
    bot.send_message(message.chat.id, resultFormula)
    bot.send_message(message.chat.id, "Отправьте бал итогового теста")


@bot.message_handler(content_types='text')
def finalTest(message):
    grade = float(message.text)

    global result
    result = resultFormula + grade
    
    bot.send_message(message.chat.id, result)
  
    msg = bot.send_message(message.chat.id, "Отправьте итоговую экзаменационую оценку")
    bot.register_next_step_handler(msg, finalExam)

def finalExam(message):
    grade = float(message.text)
    finalRes = result + grade
    bot.send_message(message.chat.id, "Итоговая оценка " + str(finalRes))


if __name__ == "__main__":
    bot.infinity_polling()