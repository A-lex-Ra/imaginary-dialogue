import openai
import apikey


def get_answer_from_ChatGPT(responding_name="name", interlocutor_name="name", topic="topic",
                            last_phrase_of_the_responder="last_phrase_of_the_responder",
                            last_phrase_of_the_interlocutor="last_phrase_of_the_interlocutor"):
    openai.api_key = apikey.key

    messages = [
     {"role": "user",
      "content":
          f"Твоя задача - вести диалог с твоим собеседником так, как делал бы тот человек, кем ты притворяешься и при этом стараться не отклоняться от темы диалога. "
          f"Я ввожу тебе имя твоего собеседника, имя того, кем будешь ты, то, что тебе сказал твой собеседник, то, что ты сказал ему до этого и тему диалога. "
          f"Свой ответ ты должен закончить так же вопросом. "
          f"Не здоровайся с собеседником, если в свое предыдущей фразе ты с ним уже поздоровался."
          f""
          f"Ты - {responding_name}"
          f"Твой собеседник - {interlocutor_name}"
          f"Ваша тема - {topic}"
          f"До этого ты сказал ему:"
          f"{last_phrase_of_the_responder}"
          f"Он сказал тебе:"
          f"{last_phrase_of_the_interlocutor}"}
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=256,
        messages=messages
    )

    chat_response = completion.choices[0].message.content
    return chat_response


def get_answer_from_Davinci(responding_name="name", interlocutor_name="name", topic="topic",
                            last_phrase_of_the_responder="last_phrase_of_the_responder",
                            last_phrase_of_the_interlocutor="last_phrase_of_the_interlocutor"):
    openai.api_key = apikey.key
    promt = f"""Я ввожу тебе имя твоего собеседника, имя того, кем будешь ты, то, что тебе сказал твой собеседник, то, что ты сказал ему до этого и тему диалога. "
          Не здоровайся с собеседником, если в своей предыдущей фразе ты с ним уже поздоровался.
          
          Ты - {responding_name}.
          Твой собеседник - {interlocutor_name}.
          Ваша тема - {topic}.
          До этого ты сказал ему:
          \"{last_phrase_of_the_responder}\".
          Он сказал тебе:
          \"{last_phrase_of_the_interlocutor}\".
          Твой ответ:
          """

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=promt,
        temperature=0.7,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response['choices'][0].text.strip()

# try:
#     print(get_answer_from_ChatGPT(responding_name="Владимир Ленин", interlocutor_name="Иосиф Сталин",
#                               topic="агитация и пропаганда",
#                               last_phrase_of_the_responder="Здравствуйте, товарищ Сталин. Рад видеть вас. Насчет вашего вопроса, "
#                                                            "я думаю, что в капиталистических странах коммунистам необходимо уделять "
#                                                            "больше внимания пропаганде. Мы должны донести до народов этих стран идеи "
#                                                            "социализма и показать, что только в равноправном обществе, основанном на "
#                                                            "коллективизме, люди могут жить в достатке и равенстве. Кроме того, "
#                                                            "мы должны использовать различные формы агитации, такие как митинги, "
#                                                            "листовки, печатные издания и радиовещание, чтобы распространять нашу "
#                                                            "идеологию. Что вы думаете об этом, товарищ Сталин?",
#                               last_phrase_of_the_interlocutor="Я согласен с вами, товарищ Ленин. Пропаганда и агитация являются важными "
#                                                               "инструментами в борьбе за нашу идеологию в капиталистических странах. "
#                                                               "Однако, я считаю, что помимо этого мы также должны строить организации "
#                                                               "и партии в этих странах, чтобы иметь возможность более эффективно "
#                                                               "работать среди местного населения и представлять их интересы. "
#                                                               "Нам нужно убедить людей, что их проблемы и беды связаны с капитализмом, "
#                                                               "а не социализмом, и что наша идеология может привести к реальным изменениям "
#                                                               "в их жизни. Кроме того, мы должны обучать местных активистов, чтобы они "
#                                                               "могли продолжать нашу работу на местах. Что вы думаете об этом подходе, "
#                                                               "товарищ Ленин?"))
# except:
#     pass