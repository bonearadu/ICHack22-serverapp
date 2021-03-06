import random

game_started = False
game_register = False

register_time = -1
game_time = -1

points_gained_match = 1
points_gained_miss_match = -1

questions = ["Where are you from?",
             "What is your university?",
             "What are your favourite hobbies?",
             "What is your favourite food?",
             "What is your favourite programming language?",
             "What technology makes the world a worse place?"
             ]


class Player:
    def __init__(self, uid, name, answers):
        self.uid = uid
        self.name = name

        for index in range(0, len(answers)):
            all_answers[index].append(answers[index])

        self.answers = answers
        self.target = []
        self.already_targeted = {}
        self.score = 0

        for index in range(0, len(questions)):
            self.already_targeted[index] = set()
        all_players[uid] = self
        self.create_targets()

    def create_targets(self):
        self.create_next_target()
        self.create_next_target()
        self.create_next_target()
        self.create_next_target()
        self.create_next_target()

    def create_next_target(self):
        rand_index = random.randint(0, len(questions) - 1)
        choice = random.choice(all_answers[rand_index])
        if choice.lower() not in self.already_targeted[rand_index]:
            self.target.append(Target(rand_index, choice))
            self.already_targeted[rand_index].add(choice.lower())
            return questions[rand_index], choice
        else:
            return self.create_next_target()

    def verify_answer(self, question, answer, uid):
        user = all_players[uid]
        index = questions.index(question)
        if user.answers[index].lower() == answer.lower():
            filtered = filter(lambda target: target.question != index or target.answer != answer, self.target)
            self.target = filtered
            if self.all_tasks_completed():
                self.create_targets()
            self.score += points_gained_match
            return True
        else:
            self.score += points_gained_miss_match
            return False

    def all_tasks_completed(self):
        ret = True
        for task in self.target:
            ret = ret and task.completed
        return ret


class Target:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.completed = False


all_players = {}
all_answers = {}
for i in range(0, len(questions)):
    all_answers[i] = []
