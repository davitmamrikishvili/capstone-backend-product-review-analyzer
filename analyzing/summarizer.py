from transformers import pipeline
from typing import List, Union

class Summarizer:
    
    def __init__(self, *args, **kwargs):
        self._pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", *args, **kwargs)
    
    def summarize(self, prompt: Union[str, List[str]], *args, **kwargs) -> str:
        if isinstance(prompt, list):
            prompt = '\n'.join(prompt)
        return self._pipeline(prompt, *args, **kwargs)[0]['summary_text']
    
# lst = [
#     """Amazing pad Thai! Great flavor, barely any bean sprouts but overall delicious.

# Avoid the Thai tea unless you like your drinks extremely sweet. I mentioned it to the waitress and it turns out the teas are premade in the morning so they can't control the sweetness.""",
# """I've been meaning to try Pai for a while now, and I finally got the chance! When I first arrived, there was a big lineup outside, which had me worried, but the wait was surprisingly quick as I was seated in about 15 minutes.

# To start, my party ordered the Mango Slaw. I chose this dish because I recently went to Lee and fell in love with their slaw, so I was curious to compare. While the ingredients at Pai were fresh, the vinegar flavor was quite strong and overpowered the dish, so I wasn't the biggest fan and I probably wouldn't order it again.

# For the mains, my party ordered the Green Curry Chicken and Khao Soi, while I went with the Pad See Ew. The food arrived quickly, and everything tasted incredibly fresh and flavorful. The Pad See Ew had a great smoky taste, and the noodles were tender. The Green Curry Chicken had a nice mild spice to it, and the Khao Soi had a nice cream broth.

# Beyond the food, the service was really good as the staff was super friendly, and my party didn't have to wait long for any of the dishes. I'd definitely come to Pai again to try some of the other dishes!""",
# """Pai Northern Thai Kitchen offers such a vibrant experience. I loved colorful lighting in the restaurant and the overall vibe at the bar.

# We didn't have any reservations and the wait was 30 minutes so hung out at the bar which was a great experience. There's a large variety of drinks that were Toronto themed which caught my attention. They had drinks like "Cherry Trent Jr" and "Scotchie Barnes" which is playful. I chose the Thai Mojito.

# Now when it came to dinner, the food was my highlight. I ordered the Green Curry Chicken and I must say that this was probably my favorite Green Curry Chicken ever. One thing that made this different than all others is that it's served in a coconut. The dish itself was tasty but one thing that I particularly loved was scraping the coconut and having a dessert-like experience afterward.

# Overall this place was great. Great location, wonderful ambiance, and enthusiastic and knowledgeable staff. I appreciated that they were able to help my colleague who had a gluten and dairy allergy."""
# ]
# summarizer = Summarizer()
# result = summarizer.summarize(lst, max_length=100, min_length=30)
# print(result)
#  Pai Northern Thai Kitchen offers such a vibrant experience . Great location, wonderful ambiance, and enthusiastic and knowledgeable staff . Avoid the Thai tea unless you like your drinks extremely sweet .
