# TL;DR: Emakume-a kalean-ozen-era galdu zen. Katu-ak emakume-ari sagu-a ekarri zen. 

AKA "Agglutination is So Much Easier on the Brain than Inflection"

To solve this, reading [the Wikipedia article about Basque grammar](https://en.wikipedia.org/wiki/Basque_grammar) is extremely helpful.

First, we must figure out what Basque words correspond to what nouns, and what are the case markers.
From reading the Wikipedia article linked above, we know that the parts after the dash are suffixes, so we need to track them separately.

In sentence 2, the only noun is 'улица', and the only word with a suffix is 'kalean-a'.
Therefore, 'kalean' is 'улица', and '-a' is the nominative case marker.

In sentence 1, the nouns are 'улица' and 'женщина', and the word with the nominative case is 'emakume-a'.
Therefore, 'emakume' is 'женщина' and '-era' is the locative marker.

In sentence 4, the nouns are 'кошка' and 'женщина', and the word with the nominative case is 'emakume-a'.
Therefore, 'katu' is 'кошка' and '-ari' is the dative marker.

We now know all the nouns necessary to form the sentences, but not all the verbs.
From Wikipedia, we know that Basque primarily has a subject-object-verb (SOV) word order, so the part after the nouns is the verb phrase.
The verbs we are looking for are 'lose-RFLX' and 'bring-P'.
The latter is used in a sentence and so can be taken from there. 
The former, on the other hand, is only found in quotes and either as an adjective or as a question phrase.

| Verb | Potential Basque |
|---|---|
| lose-RFLX | galdu zara |
| bring | ekarri zen |

Reading the [Wikipedia article on Basque verbs](https://en.wikipedia.org/wiki/Basque_verbs), we know that 'zara' is the polist second-person form meaning 'you are', and 'zen' is an allocutive form meaning '{smth} was'.
They are thus not parts of the verbs.
We can also double-check our assumption using Google Translate.

| Verb | Basque |
|---|---|
| lose-RFLX | [galdu](https://translate.google.com/#eu/en/galdu) |
| bring | [ekarri](https://translate.google.com/#eu/en/ekarri) |

Next, we need to find the adjective 'noisy'.
The only sentence which has it is sentence 2.
Since we already know that the last word is the form marker, the penultimate word -- 'ozen' -- means 'noisy'.

Finally, we need to examine sentence 3, for it has a clearly-defined agent and patient.
In cases like these, the agent is marked with '-ak' and the patient with '-a'.

We have now found all the required words.
Now, we shall parse the original sentence the way it shall be laid out in Basque.

| Russian | Parsing |
|---|---|
| Женщина потерялась на шумной улице. | woman-NOM street-noisy-LOC lose-RFLX.|
| Кошка принесла женщине мышь. | cat-AGENT woman-DAT mouse-PATIENT bring. |

Then, we shall replace the parts that we have translated.

| Parsing | Potential Basque |
|---|---|
| woman-NOM street-noisy-LOC lose-RFLX.| Emakume-a kalean-ozen-era galdu zen. |
| cat-AGENT woman-DAT mouse-PATIENT bring. | Katu-ak emakume-ari sagu-a ekarri zen. |

As a sanity test, we can use [Google](https://translate.google.com/#eu/en/Emakume-a%20kalean-ozen-era%20galdu%20zen.) [Translate](https://translate.google.com/#eu/en/Katu-ak%20emakume-ari%20sagu-a%20ekarri%20zen.),
which shows that in the first sentence, I said 'to the street' rather then 'on the street' as was the goal, and that I also have switched around the agent and patient in the second one.
However, there's not much I can do about that, since, in the first sentence, I used the locative case, which does not have direction encoded in it.
As for the second sentence, even if I [switch around the markers](https://translate.google.com/#eu/en/Katu-a%20emakume-ari%20sagu-ak%20ekarri%20zen.), the needed result is not achieved, as it just transposes the plural-vs.-singular form.
Also, rather annoyingly, Google Translate doesn't pick up the adjective in the first sentence, but does [if that section is isolated](https://translate.google.com/#eu/en/kalean-ozen-a), so I can't do much about that either. 
