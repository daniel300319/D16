from django import template

register = template.Library()

BAD_WORDS = {
    'Фекалия': 'Ф******',
    'фекалия': 'ф******',
    'Жопа': 'Ж***',
    'жопа': 'ж***',
    'Вонючка': 'В******',
    'вонючка': 'в******',
    'Хрень': 'Х****',
    'хрень': 'х****',
}

@register.filter()
def censor(value: str):
    words = value.split(' ')
    new_text = ''

    for i in range(len(words)):
        if words[i] in BAD_WORDS:
            words[i] = BAD_WORDS[words[i]]
            new_text += words[i]
            new_text += ' '
        else:
            new_text += words[i]
            new_text += ' '

    return new_text