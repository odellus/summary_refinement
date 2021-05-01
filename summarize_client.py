import requests
import json
from urllib.parse import quote

article = """Karl Heinrich Marx (German: [maʁks]; 5 May 1818 – 14 March 1883[13]) was a German philosopher, economist, historian, sociologist, political theorist, journalist and socialist revolutionary. Born in Trier, Germany, Marx studied law and philosophy at university. He married Jenny von Westphalen in 1843. Due to his political publications, Marx became stateless and lived in exile with his wife and children in London for decades, where he continued to develop his thought in collaboration with German thinker Friedrich Engels and publish his writings, researching in the reading room of the British Museum. His best-known titles are the 1848 pamphlet The Communist Manifesto and the three-volume Das Kapital (1867–1883). Marx's political and philosophical thought had enormous influence on subsequent intellectual, economic and political history. His name has been used as an adjective, a noun, and a school of social theory.\n\nMarx's critical theories about society, economics, and politics, collectively understood as Marxism, hold that human societies develop through class conflict. In the capitalist mode of production, this manifests itself in the conflict between the ruling classes (known as the bourgeoisie) that control the means of production and the working classes (known as the proletariat) that enable these means by selling their labour-power in return for wages.[14] Employing a critical approach known as historical materialism, Marx predicted that capitalism produced internal tensions like previous socioeconomic systems and that those would lead to its self-destruction and replacement by a new system known as the socialist mode of production. For Marx, class antagonisms under capitalism, owing in part to its instability and crisis-prone nature, would eventuate the working class' development of class consciousness, leading to their conquest of political power and eventually the establishment of a classless, communist society constituted by a free association of producers.[15] Marx actively pressed for its implementation, arguing that the working class should carry out organised proletarian revolutionary action to topple capitalism and bring about socio-economic emancipation.[16]\n\nMarx has been described as one of the most influential figures in human history and his work has been both lauded and criticised.[17] His work in economics laid the basis for some current theories about labour and its relation to capital.[18][19][20] Many intellectuals, labour unions, artists and political parties worldwide have been influenced by Marx's work, with many modifying or adapting his ideas. Marx is typically cited as one of the principal architects of modern social science.[21][22]
"""
article_id = '25dgdj27d8'

url = 'http://127.0.0.1:5001/summarizer'

def summarizer_client(article=article, article_id=article_id, url=url):
    article = 'article=' + quote(article)
    article_id = 'article_id=' + quote(article_id)
    data = {'article': article, 'article_id': article_id}
    body = json.dumps(data)
    result = requests.post(url, data=body)
    print(result.json())

if __name__ == '__main__':
    summarizer_client(article)
