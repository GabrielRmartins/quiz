import pytest
from model import Question
from model import Choice

@pytest.fixture
def data():
    question = Question(title='q1',points=5,max_selections=3)
    question.add_choice(text='a',is_correct=False)
    question.add_choice(text='b',is_correct=True)
    question.add_choice(text='c',is_correct=False)
    question.add_choice(text='d',is_correct=False)
    question.add_choice(text='e',is_correct=False)

    return question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_remove_all_choices_from_empty_question():
    question = Question(title='q1')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_remove_all_choice_from_filled_question():
    question = Question(title ='q1')
    question.add_choice('a', False)
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_create_question_with_lower_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points= 0)
        
def test_create_question_with_upper_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points= 101)

def test_create_choice_with_invalid_text():
    with pytest.raises(Exception):
        Choice(id=0, text='',is_correct=False)
    with pytest.raises(Exception):
        Choice(id=0, text='a'*101,is_correct=False)

def test_remove_choice_by_id():
    question = Question(title='q1')
    question.add_choice(text='a',is_correct=False)
    tested_choice = question.choices[0]
    tested_choice_id = tested_choice.id
    question.remove_choice_by_id(tested_choice_id)
    assert len(question.choices) == 0

def test_select_correct_choices():
    question = Question(title='q1')
    c1 = question.add_choice(text='a', is_correct=True)
    result = question.select_choices([c1.id])
    assert result == [c1.id]

def test_select_incorrect_choices():
    question = Question(title='q1')
    c1 = question.add_choice(text='a', is_correct=False)
    result = question.select_choices([c1.id])
    assert result == []

def test_select_multiple_correct_choices():
    question = Question(title='q1',max_selections=3)
    c1 = question.add_choice(text='a',is_correct=True)
    c2 = question.add_choice(text='b',is_correct=True)
    c3 = question.add_choice(text='c',is_correct=True)
    result = question.select_choices([c1.id,c2.id,c3.id])
    assert result == [1,2,3]

def test_select_multiple_incorrect_choices():
    question = Question(title='q1',max_selections=3)
    c1 = question.add_choice(text='a',is_correct=False)
    c2 = question.add_choice(text='b',is_correct=False)
    c3 = question.add_choice(text='c',is_correct=False)
    result = question.select_choices([c1.id,c2.id,c3.id])
    assert result == []

def test_choices_ids_creation(data):
    data.remove_choice_by_id(1)
    data.remove_choice_by_id(2)
    data.remove_choice_by_id(3)
    data.remove_choice_by_id(4)
    data.remove_choice_by_id(5)

    assert len(data.choices) == 0

def test_set_correct_choices(data):
    data.set_correct_choices([1,2,3])
    correct_choices = [choice.id for choice in data.choices if choice.is_correct]

    assert len(correct_choices) == 3
