# Questo file serve per la pagina di index, permette di creare un filtro personalizzato
# da usare nel linguaggio di template di Django. Ho creato il metodo return_item che mi
# permette di ottenere l'elemento nell'indice i della lista l.
# Ricordarsi di aggiungere {% load users_extras %} all'inizio del file html altrimenti
# non funziona. Ricordarsi di aggiungere il file __init__.py per farlo leggere da
# Python come tipo.

from django import template

register = template.Library()


@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None
