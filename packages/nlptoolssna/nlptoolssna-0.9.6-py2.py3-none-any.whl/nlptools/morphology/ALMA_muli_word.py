from nlptools.morphology import settings 
from nlptools.utils.parser import arStrip


def ALMA_multi_word(multi_word, n_gram):
    undiac_multi_word = arStrip(multi_word, True, True, True, False, True, False)  # diacs , smallDiacs , shaddah ,  digit , alif , specialChars
    #print(settings.five_grams_dict[undiac_multi_word])
    result_word = []
    if n_gram == 2:
        if undiac_multi_word in settings.two_grams_dict.keys():
           result_word = settings.two_grams_dict[undiac_multi_word]
       #result_word = json.loads(serializers.serialize('json',models.multi_word_lemmas.objects.filter(n_gram=2).filter(undiac_multi_word_lemma=undiac_multi_word)))
    elif n_gram == 3:    
        if undiac_multi_word in settings.three_grams_dict.keys():
           result_word = settings.three_grams_dict[undiac_multi_word]
       #result_word = json.loads(serializers.serialize('json',models.multi_word_lemmas.objects.filter(n_gram=3).filter(undiac_multi_word_lemma=undiac_multi_word)))
    elif n_gram == 4:    
        if undiac_multi_word in settings.four_grams_dict.keys():
           result_word = settings.four_grams_dict[undiac_multi_word]
       #result_word = json.loads(serializers.serialize('json',models.multi_word_lemmas.objects.filter(n_gram=4).filter(undiac_multi_word_lemma=undiac_multi_word))) 
    elif n_gram == 5:
        if undiac_multi_word in settings.five_grams_dict.keys():
           result_word = settings.five_grams_dict[undiac_multi_word]
       #result_word = json.loads(serializers.serialize('json',models.multi_word_lemmas.objects.filter(n_gram=5).filter(undiac_multi_word_lemma=undiac_multi_word)))
    
    return result_word   