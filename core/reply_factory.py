
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if "score" not in session:
        session["score"] = 0

    if(current_question_id == None):
       session["score"] = 0
       return True, ""
     
    if(answer == PYTHON_QUESTION_LIST[(current_question_id - 1)]['answer']):
        session["score"] = session["score"] + 1
        session.modified = True  # Mark the session as modified to ensure it is saved
    return True, ""


def get_next_question(current_question_id):
    if(current_question_id == None):
        return  [PYTHON_QUESTION_LIST[0]['question_text'],PYTHON_QUESTION_LIST[0]['options']] , 1
    else:
        if(current_question_id < len(PYTHON_QUESTION_LIST)):
            return [PYTHON_QUESTION_LIST[current_question_id]['question_text'],PYTHON_QUESTION_LIST[current_question_id]['options']] , current_question_id + 1
        else : 
            return False , -1
    # '''
    # Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    # '''

    # return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    return ["Your Score out of 10 : ",session["score"]]
